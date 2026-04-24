#!/usr/bin/env python3
"""
Add real internal links to published Le Phare triptychs.

Supported scopes:
- one triptych directory inside 07_A_Publier
- one architecture directory containing multiple triptych subdirectories

Current scope:
- verify each triptych contains exactly ACTU, TF, SENTIER
- load WordPress URLs from index_editorial.csv
- replace placeholder internal links with a real "Dans ce triptyque" block
- optionally add a "Dans cette architecture editoriale" block for multi-triptych dossiers
- update both the publish copy and the original local source file
- update WordPress drafts through the REST API
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from urllib import parse

from wp_push_draft import (
    Config,
    load_config,
    parse_article,
    split_frontmatter,
    wordpress_request_json,
)


ROOT_DIR = Path(__file__).resolve().parent.parent
REQUIRED_TYPES = ("ACTU", "TF", "SENTIER")
SECTION_HEADING = "## Dans ce triptyque"
ARCHITECTURE_SECTION_HEADING = "## Dans cette architecture editoriale"
LEGACY_SECTION_HEADING = "## Liens internes du dossier"
INDEX_NOTE = "Maillage interne triptyque ajoute automatiquement"
ARCHITECTURE_INDEX_NOTE = "Maillage inter-triptyques ajoute automatiquement"


@dataclass
class IndexRecord:
    article_id: str
    title: str
    type_code: str
    theme_code: str
    status: str
    wordpress_url: str
    wordpress_slug: str
    filename: str
    relative_folder: str
    excerpt: str
    remarks: str


@dataclass
class TriptychArticle:
    publish_path: Path
    source_path: Path | None
    article_id: str
    triptych_id: str
    triptych_label: str
    triptych_order: int
    title: str
    type_code: str
    theme_code: str
    excerpt: str
    wordpress_url: str
    wordpress_slug: str
    wordpress_id: int


@dataclass
class LinkingResult:
    article_id: str
    type_code: str
    title: str
    wordpress_id: int
    wordpress_url: str
    updated_paths: list[str]
    status: str
    error: str = ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Add internal links to a Le Phare triptych and update WordPress drafts.")
    parser.add_argument("triptych_dir", help="Path to the generated triptych directory inside 07_A_Publier")
    parser.add_argument("--index", required=True, help="Path to index_editorial.csv")
    parser.add_argument("--config", required=True, help="Path to local WordPress config JSON")
    parser.add_argument("--dry-run", action="store_true", help="Preview the triptych links without modifying files or WordPress")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        triptych_dir = Path(args.triptych_dir)
        grouped_articles = collect_triptych_groups(triptych_dir, Path(args.index))
    except Exception as exc:
        print(f"Triptych linking error: {exc}", file=sys.stderr)
        return 1

    if args.dry_run:
        payload = build_dry_run_payload(triptych_dir, grouped_articles)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    try:
        config = load_config(args.config)
        results: list[LinkingResult] = []
        all_articles = [article for articles in grouped_articles.values() for article in articles]
        for triptych_id, articles in grouped_articles.items():
            architecture_siblings = [candidate for candidate in all_articles if candidate.triptych_id != triptych_id]
            for article in articles:
                sibling_articles = [candidate for candidate in articles if candidate.article_id != article.article_id]
                triptych_block = build_triptych_links_block(article, sibling_articles)
                architecture_block = build_architecture_links_block(architecture_siblings)
                updated_paths = update_article_files(article, triptych_block, architecture_block)
                parsed_article = parse_article(article.publish_path)
                update_wordpress_post(config, article, parsed_article.body_html, parsed_article.excerpt)
                results.append(
                    LinkingResult(
                        article_id=article.article_id,
                        type_code=article.type_code,
                        title=article.title,
                        wordpress_id=article.wordpress_id,
                        wordpress_url=article.wordpress_url,
                        updated_paths=updated_paths,
                        status="updated",
                    )
                )
        update_index_notes(Path(args.index), [article.article_id for article in all_articles], len(grouped_articles) > 1)
    except Exception as exc:
        print(f"Triptych linking error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(render_summary(triptych_dir, results, dry_run=False), ensure_ascii=False, indent=2))
    return 0


def collect_triptych_groups(root_dir: Path, index_path: Path) -> dict[str, list[TriptychArticle]]:
    if not root_dir.exists():
        raise FileNotFoundError(f"Triptych directory not found: {root_dir}")
    if not root_dir.is_dir():
        raise ValueError(f"Triptych path is not a directory: {root_dir}")

    direct_files = sorted(path for path in root_dir.glob("*.md") if path.is_file())
    if direct_files:
        articles = collect_triptych_articles(root_dir, index_path)
        triptych_id = articles[0].triptych_id if articles else "triptyque_1"
        return {triptych_id: articles}

    groups: dict[str, list[TriptychArticle]] = {}
    for child in sorted(path for path in root_dir.iterdir() if path.is_dir()):
        article_files = sorted(path for path in child.glob("*.md") if path.is_file())
        if not article_files:
            continue
        articles = collect_triptych_articles(child, index_path)
        triptych_id = articles[0].triptych_id if articles else child.name
        groups[triptych_id] = articles

    if not groups:
        raise ValueError(f"No triptych markdown files found in directory: {root_dir}")
    return groups


def collect_triptych_articles(triptych_dir: Path, index_path: Path) -> list[TriptychArticle]:
    if not triptych_dir.exists():
        raise FileNotFoundError(f"Triptych directory not found: {triptych_dir}")
    if not triptych_dir.is_dir():
        raise ValueError(f"Triptych path is not a directory: {triptych_dir}")

    source_files = sorted(path for path in triptych_dir.glob("*.md") if path.is_file())
    if len(source_files) != 3:
        raise ValueError(f"Expected exactly 3 markdown files in triptych directory, found {len(source_files)}")

    index_records = load_index_records(index_path)
    articles: list[TriptychArticle] = []
    seen_types: set[str] = set()
    for path in source_files:
        metadata, _ = split_frontmatter(path.read_text(encoding="utf-8"))
        article_id = metadata.get("ID article", "").strip()
        triptych_id = metadata.get("Triptyque ID", "").strip() or triptych_dir.name
        triptych_label = metadata.get("Triptyque titre", "").strip() or triptych_dir.name
        raw_triptych_order = metadata.get("Triptyque ordre", "").strip()
        title = metadata.get("Titre", "").strip()
        type_code = metadata.get("Type", "").strip().upper()
        theme_code = metadata.get("Theme", "").strip().upper()
        excerpt = metadata.get("Resume court (500 caracteres max)", "").strip()

        if not article_id or not title or not type_code:
            raise ValueError(f"Missing mandatory metadata in file: {path}")
        if type_code not in REQUIRED_TYPES:
            raise ValueError(f"Unexpected article type '{type_code}' in triptych: {path}")
        if type_code in seen_types:
            raise ValueError(f"Duplicate article type '{type_code}' in triptych directory")
        seen_types.add(type_code)

        index_record = index_records.get(article_id)
        if index_record is None:
            raise ValueError(f"Article ID not found in index: {article_id}")
        if not index_record.wordpress_url:
            raise ValueError(f"Missing WordPress URL in index for article {article_id}")

        wordpress_id = extract_wordpress_post_id(index_record.wordpress_url, index_record.wordpress_slug)
        source_path = resolve_source_path(index_record)
        articles.append(
            TriptychArticle(
                publish_path=path,
                source_path=source_path,
                article_id=article_id,
                triptych_id=triptych_id,
                triptych_label=triptych_label,
                triptych_order=int(raw_triptych_order) if raw_triptych_order.isdigit() else 1,
                title=title,
                type_code=type_code,
                theme_code=theme_code,
                excerpt=excerpt,
                wordpress_url=index_record.wordpress_url,
                wordpress_slug=index_record.wordpress_slug,
                wordpress_id=wordpress_id,
            )
        )

    missing_types = [type_code for type_code in REQUIRED_TYPES if type_code not in seen_types]
    if missing_types:
        raise ValueError(f"Triptych directory is missing required article type(s): {', '.join(missing_types)}")

    articles.sort(key=lambda article: REQUIRED_TYPES.index(article.type_code))
    return articles


def load_index_records(index_path: Path) -> dict[str, IndexRecord]:
    if not index_path.exists():
        raise FileNotFoundError(f"Index file not found: {index_path}")

    records: dict[str, IndexRecord] = {}
    with index_path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            article_id = row.get("ID", "").strip()
            if not article_id:
                continue
            records[article_id] = IndexRecord(
                article_id=article_id,
                title=row.get("Titre", "").strip(),
                type_code=row.get("Type", "").strip().upper(),
                theme_code=row.get("Theme", "").strip().upper(),
                status=row.get("Statut", "").strip(),
                wordpress_url=row.get("URL_WordPress", "").strip(),
                wordpress_slug=row.get("Slug_WordPress", "").strip(),
                filename=row.get("Nom_fichier", "").strip(),
                relative_folder=row.get("Chemin_dossier", "").strip(),
                excerpt=row.get("Resume_court", "").strip(),
                remarks=row.get("Remarques", "").strip(),
            )
    return records


def resolve_source_path(record: IndexRecord) -> Path | None:
    if not record.filename or not record.relative_folder:
        return None
    path = ROOT_DIR / record.relative_folder / record.filename
    return path if path.exists() else None


def extract_wordpress_post_id(wordpress_url: str, wordpress_slug: str) -> int:
    parsed = parse.urlparse(wordpress_url)
    query = parse.parse_qs(parsed.query)
    raw_id = query.get("p", [""])[0]
    if raw_id.isdigit():
        return int(raw_id)
    if wordpress_slug:
        raise ValueError(f"Unable to extract WordPress post ID from URL '{wordpress_url}' for slug '{wordpress_slug}'")
    raise ValueError(f"Unable to extract WordPress post ID from URL '{wordpress_url}'")


def build_triptych_links_block(article: TriptychArticle, siblings: list[TriptychArticle]) -> str:
    intro_by_type = {
        "ACTU": "Pour replacer cette actualité dans un cadre plus durable :",
        "TF": "Pour voir comment cette grille de lecture éclaire le sujet du jour :",
        "SENTIER": "Pour relier cette mise en perspective à ses deux autres dimensions :",
    }
    label_by_type = {
        "ACTU": "Revenir à l'actualité",
        "TF": "Approfondir avec le texte fondateur",
        "SENTIER": "Prolonger avec le Sentier du Savoir",
    }
    ordered_siblings = sorted(siblings, key=lambda candidate: REQUIRED_TYPES.index(candidate.type_code))
    lines = [SECTION_HEADING, "", intro_by_type.get(article.type_code, "Pour prolonger cette lecture :")]
    for sibling in ordered_siblings:
        label = label_by_type.get(sibling.type_code, "Lire aussi")
        lines.append(f"- [{label} : {sibling.title}]({sibling.wordpress_url})")
    return "\n".join(lines).strip()


def build_architecture_links_block(siblings: list[TriptychArticle]) -> str:
    if not siblings:
        return ""

    grouped: dict[str, list[TriptychArticle]] = {}
    for sibling in siblings:
        grouped.setdefault(sibling.triptych_id, []).append(sibling)

    ordered_groups = sorted(
        grouped.items(),
        key=lambda item: min(candidate.triptych_order for candidate in item[1]),
    )
    lines = [
        ARCHITECTURE_SECTION_HEADING,
        "",
        "Pour prolonger ce triptyque dans une architecture editoriale plus large :",
    ]
    for _, group_articles in ordered_groups:
        exemplar = sorted(group_articles, key=lambda candidate: REQUIRED_TYPES.index(candidate.type_code))[0]
        lines.append(f"- [{exemplar.triptych_label}]({exemplar.wordpress_url})")
    return "\n".join(lines).strip()


def update_article_files(article: TriptychArticle, triptych_block: str, architecture_block: str = "") -> list[str]:
    updated_paths: list[str] = []
    candidate_paths = [article.publish_path]
    if article.source_path and article.source_path != article.publish_path:
        candidate_paths.append(article.source_path)

    for path in candidate_paths:
        original = path.read_text(encoding="utf-8")
        updated = replace_or_append_triptych_section(original, triptych_block, architecture_block)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
        updated_paths.append(str(path))
    return updated_paths


def replace_or_append_triptych_section(content: str, block: str, architecture_block: str = "") -> str:
    updated = remove_section(content, SECTION_HEADING)
    updated = remove_section(updated, ARCHITECTURE_SECTION_HEADING)
    updated = remove_section(updated, LEGACY_SECTION_HEADING)

    insertion_markers = ("\n## Bloc image WordPress", "\n## Bloc publication")
    insertion_index = -1
    for marker in insertion_markers:
        marker_index = updated.find(marker)
        if marker_index != -1 and (insertion_index == -1 or marker_index < insertion_index):
            insertion_index = marker_index

    normalized_blocks = [part.strip() for part in (block, architecture_block) if part and part.strip()]
    normalized_block = "\n\n".join(normalized_blocks).strip()
    if insertion_index != -1:
        prefix = updated[:insertion_index].rstrip()
        suffix = updated[insertion_index:].lstrip("\n")
        return f"{prefix}\n\n{normalized_block}\n\n{suffix}".rstrip() + "\n"
    return updated.rstrip() + f"\n\n{normalized_block}\n"


def remove_section(content: str, heading: str) -> str:
    pattern = re.compile(
        rf"(?:\n|^){re.escape(heading)}\n.*?(?=\n## |\Z)",
        flags=re.DOTALL,
    )
    return re.sub(pattern, "\n", content).strip() + "\n"


def update_wordpress_post(config: Config, article: TriptychArticle, html_content: str, excerpt: str) -> dict:
    endpoint = f"{config.site_url}/wp-json/wp/v2/posts/{article.wordpress_id}"
    payload = {
        "content": html_content,
        "status": "draft",
    }
    if excerpt:
        payload["excerpt"] = excerpt
    return wordpress_request_json(config, endpoint, method="POST", payload=payload)


def update_index_notes(index_path: Path, article_ids: list[str], has_architecture_links: bool = False) -> None:
    if not index_path.exists():
        raise FileNotFoundError(f"Index file not found: {index_path}")

    with index_path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        fieldnames = reader.fieldnames or []

    article_id_set = set(article_ids)
    for row in rows:
        article_id = row.get("ID", "").strip()
        if article_id not in article_id_set:
            continue
        row["Date_derniere_maj"] = today_iso()
        existing = row.get("Remarques", "").strip()
        if INDEX_NOTE not in existing:
            row["Remarques"] = INDEX_NOTE if not existing else f"{existing} | {INDEX_NOTE}"
            existing = row["Remarques"]
        if has_architecture_links and ARCHITECTURE_INDEX_NOTE not in existing:
            row["Remarques"] = ARCHITECTURE_INDEX_NOTE if not existing else f"{existing} | {ARCHITECTURE_INDEX_NOTE}"

    with index_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_dry_run_payload(triptych_dir: Path, grouped_articles: dict[str, list[TriptychArticle]]) -> dict:
    items: list[dict[str, object]] = []
    all_articles = [article for articles in grouped_articles.values() for article in articles]
    for triptych_id, articles in grouped_articles.items():
        architecture_siblings = [candidate for candidate in all_articles if candidate.triptych_id != triptych_id]
        for article in articles:
            siblings = [candidate for candidate in articles if candidate.article_id != article.article_id]
            items.append(
                {
                    "article_id": article.article_id,
                    "triptych_id": article.triptych_id,
                    "triptych_label": article.triptych_label,
                    "type": article.type_code,
                    "title": article.title,
                    "wordpress_id": article.wordpress_id,
                    "wordpress_url": article.wordpress_url,
                    "publish_path": str(article.publish_path),
                    "source_path": str(article.source_path) if article.source_path else "",
                    "triptych_link_block": build_triptych_links_block(article, siblings),
                    "architecture_link_block": build_architecture_links_block(architecture_siblings),
                }
            )
    return {
        "triptych_dir": str(triptych_dir),
        "mode": "triptyque_linking_v2",
        "dry_run": True,
        "total": len(items),
        "items": items,
    }


def render_summary(triptych_dir: Path, results: list[LinkingResult], dry_run: bool) -> dict:
    return {
        "triptych_dir": str(triptych_dir),
        "mode": "triptyque_linking_v2",
        "dry_run": dry_run,
        "total": len(results),
        "updated_local": sum(1 for item in results if item.updated_paths),
        "updated_wordpress": sum(1 for item in results if item.status == "updated"),
        "items": [
            {
                "article_id": item.article_id,
                "type": item.type_code,
                "title": item.title,
                "wordpress_id": item.wordpress_id,
                "wordpress_url": item.wordpress_url,
                "updated_paths": item.updated_paths,
                "status": item.status,
                "error": item.error,
            }
            for item in results
        ],
        "errors": [item.error for item in results if item.error],
    }


def today_iso() -> str:
    return date.today().isoformat()


if __name__ == "__main__":
    raise SystemExit(main())
