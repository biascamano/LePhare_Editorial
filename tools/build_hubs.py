"""Regenerate the « Liens internes du dossier » section of each dossier hub from the index.

Hub = DOSSIER article with the smallest ID in its 03_Dossiers/<Theme>/<Sous_dossier>/ folder.
Listed: the other DOSSIER articles of that folder, plus any article whose header « Dossier : »
names the hub ID, the sub-folder or the hub title. Local .md only; prints the --refresh-body commands."""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from index_editorial_utils import read_index  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SECTION = "## Liens internes du dossier"
NAV_FIRST = "**Repères de sources**"
META_RE = re.compile(r"^(?P<key>[^:\n]+?)\s*:\s*(?P<value>.*)$")


def norm(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "", text.lower())


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def header_dossier(path: Path) -> str:
    header = read_text(path).partition("\n---\n")[0]
    for line in header.splitlines():
        m = META_RE.match(line)
        if m and m["key"].strip().lstrip("﻿") == "Dossier":
            return m["value"].strip()
    return ""


def render_section(members: list[dict[str, str]]) -> str:
    lines = [SECTION]
    for r in members:
        title, url = r["Titre"].strip(), r["URL_WordPress"].strip()
        lines.append(f"- [{title}]({url})" if url else f"- {title}")
    return "\n".join(lines) + "\n"


def replace_section(text: str, section: str) -> str:
    start = text.find(SECTION + "\n")
    if start >= 0:
        rest = text[start + len(SECTION) + 1:]
        ends = [i for i in (rest.find("\n## "), rest.find("\n---\n"), rest.find("\n# ")) if i >= 0]
        end = start + len(SECTION) + 1 + (min(ends) + 1 if ends else len(rest))
        return text[:start] + section + ("\n" if end < len(text) else "") + text[end:].lstrip("\n")
    nav = text.find(NAV_FIRST)
    cut = text.rfind("\n---\n", 0, nav) if nav >= 0 else -1
    if cut < 0:
        return text.rstrip("\n") + "\n\n" + section
    return text[:cut].rstrip("\n") + "\n\n" + section + text[cut:]


def build(root: Path, index_path: Path, dry_run: bool) -> int:
    _, rows = read_index(index_path)
    folders: dict[str, list[dict[str, str]]] = {}
    for r in rows:
        folder = r["Chemin_dossier"].strip().replace("\\", "/")
        if r["Type"].strip() != "DOSSIER":
            continue
        if not re.fullmatch(r"03_Dossiers/[^/]+/[^/]+", folder):
            print(f"! {r['ID']} : DOSSIER hors 03_Dossiers/<Theme>/<Sous_dossier> ({folder!r}) — ignoré")
            continue
        folders.setdefault(folder, []).append(r)

    hubs: dict[str, dict[str, str]] = {}
    keys: dict[str, str] = {}
    for folder, members in folders.items():
        hub = min(members, key=lambda r: r["ID"].strip())
        hubs[folder] = hub
        for key in (hub["ID"].strip(), folder.rsplit("/", 1)[1], hub["Titre"]):
            keys[norm(key)] = folder

    extra: dict[str, list[dict[str, str]]] = {f: [] for f in folders}
    for r in rows:
        if r["Type"].strip() == "DOSSIER":
            continue
        path = root / r["Chemin_dossier"].strip() / r["Nom_fichier"].strip()
        if not r["Nom_fichier"].strip() or not path.is_file():
            continue
        value = header_dossier(path)
        if not value:
            continue
        folder = keys.get(norm(value))
        if folder is None:
            print(f"! {r['ID']} : « Dossier : {value} » ne correspond à aucun dossier — ignoré")
            continue
        extra[folder].append(r)

    changed = []
    for folder, hub in sorted(hubs.items()):
        assert not folder.startswith("02_Fonds")
        members = [r for r in folders[folder] if r is not hub] + extra[folder]
        members.sort(key=lambda r: r["ID"].strip())
        if not members:
            print(f"= {hub['ID']} {folder} (aucun autre article) — ignoré")
            continue
        path = root / folder / hub["Nom_fichier"].strip()
        if not path.is_file():
            print(f"! hub {hub['ID']} : fichier introuvable {folder}/{hub['Nom_fichier']}")
            continue
        text = read_text(path)
        new_text = replace_section(text, render_section(members))
        if new_text == text:
            print(f"= {hub['ID']} {folder} ({len(members)} articles) — inchangé")
            continue
        changed.append(hub)
        print(f"~ {hub['ID']} {folder} ({len(members)} articles){' [dry-run]' if dry_run else ''}")
        if not dry_run:
            path.write_text(new_text, encoding="utf-8")

    pushable = [h for h in changed if h["URL_WordPress"].strip()]
    if pushable:
        print("\nHubs déjà sur WordPress — à rafraîchir :")
        for h in pushable:
            rel = f"{h['Chemin_dossier'].strip()}/{h['Nom_fichier'].strip()}"
            print(f'python tools/wp_push_draft.py --refresh-body --config tools/wp_config.local.json --index index_editorial.csv "{rel}"')
    return 0


def main() -> int:
    global ROOT
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=str(ROOT))
    parser.add_argument("--index", help="défaut <root>/index_editorial.csv")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    ROOT = Path(args.root)
    index_path = Path(args.index) if args.index else ROOT / "index_editorial.csv"
    return build(ROOT, index_path, args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
