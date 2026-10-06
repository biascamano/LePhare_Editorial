"""Rebuild sentier_fondamentaux.csv with non-wiki canonical URLs (one-off helper)."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
manifest_path = ROOT / "00_Systeme/Manifests/sentier_fondamentaux.csv"
index_path = ROOT / "index_editorial.csv"

manifest = list(csv.DictReader(manifest_path.open(encoding="utf-8")))
rows = list(csv.DictReader(index_path.open(encoding="utf-8")))


def norm_slug(url: str) -> str:
    if not url:
        return ""
    s = url.replace("https://le-phare.info/", "").rstrip("/")
    for p in ("wiki-du-phare/", "wiki-du-phare-"):
        if s.startswith(p):
            s = s[len(p) :]
    return s


by_slug: dict[str, dict] = {}
for r in rows:
    if r.get("Type") not in ("SENTIER", "FOND"):
        continue
    u = r.get("URL_WordPress", "") or ""
    if not u:
        continue
    sl = norm_slug(u)
    is_wiki = "wiki-du-phare" in u
    entry = {
        "id": r["ID"],
        "url": u,
        "wiki": is_wiki,
        "chemin": r.get("Chemin_dossier", ""),
        "fichier": r.get("Nom_fichier", ""),
    }
    if sl not in by_slug:
        by_slug[sl] = entry
        continue
    cur = by_slug[sl]
    if cur["wiki"] and not is_wiki:
        by_slug[sl] = entry
    elif not cur["wiki"] and is_wiki:
        pass
    elif not is_wiki and not cur["wiki"]:
        # prefer lower numeric ID (older import = site root URL)
        if int(entry["id"].split("-")[1]) < int(cur["id"].split("-")[1]):
            by_slug[sl] = entry

out_rows = []
swaps = 0
for f in manifest:
    sl = f["slug_wp"]
    if int(f["fondamental_num"]) == 0:
        canon = by_slug.get(norm_slug(f.get("slug_wp", "")))
    else:
        canon = by_slug.get(sl)
    if canon and not canon["wiki"]:
        fid = f["fondamental_id"]
        if fid != canon["id"]:
            swaps += 1
        out_rows.append(
            {
                **f,
                "fondamental_id": canon["id"],
                "url_canonique": canon["url"],
                "chemin_canonique": canon["chemin"],
                "nom_fichier": canon["fichier"],
                "exclure_wiki": "oui" if canon["wiki"] else "non",
            }
        )
    else:
        out_rows.append(
            {
                **f,
                "url_canonique": "",
                "nom_fichier": "",
                "exclure_wiki": "manquant",
            }
        )

fieldnames = list(manifest[0].keys()) + ["url_canonique", "nom_fichier", "exclure_wiki"]
with manifest_path.open("w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
    w.writeheader()
    w.writerows(out_rows)

print(f"Wrote {len(out_rows)} rows, {swaps} ID swaps to non-wiki canonical")
