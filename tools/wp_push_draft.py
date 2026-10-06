#!/usr/bin/env python3
"""
Create WordPress drafts from Le Phare source files.

V1.3 scope (V2 routine):
- slug auto-dérivé du nom de fichier si 'Slug propose' absent (évite le crash NoneType sur re-run)
- champs metadata None → "" défensivement (protège .strip() sur valeurs manquantes)
- messages d'erreur enrichis sur champs obligatoires manquants

V1.2 scope:
- parse one source file or a whole directory from 07_A_Publier
- extract title, slug, excerpt, seo meta (Mot-cle principal, Meta-description, optional Titre SEO -> Rank Math)
- strip internal working blocks
- convert a markdown-like structure into simple HTML (titres #/##/###, listes, paragraphes ; en ligne : liens [texte](url), gras **texte** → <strong>)
- create a WordPress draft through the REST API
- assign WordPress categories and tags from index_editorial.csv
- optionally update index_editorial.csv with wp_draft status and draft URL
- reuse WordPress featured images by category/tag slug via optional wp_featured_media.local.json (IDs mediatheque ou noms de fichier pour retrouver un media existant)
- push Rank Math SEO fields via Rank Math REST route POST rankmath/v1/updateMeta (after post exists); enable Headless CMS Support in Rank Math if the route is blocked
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


TOOLS_DIR = Path(__file__).resolve().parent
FEATURED_MEDIA_MAP_DEFAULT = TOOLS_DIR / "wp_featured_media.local.json"

from index_editorial_utils import read_index, safe_str, write_index  # noqa: E402


VISIBILITY_TAG = "a-la-une"
META_LINE_RE = re.compile(r"^(?P<key>[^:\n]+)\s*:\s*(?P<value>.*)$")


@dataclass
class Config:
    site_url: str
    username: str
    application_password: str
    verify_ssl: bool = True
    push_rank_math_meta: bool = True


@dataclass
class Article:
    path: Path
    title: str
    slug: str
    excerpt: str
    seo_keyword: str
    seo_description: str
    seo_title: str
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
    featured_media_id: int | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create WordPress drafts from Le Phare source files.")
    parser.add_argument("source_path", help="Path to a source markdown file or a directory")
    parser.add_argument("--config", help="Path to local JSON config file")
    parser.add_argument("--dry-run", action="store_true", help="Parse and render without creating a WordPress draft")
    parser.add_argument("--index", help="Path to index_editorial.csv to update after draft creation")
    parser.add_argument("--force", action="store_true", help="Push again even if the article is already marked as wp_draft")
    parser.add_argument(
        "--featured-media-map",
        default=str(FEATURED_MEDIA_MAP_DEFAULT),
        help="JSON map category/tag slug -> WordPress media ID or filename (existing library item). Ignored if missing.",
    )
    parser.add_argument(
        "--no-featured-media",
        action="store_true",
        help="Do not set featured_media even if a map file exists",
    )
    parser.add_argument(
        "--sync-featured-media",
        action="store_true",
        help="Only PATCH featured_media on existing posts (from index URL/slug); never create a new post.",
    )
    parser.add_argument(
        "--refresh-body",
        action="store_true",
        help="PATCH post content HTML from markdown for existing post in index (fixes stale body); pair with --sync-featured-media if needed",
    )
    parser.add_argument(
        "--refresh-title",
        action="store_true",
        help="With --refresh-body: also PATCH the post title from the 'Titre :' header",
    )
    parser.add_argument(
        "--no-rank-math-meta",
        action="store_true",
        help="Do not call Rank Math rankmath/v1/updateMeta even if the # SEO block has values",
    )
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
            "push_rank_math_meta": True,
        }

    missing = [key for key in ("site_url", "username", "application_password") if not raw.get(key)]
    if missing:
        raise ValueError(f"Missing WordPress config value(s): {', '.join(missing)}")

    return Config(
        site_url=str(raw["site_url"]).rstrip("/"),
        username=str(raw["username"]),
        application_password=str(raw["application_password"]),
        verify_ssl=bool(raw.get("verify_ssl", True)),
        push_rank_math_meta=bool(raw.get("push_rank_math_meta", True)),
    )


def _get_env(name: str) -> str:
    import os

    return os.environ.get(name, "")


def _normalize_meta_key_label(key: str) -> str:
    """Fold accents so 'Mot-clé principal' matches editorial YAML 'Mot-cle principal'."""
    k = key.strip().lower()
    for ch in ("é", "è", "ê", "ë"):
        k = k.replace(ch, "e")
    return k


def strip_leading_seo_residual_markdown(body: str) -> str:
    """Drop leftover # SEO blocks or Mot-clé principal...--- if extraction ever missed them."""
    lines = body.splitlines()
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i >= len(lines):
        return body

    stripped_heading = lines[i].strip()
    if stripped_heading.casefold() in {"# seo", "#seo"}:
        j = i + 1
        while j < len(lines):
            if lines[j].strip() == "---":
                j += 1
                break
            j += 1
        lines = lines[j:]
        while lines and not lines[0].strip():
            lines.pop(0)
        return strip_leading_seo_residual_markdown("\n".join(lines))

    first = lines[i].strip()
    if re.match(r"^Mot-?cl[eé]\s+principal\s*:", first, re.IGNORECASE):
        j = i
        while j < len(lines):
            if lines[j].strip() == "---":
                j += 1
                break
            j += 1
        lines = lines[j:]
        while lines and not lines[0].strip():
            lines.pop(0)
        return strip_leading_seo_residual_markdown("\n".join(lines))
    return body


def strip_seo_leak_html(html: str) -> str:
    """Remove leading SEO leak paragraphs sometimes stored in WP from older pushes."""
    if not html:
        return html
    out = html
    out = re.sub(r"^\s*<h1>\s*SEO\s*</h1>\s*", "", out, flags=re.IGNORECASE)
    leak = re.compile(
        r"^\s*<p>[\s\S]*?Mot-?cl[eé]\s+principal\s*:[\s\S]*?Meta-description\s*:[\s\S]*?</p>\s*",
        re.IGNORECASE,
    )
    while True:
        new_out = leak.sub("", out, count=1)
        if new_out == out:
            break
        out = new_out
    return out.lstrip()


def _slug_from_filename(stem: str) -> str:
    """Derive a WordPress slug from filename stem when 'Slug propose' is absent.

    Pattern: {ID}_{TYPE}_{THEME}_{slug_words}_{VERSION}
    Example: 2026-481_ACTU_SCIENCE_canicule_mai_2026_V1 → canicule-mai-2026
    """
    s = re.sub(r"_V\d+$", "", stem)
    parts = s.split("_")
    skip = 0
    if parts and re.match(r"^\d{4}-\d+$", parts[0]):
        skip = 1
    if len(parts) > skip and parts[skip].upper() in ("ACTU", "TF", "SENTIER", "FOND", "DOSSIER", "SYNTHESE"):
        skip += 1
    if len(parts) > skip and parts[skip].upper() in (
        "ECON", "POL", "TECH", "CLIMAT", "SCIENCE", "CULTURE", "MONDE",
        "WORLD", "SCIENCE_SANTE", "SANTE",
    ):
        skip += 1
    return "-".join(p.lower() for p in parts[skip:] if p)


def parse_article(path: Path) -> Article:
    text = path.read_text(encoding="utf-8")
    metadata, remainder = split_frontmatter(text)
    # Defensive: use `or ""` so None values (malformed frontmatter) never crash .strip()
    title = (metadata.get("Titre") or "").strip()
    article_id = (metadata.get("ID article") or "").strip()
    excerpt = (metadata.get("Resume court (500 caracteres max)") or "").strip()
    if not title:
        raise ValueError(f"Missing required metadata: Titre (fichier: {path.name})")

    seo_keyword, seo_description, seo_title, body = extract_seo_and_body(remainder)
    slug = extract_slug(body)

    if not slug:
        slug = _slug_from_filename(path.stem)
        if not slug:
            raise ValueError(f"Missing required field: Slug propose (fichier: {path.name})")

    clean_body = strip_internal_sections(body)
    clean_body = strip_leading_seo_residual_markdown(clean_body)
    html = markdown_like_to_html(clean_body)
    html = strip_seo_leak_html(html)
    if not html.strip():
        raise ValueError("Article body is empty after cleanup")

    return Article(
        path=path,
        title=title,
        slug=slug,
        excerpt=excerpt,
        seo_keyword=seo_keyword,
        seo_description=seo_description,
        seo_title=seo_title,
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


def extract_seo_and_body(remainder: str) -> tuple[str, str, str, str]:
    """SEO block either leading (triptyque: `# SEO` … `---` then body) or trailing (v3: body then `# SEO`)."""
    lines = remainder.splitlines()
    seo = {"mot cle principal": "", "meta description": "", "titre seo": ""}

    def read_meta(line: str) -> None:
        match = META_LINE_RE.match(line.strip())
        if match:
            nk = _normalize_meta_key_label(match.group("key")).replace("-", " ")
            if nk in seo:
                seo[nk] = match.group("value").strip()

    lead = 0
    while lead < len(lines) and not lines[lead].strip():
        lead += 1

    if lead < len(lines) and lines[lead].strip().casefold() in {"# seo", "#seo"}:
        body_start = len(lines)
        for idx, line in enumerate(lines[lead + 1 :], start=lead + 1):
            if line.strip() == "---":
                body_start = idx + 1
                break
            read_meta(line)
        body = "\n".join(lines[body_start:]).lstrip()
    else:
        seo_idx = next(
            (i for i in range(len(lines) - 1, lead, -1) if lines[i].strip().casefold() in {"# seo", "#seo"}),
            None,
        )
        if seo_idx is None:
            body = "\n".join(lines[lead:])
        else:
            tail = lines[seo_idx + 1 :]
            for line in tail:
                read_meta(line)
            head = lines[:seo_idx]
            while head and head[-1].strip() in {"", "---"}:
                head.pop()
            # Slug propose stays in body for extract_slug; strip_internal_sections drops it from HTML.
            head += [line.strip() for line in tail if line.strip().startswith("Slug propose")]
            body = "\n".join(head).lstrip()
    return seo["mot cle principal"], seo["meta description"], seo["titre seo"], body


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
    """Inline: [label](url) links, **bold** → <strong> (non-greedy pairs). Plain text HTML-escaped."""

    def segment_to_html(segment: str) -> str:
        out: list[str] = []
        pos = 0
        for m in re.finditer(r"\*\*(.+?)\*\*", segment):
            if m.start() > pos:
                out.append(escape(segment[pos : m.start()]))
            out.append(f"<strong>{escape(m.group(1))}</strong>")
            pos = m.end()
        if pos < len(segment):
            out.append(escape(segment[pos:]))
        return "".join(out)

    parts: list[str] = []
    cursor = 0
    for match in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", text):
        start, end = match.span()
        if start > cursor:
            parts.append(segment_to_html(text[cursor:start]))
        label = match.group(1).strip()
        url = match.group(2).strip()
        parts.append(f'<a href="{escape(url, quote=True)}">{segment_to_html(label)}</a>')
        cursor = end
    if cursor < len(text):
        parts.append(segment_to_html(text[cursor:]))
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
            html_parts.append(f"<h1>{render_inline_markdown(line[2:].strip())}</h1>")
            continue

        if line.startswith("## "):
            flush_paragraph()
            flush_list()
            html_parts.append(f"<h2>{render_inline_markdown(line[3:].strip())}</h2>")
            continue

        if line.startswith("### "):
            flush_paragraph()
            flush_list()
            html_parts.append(f"<h3>{render_inline_markdown(line[4:].strip())}</h3>")
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


def rank_math_meta_payload(article: Article, *, enabled: bool) -> dict[str, str] | None:
    """Key/value map for Rank Math POST rankmath/v1/updateMeta (meta sub-object)."""
    if not enabled:
        return None
    meta: dict[str, str] = {}
    kw = (article.seo_keyword or "").strip()
    desc = (article.seo_description or "").strip()
    st = (article.seo_title or "").strip()
    if st:
        meta["rank_math_title"] = st
    if kw:
        meta["rank_math_focus_keyword"] = kw
    if desc:
        meta["rank_math_description"] = desc
    return meta or None


def rank_math_apply_rest_meta(config: Config, post_id: int, meta: dict[str, str]) -> dict:
    """Rank Math's own REST API (no core post meta / no mu-plugin)."""
    endpoint = f"{config.site_url}/wp-json/rankmath/v1/updateMeta"
    payload = {
        "objectType": "post",
        "objectID": post_id,
        "meta": meta,
    }
    try:
        return wordpress_request_json(config, endpoint, method="POST", payload=payload)
    except RuntimeError as exc:
        msg = str(exc)
        hint = (
            " Rank Math: activer l'extension, puis Rank Math > Reglages generaux > "
            "Autres > Headless CMS Support si besoin; debloquer /wp-json/rankmath/v1/updateMeta (firewall / ModSecurity)."
        )
        raise RuntimeError(msg + hint) from exc


def _build_post_payload(
    article: Article,
    *,
    category_ids: list[int] | None = None,
    tag_ids: list[int] | None = None,
    featured_media_id: int | None = None,
    include_slug: bool = True,
    status: str = "draft",
) -> dict:
    payload: dict[str, object] = {
        "title": article.title,
        "content": article.body_html,
        "status": status,
    }
    if include_slug and article.slug:
        payload["slug"] = article.slug
    if article.excerpt:
        payload["excerpt"] = article.excerpt
    if category_ids:
        payload["categories"] = category_ids
    if tag_ids:
        payload["tags"] = tag_ids
    if featured_media_id is not None:
        payload["featured_media"] = featured_media_id
    return payload


def create_wordpress_draft(
    article: Article,
    config: Config,
    category_ids: list[int] | None = None,
    tag_ids: list[int] | None = None,
    featured_media_id: int | None = None,
) -> dict:
    endpoint = f"{config.site_url}/wp-json/wp/v2/posts"
    payload = _build_post_payload(
        article,
        category_ids=category_ids,
        tag_ids=tag_ids,
        featured_media_id=featured_media_id,
        include_slug=True,
        status="draft",
    )
    return wordpress_request_json(config, endpoint, method="POST", payload=payload)


def update_wordpress_post(
    config: Config,
    post_id: int,
    article: Article,
    category_ids: list[int] | None = None,
    tag_ids: list[int] | None = None,
    featured_media_id: int | None = None,
) -> dict:
    """Update an existing post instead of creating a duplicate (slug left unchanged on WP)."""
    endpoint = f"{config.site_url}/wp-json/wp/v2/posts/{post_id}"
    payload = _build_post_payload(
        article,
        category_ids=category_ids,
        tag_ids=tag_ids,
        featured_media_id=featured_media_id,
        include_slug=False,
    )
    return wordpress_request_json(config, endpoint, method="POST", payload=payload)


def find_wp_post_id_by_slug(config: Config, slug: str, *, loose_suffix: bool = False) -> int | None:
    slug = safe_str(slug)
    if not slug:
        return None
    statuses = "draft,publish,pending,private,future"
    endpoint = (
        f"{config.site_url}/wp-json/wp/v2/posts"
        f"?slug={parse.quote(slug)}&status={statuses}&per_page=10"
    )
    items = wordpress_request_json(config, endpoint, method="GET")
    if isinstance(items, list) and items:
        slug_cf = slug.casefold()
        for item in items:
            if safe_str(item.get("slug")).casefold() == slug_cf:
                post_id = item.get("id")
                if isinstance(post_id, int):
                    return post_id
        post_id = items[0].get("id")
        if isinstance(post_id, int):
            return post_id

    if not loose_suffix or re.search(r"-\d+$", slug):
        return None
    # WordPress may have appended -2, -4, etc. when the base slug was already taken.
    for suffix in range(2, 10):
        candidate = f"{slug}-{suffix}"
        endpoint = (
            f"{config.site_url}/wp-json/wp/v2/posts"
            f"?slug={parse.quote(candidate)}&status={statuses}&per_page=1"
        )
        items = wordpress_request_json(config, endpoint, method="GET")
        if isinstance(items, list) and items:
            post_id = items[0].get("id")
            if isinstance(post_id, int):
                return post_id
    return None


def resolve_existing_post_id(
    config: Config,
    article: Article,
    index_record: IndexRecord | None,
) -> int | None:
    """Find a WordPress post already created for this article (avoids -2 / -4 slug duplicates on retry)."""
    if index_record:
        post_id = resolve_wp_post_id(config, index_record)
        if post_id is not None:
            return post_id
        url_field = safe_str(index_record.wordpress_url)
        if url_field and not url_field.startswith(("http://", "https://")):
            post_id = find_wp_post_id_by_slug(config, url_field, loose_suffix=True)
            if post_id is not None:
                return post_id
        if index_record.wordpress_slug:
            post_id = find_wp_post_id_by_slug(config, index_record.wordpress_slug, loose_suffix=True)
            if post_id is not None:
                return post_id
    if article.slug:
        return find_wp_post_id_by_slug(config, article.slug, loose_suffix=True)
    return None


def load_index_record(index_path: Path, article_id: str) -> IndexRecord:
    if not article_id:
        raise ValueError("Cannot read index without article ID")
    if not index_path.exists():
        raise FileNotFoundError(f"Index file not found: {index_path}")

    with index_path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            if safe_str(row.get("ID")) == article_id:
                return IndexRecord(
                    article_id=article_id,
                    status=safe_str(row.get("Statut")),
                    wordpress_url=safe_str(row.get("URL_WordPress")),
                    wordpress_slug=safe_str(row.get("Slug_WordPress")),
                    categories=split_multi_value_field(row.get("Categorie_WP")),
                    tags=with_visibility_tag(split_multi_value_field(row.get("Tags_WP"))),
                )

    raise ValueError(f"Article ID not found in index: {article_id}")


def with_visibility_tag(tags: list[str]) -> list[str]:
    # Un update WP remplace la liste de tags : sans « a-la-une », le thème masque l'article.
    return tags if VISIBILITY_TAG in tags else [*tags, VISIBILITY_TAG]


def split_multi_value_field(raw_value: str | None) -> list[str]:
    return [part.strip() for part in safe_str(raw_value).split(";") if part.strip()]


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


def load_featured_media_map(map_path: Path) -> dict | None:
    if not map_path.is_file():
        return None
    try:
        raw = json.loads(map_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return raw if isinstance(raw, dict) else None


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


def resolve_wp_post_id(config: Config, record: IndexRecord | None) -> int | None:
    """Resolve REST post id from index URL (?p=) or slug field / permalink path."""
    if not record:
        return None
    url_field = safe_str(record.wordpress_url)
    if url_field and not url_field.startswith(("http://", "https://")):
        return find_wp_post_id_by_slug(config, url_field)
    parsed = parse.urlparse(url_field)
    query_ids = parse.parse_qs(parsed.query).get("p", [])
    if query_ids and str(query_ids[0]).isdigit():
        return int(query_ids[0])

    slug = safe_str(record.wordpress_slug)
    if not slug:
        tail = parsed.path.rstrip("/").split("/")[-1].strip()
        slug = tail if tail else ""

    return find_wp_post_id_by_slug(config, slug)


def patch_post_partial(
    config: Config,
    post_id: int,
    *,
    featured_media_id: int | None = None,
) -> dict:
    endpoint = f"{config.site_url}/wp-json/wp/v2/posts/{post_id}"
    payload: dict[str, object] = {}
    if featured_media_id is not None:
        payload["featured_media"] = featured_media_id
    if not payload:
        raise ValueError("patch_post_partial: featured_media_id is required")
    return wordpress_request_json(config, endpoint, method="POST", payload=payload)


def patch_post_content(config: Config, post_id: int, html_content: str, title: str | None = None) -> dict:
    endpoint = f"{config.site_url}/wp-json/wp/v2/posts/{post_id}"
    payload: dict[str, object] = {"content": html_content}
    if title:
        payload["title"] = title
    return wordpress_request_json(config, endpoint, method="POST", payload=payload)


def _coerce_positive_media_id(val: object) -> int | None:
    if isinstance(val, bool):
        return None
    if isinstance(val, int):
        return val if val > 0 else None
    if isinstance(val, str):
        s = val.strip()
        if not s:
            return None
        if s.isdigit():
            n = int(s)
            return n if n > 0 else None
    return None


def featured_map_needs_wp_lookup(feature_map: dict | None) -> bool:
    if not feature_map:
        return False
    for key in ("by_category_slug", "by_tag_slug"):
        sub = feature_map.get(key)
        if isinstance(sub, dict):
            for v in sub.values():
                if isinstance(v, str) and v.strip() and _coerce_positive_media_id(v) is None:
                    return True
    v = feature_map.get("default_media_id")
    return isinstance(v, str) and bool(v.strip()) and _coerce_positive_media_id(v) is None


def search_media_id_by_filename(config: Config, ref: str, cache: dict[str, int]) -> int | None:
    key = ref.strip().lower()
    if not key:
        return None
    if key in cache:
        return cache[key]

    basename = key.split("/")[-1]
    stem = basename.rsplit(".", 1)[0] if "." in basename else basename
    want = basename.casefold()

    def pick_from_items(items: object) -> int | None:
        if not isinstance(items, list):
            return None
        for item in items:
            url = str(item.get("source_url") or "")
            tail = parse.urlparse(url).path.rstrip("/").split("/")[-1].casefold()
            if tail == want:
                mid = item.get("id")
                if isinstance(mid, int) and mid > 0:
                    cache[key] = mid
                    return mid
        return None

    base = config.site_url.rstrip("/")
    for term in (basename, stem):
        if not term:
            continue
        endpoint = f"{base}/wp-json/wp/v2/media?per_page=50&search={parse.quote(term)}"
        found = pick_from_items(wordpress_request_json(config, endpoint, method="GET"))
        if found is not None:
            return found

    slug_try = slugify_term(stem) if stem else ""
    if slug_try:
        endpoint = f"{base}/wp-json/wp/v2/media?slug={parse.quote(slug_try)}"
        items = wordpress_request_json(config, endpoint, method="GET")
        if isinstance(items, list) and items:
            mid = items[0].get("id")
            if isinstance(mid, int) and mid > 0:
                cache[key] = mid
                return mid

    return None


def resolve_map_entry(config: Config | None, raw: object, cache: dict[str, int]) -> int | None:
    pid = _coerce_positive_media_id(raw)
    if pid is not None:
        return pid
    if isinstance(raw, str):
        s = raw.strip()
        if s and config is not None:
            return search_media_id_by_filename(config, s, cache)
    return None


def resolve_featured_media_id(
    feature_map: dict | None,
    categories: list[str],
    tags: list[str],
    config: Config | None,
    cache: dict[str, int],
) -> int | None:
    if not feature_map:
        return None
    by_cat = feature_map.get("by_category_slug") or {}
    by_tag = feature_map.get("by_tag_slug") or {}
    if not isinstance(by_cat, dict):
        by_cat = {}
    if not isinstance(by_tag, dict):
        by_tag = {}

    for label in categories:
        slug = slugify_term(label)
        mid = resolve_map_entry(config, by_cat.get(slug), cache)
        if mid is not None:
            return mid
    for label in tags:
        slug = slugify_term(label)
        mid = resolve_map_entry(config, by_tag.get(slug), cache)
        if mid is not None:
            return mid
    return resolve_map_entry(config, feature_map.get("default_media_id"), cache)


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
    fieldnames, rows = read_index(index_path)

    updated = False
    for row in rows:
        if safe_str(row.get("ID")) == article.article_id:
            row["Statut"] = "wp_draft"
            row["URL_WordPress"] = safe_str(wp_result.get("link"))
            row["Slug_WordPress"] = safe_str(wp_result.get("slug")) or safe_str(article.slug)
            row["Date_derniere_maj"] = _today_iso()
            existing = safe_str(row.get("Remarques"))
            note = "Brouillon WordPress créé via script"
            row["Remarques"] = note if not existing else f"{existing} | {note}"
            updated = True
            break

    if not updated:
        raise ValueError(f"Article ID not found in index: {article.article_id}")

    write_index(index_path, fieldnames, rows)
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


def should_skip_publish(
    index_record: IndexRecord | None,
    force: bool,
    existing_post_id: int | None,
) -> bool:
    """Skip only when index already points to a live WP URL and the post still exists."""
    if force or not index_record or existing_post_id is None:
        return False
    url = safe_str(index_record.wordpress_url)
    if not url.startswith(("http://", "https://")):
        return False
    if index_record.status not in ("wp_draft", "publie"):
        return False
    return True


def build_dry_run_payload(article: Article, index_record: IndexRecord | None, multi_file: bool) -> dict:
    payload = {
        "path": str(article.path),
        "article_id": article.article_id,
        "title": article.title,
        "slug": article.slug,
        "excerpt": article.excerpt,
        "seo_keyword": article.seo_keyword,
        "seo_description": article.seo_description,
        "seo_title": article.seo_title,
        "categories": index_record.categories if index_record else [],
        "tags": index_record.tags if index_record else [],
    }
    if not multi_file:
        payload["html_preview"] = article.body_html[:1500]
    return payload


def process_article(
    path: Path,
    args: argparse.Namespace,
    config: Config | None,
    multi_file: bool,
    featured_map: dict | None,
    media_cache: dict[str, int],
) -> ArticleRunResult | dict:
    article = parse_article(path)
    index_record = load_index_record(Path(args.index), article.article_id) if args.index else None

    cats = index_record.categories if index_record else []
    tags = index_record.tags if index_record else []
    fm_id = resolve_featured_media_id(featured_map, cats, tags, config, media_cache)
    rm_enabled = (config.push_rank_math_meta if config else True) and not args.no_rank_math_meta
    rm_payload = rank_math_meta_payload(article, enabled=rm_enabled)

    if args.dry_run:
        preview = build_dry_run_payload(article, index_record, multi_file)
        if fm_id is not None:
            preview["featured_media"] = fm_id
        if rm_payload:
            preview["rank_math_meta"] = rm_payload
        if getattr(args, "refresh_body", False):
            preview["refresh_body"] = True
        if getattr(args, "sync_featured_media", False):
            preview["sync_featured_media"] = True
        if (
            (getattr(args, "sync_featured_media", False) or getattr(args, "refresh_body", False))
            and config is not None
            and index_record
        ):
            preview["wordpress_post_id_resolve"] = resolve_wp_post_id(config, index_record)
        elif getattr(args, "sync_featured_media", False) or getattr(args, "refresh_body", False):
            preview["wordpress_post_id_resolve"] = None
        return preview

    if config is None:
        raise ValueError("Config is required for publishing")

    sync_fm = getattr(args, "sync_featured_media", False)
    refresh_body = getattr(args, "refresh_body", False)
    if sync_fm or refresh_body:
        if not args.index:
            return ArticleRunResult(
                path=str(article.path),
                article_id=article.article_id,
                title=article.title,
                status="error",
                skipped=False,
                error="--refresh-body / --sync-featured-media require --index.",
                categories=cats,
                tags=tags,
            )
        if index_record is None:
            return ArticleRunResult(
                path=str(article.path),
                article_id=article.article_id,
                title=article.title,
                status="error",
                skipped=False,
                error=f"Article ID not found in index: {article.article_id}",
                categories=cats,
                tags=tags,
            )
        post_id = resolve_wp_post_id(config, index_record)
        if post_id is None:
            return ArticleRunResult(
                path=str(article.path),
                article_id=article.article_id,
                title=article.title,
                status="error",
                skipped=False,
                error="Cannot resolve WordPress post id from index (URL ?p= or slug).",
                categories=cats,
                tags=tags,
            )
        if sync_fm and fm_id is None:
            return ArticleRunResult(
                path=str(article.path),
                article_id=article.article_id,
                title=article.title,
                status="error",
                skipped=False,
                error="--sync-featured-media requires a resolved featured_media id (check wp_featured_media map and tags).",
                categories=cats,
                tags=tags,
            )
        wp_result: dict = {}
        if refresh_body:
            title = article.title if getattr(args, "refresh_title", False) else None
            wp_result = patch_post_content(config, post_id, article.body_html, title=title)
        if sync_fm:
            wp_result = patch_post_partial(config, post_id, featured_media_id=fm_id)
        if rm_payload:
            rank_math_apply_rest_meta(config, post_id, rm_payload)
        link = str(wp_result.get("link", "") or "")
        return ArticleRunResult(
            path=str(article.path),
            article_id=article.article_id,
            title=article.title,
            status=str(wp_result.get("status", "")),
            skipped=False,
            wordpress_id=post_id,
            wordpress_slug=str(wp_result.get("slug", "") or ""),
            wordpress_link=link,
            categories=cats,
            tags=tags,
            featured_media_id=fm_id,
        )

    existing_post_id = resolve_existing_post_id(config, article, index_record)

    if should_skip_publish(index_record, args.force, existing_post_id):
        return ArticleRunResult(
            path=str(article.path),
            article_id=article.article_id,
            title=article.title,
            status="skipped",
            skipped=True,
            wordpress_id=existing_post_id,
            wordpress_slug=index_record.wordpress_slug if index_record else "",
            wordpress_link=index_record.wordpress_url if index_record else "",
            categories=cats,
            tags=tags,
            featured_media_id=fm_id,
        )

    category_ids = resolve_taxonomy_ids(config, "categories", index_record.categories) if index_record else []
    tag_ids = resolve_taxonomy_ids(config, "tags", index_record.tags) if index_record else []

    reused_existing = existing_post_id is not None
    if reused_existing:
        result = update_wordpress_post(
            config,
            existing_post_id,
            article,
            category_ids=category_ids,
            tag_ids=tag_ids,
            featured_media_id=fm_id,
        )
    else:
        result = create_wordpress_draft(
            article,
            config,
            category_ids=category_ids,
            tag_ids=tag_ids,
            featured_media_id=fm_id,
        )

    wordpress_id = result.get("id")
    if not isinstance(wordpress_id, int) and reused_existing:
        wordpress_id = existing_post_id
    if rm_payload and isinstance(wordpress_id, int):
        rank_math_apply_rest_meta(config, wordpress_id, rm_payload)

    index_updated = False
    index_error = ""
    if args.index:
        try:
            index_updated = update_index(Path(args.index), article, result)
        except Exception as exc:
            index_error = str(exc)

    return ArticleRunResult(
        path=str(article.path),
        article_id=article.article_id,
        title=article.title,
        status=str(result.get("status", "")),
        skipped=False,
        wordpress_id=wordpress_id if isinstance(wordpress_id, int) else None,
        wordpress_slug=str(result.get("slug", "") or article.slug),
        wordpress_link=str(result.get("link", "") or ""),
        categories=cats,
        tags=tags,
        index_updated=index_updated,
        featured_media_id=fm_id,
        error=index_error,
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
                "featured_media": item.featured_media_id,
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
    featured_map: dict | None = None
    if not args.no_featured_media:
        featured_map = load_featured_media_map(Path(args.featured_media_map))

    media_cache: dict[str, int] = {}

    try:
        if args.dry_run:
            config = None
            dry_need_lookup = featured_map and not args.no_featured_media and featured_map_needs_wp_lookup(featured_map)
            dry_need_resolve = getattr(args, "sync_featured_media", False) or getattr(args, "refresh_body", False)
            if dry_need_lookup or dry_need_resolve:
                config = load_config(args.config)
        else:
            config = load_config(args.config)
    except Exception as exc:
        print(f"Publish error: {exc}", file=sys.stderr)
        return 1

    if not multi_file:
        try:
            result = process_article(
                source_files[0],
                args,
                config,
                multi_file=False,
                featured_map=featured_map,
                media_cache=media_cache,
            )
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
                previews.append(
                    process_article(path, args, config, multi_file=True, featured_map=featured_map, media_cache=media_cache),
                )
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
            article_result = process_article(path, args, config, multi_file=True, featured_map=featured_map, media_cache=media_cache)
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
