#!/usr/bin/env python3
"""
Create WordPress drafts from Le Phare source files.

V1.2 scope:
- parse one source file or a whole directory from 07_A_Publier
- extract title, slug, excerpt, seo meta, body
- strip internal working blocks
- convert a markdown-like structure into simple HTML
- create a WordPress draft through the REST API
- assign WordPress categories and tags from index_editorial.csv
- optionally update index_editorial.csv with wp_draft status and draft URL
- process articles in batch with a final success/error summary

No image upload.
"""

from __future__ import annotations

import argparse
import base64
import csv
import dataclasses
import json
import re
import ssl
import sys
from urllib import parse
from dataclasses import dataclass
from html import escape
from pathlib import Path
from urllib import request, error


META_LINE_RE = re.compile(r"^(?P<key>[^:\n]+)\s*:\s*(?P<value>.*)$")


@dataclass
class Config:
    site_url: str
    username: str
    application_password: str
    verify_ssl: bool = True


@dataclass
class Article:
    path: Path
    title: str
    slug: str
    excerpt: str
    seo_keyword: str
    seo_description: str
    body_markdown: str
    body_html: str
    article_id: str


@dataclass
class IndexRecord:
    article_id: str
    status: str
    wordpress_url: str
    wordpress_slug: str
    categories: list[str]
    tags: list[str]


@dataclass
class ArticleRunResult:
    path: str
    article_id: str
    title: str
    status: str
    skipped: bool
    wordpress_id: int | None = None
    wordpress_slug: str = ""
    wordpress_link: str = ""
    categories: list[str] | None = None
    tags: list[str] | None = None
    index_updated: bool = False
    error: str = ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create WordPress drafts from Le Phare source files.")
    parser.add_argument("source_path", help="Path to a source markdown file or a directory")
    parser.add_argument("--config", help="Path to local JSON config file")
    parser.add_argument("--dry-run", action="store_true", help="Parse and render without creating a WordPress draft")
    parser.add_argument("--index", help="Path to index_editorial.csv to update after draft creation")
    parser.add_argument("--force", action="store_true", help="Push again even if the article is already marked as wp_draft")
    return parser.parse_args()


def load_config(config_path: str | None) -> Config:
    if config_path:
        raw = json.loads(Path(config_path).read_text(encoding="utf-8"))
    else:
        env_site = _get_env("LP_WP_SITE_URL")
        env_user = _get_env("LP_WP_USERNAME")
        env_password = _get_env("LP_WP_APPLICATION_PASSWORD")
        raw = {
            "site_url": env_site,
            "username": env_user,
            "application_password": env_password,
            "verify_ssl": True,
        }

    missing = [key for key in ("site_url", "username", "application_password") if not raw.get(key)]
    if missing:
        raise ValueError(f"Missing WordPress config value(s): {', '.join(missing)}")

    return Config(
        site_url=str(raw["site_url"]).rstrip("/"),
        username=str(raw["username"]),
        application_password=str(raw["application_password"]),
        verify_ssl=bool(raw.get("verify_ssl", True)),
    )


def _get_env(name: str) -> str:
    import os

    return os.environ.get(name, "")


def parse_article(path: Path) -> Article:
    text = path.read_text(encoding="utf-8")
    metadata, remainder = split_frontmatter(text)
    title = metadata.get("Titre", "").strip()
    article_id = metadata.get("ID article", "").strip()
    excerpt = metadata.get("Resume court (500 caracteres max)", "").strip()
    if not title:
        raise ValueError("Missing required metadata: Titre")

    seo_keyword, seo_description, body = extract_seo_and_body(remainder)
    slug = extract_slug(body)

    if not slug:
        raise ValueError("Missing required field: Slug propose")

    clean_body = strip_internal_sections(body)
    html = markdown_like_to_html(clean_body)
    if not html.strip():
        raise ValueError("Article body is empty after cleanup")

    return Article(
        path=path,
        title=title,
        slug=slug,
        excerpt=excerpt,
        seo_keyword=seo_keyword,
        seo_description=seo_description,
        body_markdown=clean_body,
        body_html=html,
        article_id=article_id,
    )


def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    lines = text.splitlines()
    metadata: dict[str, str] = {}
    idx = 0
    while idx < len(lines):
        line = lines[idx].strip("\ufeff")
        if line == "---":
            idx += 1
            break
        match = META_LINE_RE.match(line)
        if match:
            metadata[match.group("key").strip()] = match.group("value").strip()
            idx += 1
            continue
        idx += 1
    return metadata, "\n".join(lines[idx:])


def extract_seo_and_body(remainder: str) -> tuple[str, str, str]:
    lines = remainder.splitlines()
    seo_keyword = ""
    seo_description = ""
    body_start = 0

    if lines and lines[0].strip() == "# SEO":
        for idx, line in enumerate(lines[1:], start=1):
            stripped = line.strip()
            if stripped == "---":
                body_start = idx + 1
                break
            match = META_LINE_RE.match(stripped)
            if match:
                key = match.group("key").strip()
                value = match.group("value").strip()
                if key == "Mot-cle principal":
                    seo_keyword = value
                elif key == "Meta-description":
                    seo_description = value
        else:
            body_start = len(lines)
    body = "\n".join(lines[body_start:]).lstrip()
    return seo_keyword, seo_description, body


def extract_slug(body: str) -> str:
    match = re.search(r"^Slug propose\s*:\s*(.+)$", body, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def strip_internal_sections(body: str) -> str:
    lines = body.splitlines()
    kept: list[str] = []
    skip = False
    first_h1_removed = False
    for line in lines:
        stripped = line.strip()
        if stripped in {"## Bloc image WordPress", "## Bloc publication"}:
            skip = True
            continue
        if skip and stripped.startswith("## "):
            skip = False
        if skip:
            continue
        if stripped.startswith("Slug propose :") or stripped.startswith("Statut publication :") or stripped.startswith("Date cible publication :"):
            continue
        if not first_h1_removed and stripped.startswith("# "):
            first_h1_removed = True
            continue
        kept.append(line)
    return "\n".join(kept).strip()


def render_inline_markdown(text: str) -> str:
    parts: list[str] = []
    cursor = 0
    for match in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", text):
        start, end = match.span()
        if start > cursor:
            parts.append(escape(text[cursor:start]))
        label = match.group(1).strip()
        url = match.group(2).strip()
        parts.append(f'<a href="{escape(url, quote=True)}">{escape(label)}</a>')
        cursor = end
    if cursor < len(text):
        parts.append(escape(text[cursor:]))
    return "".join(parts)


def markdown_like_to_html(text: str) -> str:
    blocks = text.splitlines()
    html_parts: list[str] = []
    paragraph_buffer: list[str] = []
    list_buffer: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph_buffer
        if paragraph_buffer:
            html_parts.append(f"<p>{render_inline_markdown(' '.join(paragraph_buffer).strip())}</p>")
            paragraph_buffer = []

    def flush_list() -> None:
        nonlocal list_buffer
        if list_buffer:
            items = "".join(f"<li>{render_inline_markdown(item)}</li>" for item in list_buffer)
            html_parts.append(f"<ul>{items}</ul>")
            list_buffer = []

    for raw_line in blocks:
        line = raw_line.strip()
        if not line:
            flush_paragraph()
            flush_list()
            continue

        if line.startswith("# "):
            flush_paragraph()
            flush_list()
            html_parts.append(f"<h1>{escape(line[2:].strip())}</h1>")
            continue

        if line.startswith("## "):
            flush_paragraph()
            flush_list()
            html_parts.append(f"<h2>{escape(line[3:].strip())}</h2>")
            continue

        if line.startswith("### "):
            flush_paragraph()
            flush_list()
            html_parts.append(f"<h3>{escape(line[4:].strip())}</h3>")
            continue

        if re.match(r"^[-*]\s+", line):
            flush_paragraph()
            list_buffer.append(re.sub(r"^[-*]\s+", "", line).strip())
            continue

        if re.match(r"^\d+\.\s+", line):
            flush_paragraph()
            list_buffer.append(re.sub(r"^\d+\.\s+", "", line).strip())
            continue

        flush_list()
        paragraph_buffer.append(line)

    flush_paragraph()
    flush_list()
    return "\n".join(html_parts)


def create_wordpress_draft(
    article: Article,
    config: Config,
    category_ids: list[int] | None = None,
    tag_ids: list[int] | None = None,
) -> dict:
    endpoint = f"{config.site_url}/wp-json/wp/v2/posts"
    payload = {
        "title": article.title,
        "slug": article.slug,
        "content": article.body_html,
        "status": "draft",
    }
    if article.excerpt:
        payload["excerpt"] = article.excerpt
    if category_ids:
        payload["categories"] = category_ids
    if tag_ids:
        payload["tags"] = tag_ids

    return wordpress_request_json(config, endpoint, method="POST", payload=payload)


def load_index_record(index_path: Path, article_id: str) -> IndexRecord:
    if not article_id:
        raise ValueError("Cannot read index without article ID")
    if not index_path.exists():
        raise FileNotFoundError(f"Index file not found: {index_path}")

    with index_path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            if row.get("ID", "").strip() == article_id:
                return IndexRecord(
                    article_id=article_id,
                    status=row.get("Statut", "").strip(),
                    wordpress_url=row.get("URL_WordPress", "").strip(),
                    wordpress_slug=row.get("Slug_WordPress", "").strip(),
                    categories=split_multi_value_field(row.get("Categorie_WP", "")),
                    tags=split_multi_value_field(row.get("Tags_WP", "")),
                )

    raise ValueError(f"Article ID not found in index: {article_id}")


def split_multi_value_field(raw_value: str) -> list[str]:
    return [part.strip() for part in raw_value.split(";") if part.strip()]


def resolve_taxonomy_ids(config: Config, taxonomy: str, values: list[str]) -> list[int]:
    term_ids: list[int] = []
    for value in values:
        term = get_or_create_term(config, taxonomy, value)
        term_id = term.get("id")
        if not isinstance(term_id, int):
            raise RuntimeError(f"Invalid {taxonomy} term returned for '{value}': {term}")
        term_ids.append(term_id)
    return term_ids


def get_or_create_term(config: Config, taxonomy: str, raw_value: str) -> dict:
    normalized = raw_value.strip()
    if not normalized:
        raise ValueError(f"Empty taxonomy value for {taxonomy}")

    slug_candidate = slugify_term(normalized)
    base_endpoint = f"{config.site_url}/wp-json/wp/v2/{taxonomy}"

    for endpoint in (
        f"{base_endpoint}?per_page=100&slug={parse.quote(slug_candidate)}",
        f"{base_endpoint}?per_page=100&search={parse.quote(normalized)}",
    ):
        items = wordpress_request_json(config, endpoint, method="GET")
        if isinstance(items, list):
            exact = pick_matching_term(items, normalized, slug_candidate)
            if exact:
                return exact

    payload = {
        "name": normalized,
        "slug": slug_candidate,
    }
    created = wordpress_request_json(config, base_endpoint, method="POST", payload=payload)
    if not isinstance(created, dict):
        raise RuntimeError(f"Unexpected create response for {taxonomy}: {created}")
    return created


def pick_matching_term(items: list[dict], raw_value: str, slug_candidate: str) -> dict | None:
    raw_value_lower = raw_value.casefold()
    slug_lower = slug_candidate.casefold()
    for item in items:
        name = str(item.get("name", "")).strip().casefold()
        slug = str(item.get("slug", "")).strip().casefold()
        if name == raw_value_lower or slug == raw_value_lower or slug == slug_lower:
            return item
    return None


def slugify_term(value: str) -> str:
    slug = value.strip().casefold()
    slug = re.sub(r"\s+", "-", slug)
    slug = re.sub(r"[^a-z0-9-]", "-", slug)
    slug = re.sub(r"-{2,}", "-", slug)
    return slug.strip("-")


def wordpress_request_json(config: Config, endpoint: str, method: str, payload: dict | None = None) -> dict | list:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = request.Request(
        endpoint,
        data=data,
        headers=build_auth_headers(config, include_json=payload is not None),
        method=method,
    )

    try:
        with request.urlopen(req, context=build_ssl_context(config)) as response:
            return json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"WordPress API error {exc.code}: {detail}") from exc


def build_auth_headers(config: Config, include_json: bool) -> dict[str, str]:
    token = base64.b64encode(f"{config.username}:{config.application_password}".encode("utf-8")).decode("ascii")
    headers = {
        "Authorization": f"Basic {token}",
    }
    if include_json:
        headers["Content-Type"] = "application/json"
    return headers


def build_ssl_context(config: Config) -> ssl.SSLContext:
    # Force a modern TLS floor while still allowing an opt-out for certificate
    # validation in local troubleshooting scenarios.
    if config.verify_ssl:
        context = ssl.create_default_context()
    else:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

    if hasattr(ssl, "TLSVersion"):
        context.minimum_version = ssl.TLSVersion.TLSv1_2
    return context


def update_index(index_path: Path, article: Article, wp_result: dict) -> bool:
    if not article.article_id:
        raise ValueError("Cannot update index without 'ID article'")
    if not index_path.exists():
        raise FileNotFoundError(f"Index file not found: {index_path}")

    with index_path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        fieldnames = reader.fieldnames or []

    updated = False
    for row in rows:
        if row.get("ID", "").strip() == article.article_id:
            row["Statut"] = "wp_draft"
            row["URL_WordPress"] = str(wp_result.get("link", "") or "")
            row["Slug_WordPress"] = str(wp_result.get("slug", "") or article.slug)
            row["Date_derniere_maj"] = _today_iso()
            existing = row.get("Remarques", "").strip()
            note = "Brouillon WordPress créé via script"
            row["Remarques"] = note if not existing else f"{existing} | {note}"
            updated = True
            break

    if not updated:
        raise ValueError(f"Article ID not found in index: {article.article_id}")

    normalized_rows: list[dict[str, str]] = []
    for row in rows:
        normalized_rows.append({fieldname: row.get(fieldname, "") for fieldname in fieldnames})

    with index_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(normalized_rows)
    return True


def _today_iso() -> str:
    from datetime import date

    return date.today().isoformat()


def collect_source_files(source_path: Path) -> list[Path]:
    if not source_path.exists():
        raise FileNotFoundError(f"Source path not found: {source_path}")
    if source_path.is_file():
        return [source_path]

    files = sorted(path for path in source_path.rglob("*.md") if path.is_file())
    if not files:
        raise ValueError(f"No markdown files found in directory: {source_path}")
    return files


def should_skip_publish(index_record: IndexRecord | None, force: bool) -> bool:
    if force or not index_record:
        return False
    return index_record.status == "wp_draft" and bool(index_record.wordpress_url)


def build_dry_run_payload(article: Article, index_record: IndexRecord | None, multi_file: bool) -> dict:
    payload = {
        "path": str(article.path),
        "article_id": article.article_id,
        "title": article.title,
        "slug": article.slug,
        "excerpt": article.excerpt,
        "seo_keyword": article.seo_keyword,
        "seo_description": article.seo_description,
        "categories": index_record.categories if index_record else [],
        "tags": index_record.tags if index_record else [],
    }
    if not multi_file:
        payload["html_preview"] = article.body_html[:1500]
    return payload


def process_article(path: Path, args: argparse.Namespace, config: Config | None, multi_file: bool) -> ArticleRunResult | dict:
    article = parse_article(path)
    index_record = load_index_record(Path(args.index), article.article_id) if args.index else None

    if args.dry_run:
        return build_dry_run_payload(article, index_record, multi_file)

    if config is None:
        raise ValueError("Config is required for publishing")

    if should_skip_publish(index_record, args.force):
        return ArticleRunResult(
            path=str(article.path),
            article_id=article.article_id,
            title=article.title,
            status="skipped",
            skipped=True,
            wordpress_slug=index_record.wordpress_slug if index_record else "",
            wordpress_link=index_record.wordpress_url if index_record else "",
            categories=index_record.categories if index_record else [],
            tags=index_record.tags if index_record else [],
        )

    category_ids = resolve_taxonomy_ids(config, "categories", index_record.categories) if index_record else []
    tag_ids = resolve_taxonomy_ids(config, "tags", index_record.tags) if index_record else []
    result = create_wordpress_draft(article, config, category_ids=category_ids, tag_ids=tag_ids)
    index_updated = False
    if args.index:
        index_updated = update_index(Path(args.index), article, result)

    wordpress_id = result.get("id")
    return ArticleRunResult(
        path=str(article.path),
        article_id=article.article_id,
        title=article.title,
        status=str(result.get("status", "")),
        skipped=False,
        wordpress_id=wordpress_id if isinstance(wordpress_id, int) else None,
        wordpress_slug=str(result.get("slug", "") or article.slug),
        wordpress_link=str(result.get("link", "") or ""),
        categories=index_record.categories if index_record else [],
        tags=index_record.tags if index_record else [],
        index_updated=index_updated,
    )


def render_batch_summary(results: list[ArticleRunResult], source_path: Path) -> dict:
    return {
        "source": str(source_path),
        "total": len(results),
        "created": sum(1 for item in results if item.status == "draft" and not item.skipped),
        "skipped": sum(1 for item in results if item.skipped),
        "failed": sum(1 for item in results if item.error),
        "items": [
            {
                "path": item.path,
                "article_id": item.article_id,
                "title": item.title,
                "status": item.status,
                "wordpress_id": item.wordpress_id,
                "slug": item.wordpress_slug,
                "link": item.wordpress_link,
                "categories": item.categories or [],
                "tags": item.tags or [],
                "index_updated": item.index_updated,
                "error": item.error,
            }
            for item in results
        ],
    }


def main() -> int:
    args = parse_args()
    try:
        source_path = Path(args.source_path)
        source_files = collect_source_files(source_path)
    except Exception as exc:
        print(f"Source error: {exc}", file=sys.stderr)
        return 1

    multi_file = len(source_files) > 1
    try:
        config = None if args.dry_run else load_config(args.config)
    except Exception as exc:
        print(f"Publish error: {exc}", file=sys.stderr)
        return 1

    if not multi_file:
        try:
            result = process_article(source_files[0], args, config, multi_file=False)
        except Exception as exc:
            print(f"Publish error: {exc}", file=sys.stderr)
            return 1

        if isinstance(result, ArticleRunResult):
            output = dataclasses.asdict(result)
        else:
            output = result
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return 0

    if args.dry_run:
        previews: list[dict] = []
        errors: list[dict] = []
        for path in source_files:
            try:
                previews.append(process_article(path, args, config, multi_file=True))
            except Exception as exc:
                errors.append({"path": str(path), "error": str(exc)})

        print(json.dumps(
            {
                "source": str(source_path),
                "total": len(source_files),
                "ok": len(previews),
                "failed": len(errors),
                "items": previews,
                "errors": errors,
            },
            ensure_ascii=False,
            indent=2,
        ))
        return 0 if not errors else 1

    results: list[ArticleRunResult] = []
    for path in source_files:
        try:
            article_result = process_article(path, args, config, multi_file=True)
            assert isinstance(article_result, ArticleRunResult)
            results.append(article_result)
        except Exception as exc:
            results.append(ArticleRunResult(
                path=str(path),
                article_id="",
                title=path.name,
                status="error",
                skipped=False,
                error=str(exc),
            ))

    print(json.dumps(render_batch_summary(results, source_path), ensure_ascii=False, indent=2))
    return 0 if not any(item.error for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
