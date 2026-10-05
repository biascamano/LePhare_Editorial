#!/usr/bin/env python3
"""
Shared helpers for index_editorial.csv — column contract, safe reads/writes, append.

Prevents misaligned rows (empty URL_WordPress / Slug_WordPress columns) that break
wp_push_draft.update_index and cause duplicate WordPress posts on retry.
"""

from __future__ import annotations

import csv
from pathlib import Path

# Canonical column order (must match index_editorial.csv header).
INDEX_COLUMNS: tuple[str, ...] = (
    "ID",
    "Titre",
    "Type",
    "Theme",
    "Statut",
    "Version",
    "Date_creation",
    "Date_derniere_maj",
    "Auteur",
    "Etape_sentier",
    "Articles_lies",
    "Mots_cles",
    "Resume_court",
    "Objectif",
    "Nom_fichier",
    "Chemin_dossier",
    "Date_publication_WP",
    "URL_WordPress",
    "Slug_WordPress",
    "Categorie_WP",
    "Tags_WP",
    "Remarques",
)


def safe_str(value: object, default: str = "") -> str:
    """Normalize CSV cell values (None → empty string)."""
    if value is None:
        return default
    return str(value).strip()


def normalize_row(row: dict[str, object], fieldnames: list[str] | None = None) -> dict[str, str]:
    """Ensure every expected column exists as a string (no None)."""
    cols = fieldnames or list(INDEX_COLUMNS)
    return {name: safe_str(row.get(name)) for name in cols}


def validate_row_columns(row: dict[str, str], fieldnames: list[str]) -> list[str]:
    """Return human-readable issues if row looks misaligned or incomplete."""
    issues: list[str] = []
    article_id = safe_str(row.get("ID"))
    if not article_id:
        issues.append("missing ID")
        return issues

    url = safe_str(row.get("URL_WordPress"))
    slug = safe_str(row.get("Slug_WordPress"))
    categorie = safe_str(row.get("Categorie_WP"))

    if url and not url.startswith(("http://", "https://")) and "." not in url.split("/")[0]:
        # Slug stored in URL column (classic misalignment)
        issues.append(f"URL_WordPress looks like a slug ({url!r}), not a URL")

    tags = safe_str(row.get("Tags_WP"))
    if categorie and ";" in categorie and not tags:
        issues.append("Categorie_WP contains ';' but Tags_WP is empty — likely column shift")

    if slug and slug.startswith(("http://", "https://")):
        issues.append("Slug_WordPress looks like a URL")

    for key in ("Remarques", "URL_WordPress", "Slug_WordPress", "Categorie_WP"):
        if key in row and row[key] is None:
            issues.append(f"{key} is None (DictReader misalignment)")

    missing = [c for c in fieldnames if c not in row]
    if missing:
        issues.append(f"missing columns: {', '.join(missing[:5])}")

    return issues


def read_index(index_path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not index_path.exists():
        raise FileNotFoundError(f"Index file not found: {index_path}")
    with index_path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        fieldnames = list(reader.fieldnames or [])
        if fieldnames != list(INDEX_COLUMNS):
            # Allow extra columns at end but warn via normalize; keep file fieldnames for round-trip
            pass
        rows = [normalize_row(row, fieldnames) for row in reader]
    return fieldnames, rows


def write_index(index_path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    normalized = [normalize_row(row, fieldnames) for row in rows]
    with index_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(normalized)


def build_index_row(
    *,
    article_id: str,
    title: str,
    type_code: str,
    theme_code: str,
    etape_sentier: str,
    linked_ids: list[str],
    keywords: list[str],
    summary: str,
    objective: str,
    filename: str,
    relative_folder: str,
    slug: str,
    wp_categories: list[str],
    wp_tags: list[str],
    remarques: str,
    statut: str = "pret_a_publier",
) -> dict[str, str]:
    from datetime import date

    today = date.today().isoformat()
    return normalize_row(
        {
            "ID": article_id,
            "Titre": title,
            "Type": type_code,
            "Theme": theme_code,
            "Statut": statut,
            "Version": "V1",
            "Date_creation": today,
            "Date_derniere_maj": today,
            "Auteur": "Le Phare Info",
            "Etape_sentier": etape_sentier,
            "Articles_lies": ";".join(linked_ids),
            "Mots_cles": ";".join(keywords),
            "Resume_court": summary,
            "Objectif": objective,
            "Nom_fichier": filename,
            "Chemin_dossier": relative_folder,
            "Date_publication_WP": "",
            "URL_WordPress": "",
            "Slug_WordPress": slug,
            "Categorie_WP": ";".join(wp_categories),
            "Tags_WP": ";".join(wp_tags),
            "Remarques": remarques,
        }
    )


def append_rows_to_index(index_path: Path, new_rows: list[dict[str, str]]) -> int:
    fieldnames, rows = read_index(index_path)
    if fieldnames != list(INDEX_COLUMNS):
        raise ValueError(
            f"index_editorial.csv header mismatch. Expected {len(INDEX_COLUMNS)} columns, "
            f"got {len(fieldnames)}. Use tools/index_editorial_utils.INDEX_COLUMNS."
        )
    existing_ids = {safe_str(r.get("ID")) for r in rows}
    appended = 0
    for row in new_rows:
        row = normalize_row(row, fieldnames)
        aid = safe_str(row.get("ID"))
        if not aid:
            raise ValueError("Index row missing ID")
        if aid in existing_ids:
            raise ValueError(f"Article ID already exists in index: {aid}")
        problems = validate_row_columns(row, fieldnames)
        if problems:
            raise ValueError(f"Invalid index row for {aid}: {'; '.join(problems)}")
        rows.append(row)
        existing_ids.add(aid)
        appended += 1
    write_index(index_path, fieldnames, rows)
    return appended


def scan_index_issues(index_path: Path) -> list[tuple[str, list[str]]]:
    """Return (article_id, issues) for rows that look misaligned."""
    fieldnames, rows = read_index(index_path)
    out: list[tuple[str, list[str]]] = []
    for row in rows:
        aid = safe_str(row.get("ID"))
        if not aid:
            continue
        issues = validate_row_columns(row, fieldnames)
        if issues:
            out.append((aid, issues))
    return out
