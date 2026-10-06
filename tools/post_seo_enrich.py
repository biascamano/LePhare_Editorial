#!/usr/bin/env python3
"""
Post-linking SEO / Rank Math enrichment for Le Phare triptychs (optional API pass).

Référence critères Rank Math (analyse de contenu, score 100) :
https://rankmath.com/kb/score-100-in-tests/

- Reads three article IDs (triptych) from index_editorial.csv (canonical paths).
- Calls an OpenAI-compatible Chat Completions API (default model from config: gpt-5.5).
- Rewrites the Markdown *after* the YAML frontmatter: # SEO block + corps, en préservant
  les faits et les URLs existantes ; le prompt système aligne les sorties sur les **tests**
  Rank Math (Basic SEO, Additional, lisibilité titre/contenu) **sans** clickbait ni
  contradiction avec les longueurs cibles Le Phare (Instructions 3.7).
- Writes canonical .md files back, puis optionnellement : wp_push_draft --refresh-body
  pour repousser HTML + meta Rank Math (rankmath/v1/updateMeta).

Activation : dans tools/editorial_config.local.json
  "seo_enrich_api_enabled": true
  + api_key renseignée + "seo_enrich_model": "gpt-5.5" (optionnel)

Usage :
  python tools/post_seo_enrich.py --article-ids 2026-457,2026-458,2026-459 \\
      --editorial-config tools/editorial_config.local.json \\
      --wp-config tools/wp_config.local.json --index index_editorial.csv

  python tools/post_seo_enrich.py ... --dry-run
  python tools/post_seo_enrich.py ... --no-wp-refresh   # seulement les .md locaux
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parent.parent
TOOLS_DIR = ROOT_DIR / "tools"
WP_PUSH_PATH = TOOLS_DIR / "wp_push_draft.py"

# Reuse frontmatter split from wp_push_draft (same format as depot)
from wp_push_draft import split_frontmatter  # noqa: E402


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="SEO/Rank Math enrichment pass after triptych maillage (API).")
    p.add_argument(
        "--article-ids",
        required=True,
        help="Comma-separated three IDs, ex. 2026-457,2026-458,2026-459",
    )
    p.add_argument("--index", default=str(ROOT_DIR / "index_editorial.csv"), help="Path to index_editorial.csv")
    p.add_argument(
        "--editorial-config",
        default=str(TOOLS_DIR / "editorial_config.local.json"),
        help="Editorial LLM JSON (api_key, seo_enrich_*)",
    )
    p.add_argument("--wp-config", default=str(TOOLS_DIR / "wp_config.local.json"), help="WordPress REST config")
    p.add_argument(
        "--ignore-config-gate",
        action="store_true",
        help="Run even if seo_enrich_api_enabled is false (usage avancé)",
    )
    p.add_argument("--dry-run", action="store_true", help="Print LLM JSON only, do not write files or WP")
    p.add_argument("--no-wp-refresh", action="store_true", help="Do not run wp_push_draft --refresh-body after writes")
    return p.parse_args()


def load_index_row(index_path: Path, article_id: str) -> dict[str, str]:
    with index_path.open("r", encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            if row.get("ID", "").strip() == article_id:
                return row
    raise ValueError(f"ID absent de l'index : {article_id}")


def resolve_canonical_path(row: dict[str, str]) -> Path:
    folder = row.get("Chemin_dossier", "").strip()
    name = row.get("Nom_fichier", "").strip()
    if not folder or not name:
        raise ValueError(f"Ligne index incomplète pour {row.get('ID')}")
    path = ROOT_DIR / folder / name
    if not path.is_file():
        raise FileNotFoundError(f"Fichier canonique introuvable : {path}")
    return path


def rebuild_frontmatter(metadata: dict[str, str]) -> str:
    lines = [f"{k} : {v}" for k, v in metadata.items()]
    return "\n".join(lines) + "\n---\n"


def truncate(s: str, max_chars: int) -> str:
    if len(s) <= max_chars:
        return s
    return s[: max_chars - 80] + "\n\n[… corps tronqué pour l'appel API ; conserver la fin et les sections Repères / Blocs en fin de fichier …]\n\n" + s[-4000:]


def load_editorial_raw(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def openai_chat_json(
    *,
    base_url: str,
    api_key: str,
    model: str,
    temperature: float,
    timeout: float,
    system: str,
    user: str,
    max_completion_tokens: int,
) -> dict[str, Any]:
    from urllib import error, request

    endpoint = f"{base_url.rstrip('/')}/chat/completions"
    payload: dict[str, Any] = {
        "model": model,
        "temperature": temperature,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "max_tokens": max_completion_tokens,
        "response_format": {"type": "json_object"},
    }
    req = request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=timeout) as response:
            data = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"API LLM HTTP {exc.code}: {detail}") from exc
    content = data["choices"][0]["message"]["content"]
    return json.loads(content)


SYSTEM_SEO_ENRICH = """Tu es réviseur SEO senior pour le site le-phare.info (Rank Math sur WordPress).
Tu reçois 3 articles d'un même triptyque (ACTU, TF, SENTIER). Tu optimises pour les **tests d'analyse de contenu**
Rank Math (cf. documentation officielle « Score 100/100 » : critères Basic SEO, Additional SEO,
lisibilité du titre, lisibilité du contenu — https://rankmath.com/kb/score-100-in-tests/ ),
sans sensationnalisme : slow journalism, faits exacts, pas d'invention de sources ni de chiffres.

Priorité : **le lecteur d'abord**. Les scores Rank Math sont des repères, pas une religion ; ne pas sacrifier
la nuance ni la sobriété éditoriale Le Phare pour un 100 artificiel.

--- Critères Rank Math à viser (quand c'est compatible avec le texte) ---

**Basic SEO (mot-clé principal = « Mot-clé principal » du bloc # SEO)**
- Présence du mot-clé dans le **Titre SEO** (snippet Rank Math) : idéalement dans les **~50 premiers caractères**
  (affichage SERP mobile ~50 car.).
- Présence dans la **méta-description** : dans les **120–160 premiers caractères** du texte de méta.
- **Slug / URL** : cohérent avec le champ « Slug propose » ; inclure les termes clés quand c'est naturel (le test
  « longueur d'URL » Rank Math compte souvent **toute** l'URL jusqu'à ~75 car. — domaine inclus ; ne pas forcer un slug absurde).
- Mot-clé dans les **10 % premiers du corps** (après le H1) ; si l'article fait moins de ~300 mots, Rank Math teste
  sur l'ensemble — rester factuel.
- Mot-clé présent **dans le corps** de façon naturelle (français : pas de règle de pluriel automatique comme en anglais).

**Longueur du contenu (sous-score Rank Math, souvent la cause d'un score bas)**
- Barème indicatif Rank Math pour ce test : **> 2500 mots ≈ 100 %** ; 2000–2500 ≈ 70 % ; 1500–2000 ≈ 60 % ;
  1000–1500 ≈ 40 % ; 600–1000 ≈ 20 % ; **< 600 ≈ 0 %**.
- **Contrainte Le Phare** : respecter d'abord les cibles par type (ACTU ~650–1100 ; TF plus long ; SENTIER outil dense).
  Pour le **TF**, enrichir sans digression jusqu'à **~1800–2200+ mots** *si la matière le porte* pour améliorer ce sous-score.
  Pour l'**ACTU**, ne **pas** allonger artificiellement : accepter un score **partiel** sur la longueur plutôt que du remplissage.

**Additional SEO**
- Au moins **un sous-titre H2 ou H3** intègre une formulation proche du mot-clé (sans bourrage ni répétition mécanique).
- **Densité** du mot-clé principal : viser **~1 % à 1,5 %** du texte utile ; **éviter > 2,5 %** (alerte sur-optimisation).
- **Liens externes** d'autorité : au moins **deux** domaines distincts crédibles (réutiliser les Repères quand possible) ;
  au moins **un** lien externe « suivi » par défaut (ne pas ajouter de `nofollow` sur des sources institutionnelles de confiance).
- **Liens internes** : au moins **2** vers d'autres articles du site quand c'est pertinent ; ne pas supprimer le bloc
  « ## Dans ce triptyque » ni les URLs déjà maillées.

**Médias (souvent 0 % si aucune image dans le HTML)**
- Si pertinent : ajouter au plus **1–2** images Markdown `![alt descriptif](URL)` avec **URL réelle** ; l'**alt** doit
  contenir une formulation naturelle proche du mot-clé pour au moins une image. **Ne pas inventer** d'URL ou de captures.
  (Rank Math peut exiger **plusieurs** médias pour 100 % sur ce test — signaler dans `notes_rank_math` si l'admin doit
  compléter dans l’éditeur WordPress.)

**Lisibilité du contenu**
- **Paragraphes courts** : viser **≤ ~120 mots** par bloc ; scinder les blocs trop longs.
- **Table des matières** : le test Rank Math repose souvent sur un **plugin / bloc TOC** côté WordPress ; ne pas simuler
  une fausse TOC en Markdown si ce n'est pas fiable. Indiquer dans `notes_rank_math` si l'éditeur doit ajouter le bloc
  « Table of Contents » Rank Math (ou plugin listé par Rank Math) après publication.

**Lisibilité du titre (Rank Math — secondaire)**
- Mot-clé dans la **première moitié** du Titre SEO.
- Tests « sentiment », « mot de pouvoir », « chiffre dans le titre » : les satisfaire **seulement** si cela reste **sobre**
  et non clickbait (ex. une année, « trois questions »). Sinon laisser un score partiel plutôt qu'un titre ridicule.

--- Forme et intérêt Le Phare (toujours) ---
- Moins « gabarit » : H2/H3 **concrets** liés au sujet ; fusionner ou subdiviser les sections si utile.
- Trois parcours **distincts** entre ACTU, TF et SENTIER ; pas trois squelettes identiques.
- Rester sobre : pas d'effet magazine artificiel.

Règles strictes :
- Conserver l'YAML frontmatter inchangé : tu NE le renvoies PAS ; tu ne renvoies que le champ markdown_remainder par article.
- Le markdown_remainder commence par la ligne exacte `# SEO` (ou # seo) puis Mot-clé principal, Meta-description, Titre SEO (si présent), puis `---`, puis le corps jusqu'à la fin du fichier (inclure ## Repères / ## Reperes, ## Dans ce triptyque, ## Bloc publication, ## Bloc image WordPress, ## Liens internes si présents).
- Ne supprime pas les URLs existantes ; tu peux compléter les Repères avec de vrais liens institutionnels.
- Répondre UNIQUEMENT en JSON objet avec la clé "articles" : liste de 3 objets { "article_id", "markdown_remainder", "notes_rank_math" }.
Le champ notes_rank_math résume en une phrase les **tests Rank Math** encore partiels (ex. longueur, TOC, médias) pour relecture humaine.
"""


def build_user_payload_bundle(
    articles: list[dict[str, Any]],
) -> str:
    return json.dumps({"triptych_articles": articles}, ensure_ascii=False, indent=2)


def main() -> int:
    args = parse_args()
    index_path = Path(args.index)
    editorial_path = Path(args.editorial_config)
    raw = load_editorial_raw(editorial_path)

    body_max_in = int(raw.get("seo_enrich_max_input_chars_per_article", 12000))

    ids = [x.strip() for x in args.article_ids.split(",") if x.strip()]
    if len(ids) != 3:
        print("post_seo_enrich: fournir exactement 3 IDs séparés par des virgules.", file=sys.stderr)
        return 2

    bundle: list[dict[str, Any]] = []
    paths: dict[str, Path] = {}
    for aid in ids:
        row = load_index_row(index_path, aid)
        path = resolve_canonical_path(row)
        paths[aid] = path
        text = path.read_text(encoding="utf-8")
        _meta, remainder = split_frontmatter(text)
        bundle.append(
            {
                "article_id": aid,
                "type": row.get("Type", ""),
                "theme": row.get("Theme", ""),
                "titre_index": row.get("Titre", ""),
                "url_wordpress": row.get("URL_WordPress", ""),
                "markdown_remainder_input": truncate(remainder, body_max_in),
            }
        )

    user_prompt = (
        "Améliore les trois articles pour Rank Math (WordPress), pour la diversité rédactionnelle, "
        "et pour un rendu **moins « gabarit »** : titres de sections adaptés au sujet, progression intéressante, "
        "pas trois textes au même squelette.\n"
        "Entrée JSON ci-dessous. Renvoie uniquement le JSON de sortie schema {articles:[...]}.\n\n"
        + build_user_payload_bundle(bundle)
    )

    if args.dry_run:
        print("--- dry-run : user prompt (tronqué affichage) ---")
        print(user_prompt[:12000])
        if len(user_prompt) > 12000:
            print("\n... [tronqué pour l'affichage] ...\n")
        return 0

    if not args.ignore_config_gate and not raw.get("seo_enrich_api_enabled"):
        print(
            "post_seo_enrich: seo_enrich_api_enabled est false dans la config éditoriale ; abandon.",
            file=sys.stderr,
        )
        return 2

    api_key = str(raw.get("api_key", "") or "").strip()
    if not api_key:
        print("post_seo_enrich: api_key vide dans la config éditoriale.", file=sys.stderr)
        return 2

    base_url = str(raw.get("base_url", "https://api.openai.com/v1")).rstrip("/")
    model = str(raw.get("seo_enrich_model") or raw.get("calibration_model") or "gpt-5.5").strip()
    temperature = float(raw.get("seo_enrich_temperature", raw.get("temperature", 0.35)))
    timeout = float(raw.get("seo_enrich_request_timeout_seconds", raw.get("request_timeout_seconds", 300)))
    max_out = int(raw.get("seo_enrich_max_output_tokens", 14000))

    try:
        result = openai_chat_json(
            base_url=base_url,
            api_key=api_key,
            model=model,
            temperature=temperature,
            timeout=timeout,
            system=SYSTEM_SEO_ENRICH,
            user=user_prompt,
            max_completion_tokens=max_out,
        )
    except Exception as exc:
        print(f"post_seo_enrich: erreur API : {exc}", file=sys.stderr)
        return 1

    items = result.get("articles")
    if not isinstance(items, list) or len(items) != 3:
        print("post_seo_enrich: réponse JSON invalide (articles[] attendu, len=3).", file=sys.stderr)
        print(json.dumps(result, ensure_ascii=False, indent=2)[:4000], file=sys.stderr)
        return 1

    for item in items:
        aid = str(item.get("article_id", "")).strip()
        md_rem = str(item.get("markdown_remainder", "")).strip()
        if aid not in paths:
            print(f"post_seo_enrich: article_id inconnu {aid}", file=sys.stderr)
            return 1
        if not re.search(r"(?im)^#\s*seo\s*$", md_rem[:2500], re.MULTILINE):
            print(f"post_seo_enrich: markdown_remainder sans bloc # SEO pour {aid}", file=sys.stderr)
            return 1
        path = paths[aid]
        full_text = path.read_text(encoding="utf-8")
        meta, _old_rem = split_frontmatter(full_text)
        new_text = rebuild_frontmatter(meta) + md_rem.lstrip("\n")
        if not new_text.endswith("\n"):
            new_text += "\n"
        path.write_text(new_text, encoding="utf-8")
        notes = item.get("notes_rank_math", "")
        print(f"OK écrit : {path} ({notes})")

    if args.no_wp_refresh:
        return 0

    wp_config = Path(args.wp_config)
    for aid in ids:
        cmd = [
            sys.executable,
            str(WP_PUSH_PATH),
            str(paths[aid]),
            "--config",
            str(wp_config),
            "--index",
            str(index_path),
            "--refresh-body",
        ]
        r = subprocess.run(cmd, cwd=str(ROOT_DIR), capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stdout + r.stderr, file=sys.stderr)
            print(f"post_seo_enrich: wp_push_draft --refresh-body a échoué pour {aid}", file=sys.stderr)
            return 1
        print(f"OK WordPress refresh : {aid}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
