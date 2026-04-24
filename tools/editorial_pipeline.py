#!/usr/bin/env python3
"""
Automate a Le Phare editorial triptych from a news topic.

Current MVP scope:
- generate a minimal editorial architecture manifest from a topic using an OpenAI-compatible LLM
- operationally generate either a triptych or a mini encyclopedie
- append the generated articles to index_editorial.csv
- duplicate the generated files into 07_A_Publier
- optionally push the publish folder to WordPress drafts through wp_push_draft.py

Supported modes:
1. architecture_editoriale
2. triptyque
3. mini_encyclopedie
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import socket
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any
from urllib import parse
from urllib import error, request


ROOT_DIR = Path(__file__).resolve().parent.parent
TOOLS_DIR = ROOT_DIR / "tools"
SYSTEM_DIR = ROOT_DIR / "00_Systeme"
PROMPTS_DIR = SYSTEM_DIR / "Prompts"
INDEX_PATH_DEFAULT = ROOT_DIR / "index_editorial.csv"
MANIFESTS_DIR = SYSTEM_DIR / "Manifests"
PUBLISH_DIR_ROOT = ROOT_DIR / "07_A_Publier"

CONTENT_MODES = ("architecture_editoriale", "triptyque", "mini_encyclopedie")
OUTPUT_PROFILES = ("triptyque_minimal", "dossier_2_triptyques", "dossier_3_triptyques", "reseau_5_contenus")
TYPE_ORDER = ("ACTU", "TF", "SENTIER")
MINI_TYPE_ORDER = ("DOSSIER",)
THEME_CODES = ("MONDE", "POL", "ECON", "TECH", "CLIMAT", "SCIENCE", "CULTURE")
SENTIER_POSTURES = ("Observer", "Questionner", "Comprendre", "Analyser", "Relier", "Transmettre")
POLITIQUE_FOLDER = "01_Actualites/Politique_Societe"
POLITIQUE_DOSSIER_FOLDER = "03_Dossiers/Politique_Societe"
DEFAULT_SENTIER_CRITIQUE_FOLDER = "05_Sentier/Etape_02_Pensee_critique"
FULL_SENTIER_ENUM = "Observer|Questionner|Comprendre|Analyser|Relier|Transmettre"
SENTIER_FOLDERS = (
    "05_Sentier/Etape_01_Culture_generale",
    DEFAULT_SENTIER_CRITIQUE_FOLDER,
    "05_Sentier/Etape_03_Argumentation",
    "05_Sentier/Etape_04_Expertise",
    "05_Sentier/Etape_05_Polyglotte",
    "05_Sentier/Etape_06_Methode_scientifique",
    "05_Sentier/Etape_07_Transmission",
    "05_Sentier/Etape_08_Relier_savoirs_et_experience",
    "05_Sentier/Etape_09_Equilibre_corps_esprit",
    "05_Sentier/Bonus_Art_de_la_memoire",
)

THEME_LABELS = {
    "MONDE": "Monde",
    "POL": "Politique & Societe",
    "ECON": "Economie & Finance",
    "TECH": "Technologie & IA",
    "CLIMAT": "Environnement & Climat",
    "SCIENCE": "Science & Sante",
    "CULTURE": "Culture & Philosophie",
}

ACTU_FOLDERS = {
    "MONDE": POLITIQUE_FOLDER,
    "POL": POLITIQUE_FOLDER,
    "ECON": "01_Actualites/Economie_Finance",
    "TECH": "01_Actualites/Technologie_IA",
    "CLIMAT": "01_Actualites/Climat_Transition",
    "SCIENCE": "01_Actualites/Science_Sante",
    "CULTURE": POLITIQUE_FOLDER,
}

DOSSIER_FOLDERS = {
    "MONDE": POLITIQUE_DOSSIER_FOLDER,
    "POL": POLITIQUE_DOSSIER_FOLDER,
    "ECON": "03_Dossiers/Economie_Finance",
    "TECH": "03_Dossiers/Technologie_IA",
    "CLIMAT": "03_Dossiers/Climat_Transition",
    "SCIENCE": "03_Dossiers/Science_Sante",
    "CULTURE": POLITIQUE_DOSSIER_FOLDER,
}

DEFAULT_SENTIER_FOLDERS = {
    "Observer": "05_Sentier/Etape_01_Culture_generale",
    "Questionner": DEFAULT_SENTIER_CRITIQUE_FOLDER,
    "Comprendre": "05_Sentier/Etape_06_Methode_scientifique",
    "Analyser": "05_Sentier/Etape_03_Argumentation",
    "Relier": "05_Sentier/Etape_08_Relier_savoirs_et_experience",
    "Transmettre": "05_Sentier/Etape_07_Transmission",
}


@dataclass
class LlmConfig:
    base_url: str
    api_key: str
    model: str
    temperature: float = 0.4
    request_timeout_seconds: float = 300.0
    manifest_max_tokens: int = 1800
    article_max_tokens: int = 2600
    repair_max_tokens: int = 3200
    allow_local_llm: bool = False


@dataclass
class PlannedArticle:
    article_id: str
    triptych_id: str
    triptych_label: str
    triptych_order: int
    type_code: str
    theme_code: str
    title: str
    objective: str
    summary: str
    keywords: list[str]
    primary_sources: list[str]
    etape_sentier: str
    wp_categories: list[str]
    wp_tags: list[str]
    relative_folder: str
    filename: str
    slug: str
    generated: dict[str, Any]


@dataclass
class TriptychWorkerBrief:
    triptych_id: str
    triptych_label: str
    triptych_order: int
    function: str
    core_tension: str
    covered_nodes: list[str]
    links_to_triptychs: list[str]
    article_blueprints: list[dict[str, Any]]
    related_triptychs: list[dict[str, Any]]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Le Phare editorial content from a news topic.")
    parser.add_argument("topic", help="News topic or working question")
    parser.add_argument("--mode", choices=CONTENT_MODES, default="architecture_editoriale", help="Editorial generation mode")
    parser.add_argument("--output-profile", choices=OUTPUT_PROFILES, default="triptyque_minimal", help="Requested editorial output profile")
    parser.add_argument("--angle", help="Optional editorial angle to privilege")
    parser.add_argument("--theme", choices=THEME_CODES, help="Optional theme override")
    parser.add_argument("--config", help="Path to local editorial LLM config JSON")
    parser.add_argument("--index", default=str(INDEX_PATH_DEFAULT), help="Path to index_editorial.csv")
    parser.add_argument("--manifest-only", action="store_true", help="Generate and save the manifest only")
    parser.add_argument("--publish-drafts", action="store_true", help="Push the generated folder to WordPress drafts")
    parser.add_argument("--wp-config", help="Path to tools/wp_config.local.json for WordPress push")
    parser.add_argument("--publish-folder-name", help="Optional custom folder name inside 07_A_Publier")
    parser.add_argument("--use-api-llm", action="store_true", help="Use an external OpenAI-compatible API LLM for manifest/article generation")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if not args.use_api_llm:
            raise ValueError(
                "API LLM generation is disabled by default in this project. "
                "Use the GPT-5.4 agent for default editorial writing, or pass --use-api-llm for explicit API generation."
            )
        llm_config = load_llm_config(args.config)
        print(f"Generating manifest for mode={args.mode}, output_profile={args.output_profile}...", flush=True)
        manifest = generate_manifest(
            topic=args.topic,
            mode=args.mode,
            output_profile=args.output_profile,
            angle=args.angle or "",
            forced_theme=args.theme or "",
            llm_config=llm_config,
        )
        assigned_ids = reserve_article_ids(Path(args.index), len(manifest["articles"]))
        publish_folder_name = args.publish_folder_name or build_publish_folder_name(args.topic, args.mode)
        manifest_path = write_manifest(manifest, publish_folder_name, assigned_ids)
        print(f"Manifest saved: {manifest_path}")

        if args.manifest_only:
            return 0

        print(f"Generating {len(manifest['articles'])} article(s) from manifest...", flush=True)
        planned_articles = generate_articles_from_manifest(
            manifest=manifest,
            assigned_ids=assigned_ids,
            publish_folder_name=publish_folder_name,
            llm_config=llm_config,
        )
        print("Writing articles locally...", flush=True)
        write_articles(planned_articles)
        print("Appending index rows...", flush=True)
        append_rows_to_index(Path(args.index), planned_articles)
        print("Duplicating publish folder...", flush=True)
        publish_dir = duplicate_to_publish_folder(planned_articles, publish_folder_name)
        print(f"Triptych generated locally in: {publish_dir}")

        if args.publish_drafts:
            if not args.wp_config:
                raise ValueError("--wp-config is required when --publish-drafts is used")
            print("Pushing drafts to WordPress...", flush=True)
            push_to_wordpress_drafts(publish_dir, Path(args.index), Path(args.wp_config))
            print(f"WordPress drafts pushed from: {publish_dir}")

        return 0
    except Exception as exc:
        print(f"Editorial pipeline error: {exc}", file=sys.stderr)
        return 1


def load_llm_config(config_path: str | None) -> LlmConfig:
    import os

    env_raw = {
        "base_url": os.environ.get("LP_LLM_BASE_URL", "https://api.openai.com/v1"),
        "api_key": os.environ.get("LP_LLM_API_KEY", "") or os.environ.get("OPENAI_API_KEY", ""),
        "model": os.environ.get("LP_LLM_MODEL", ""),
        "temperature": os.environ.get("LP_LLM_TEMPERATURE", "0.4"),
        "request_timeout_seconds": os.environ.get("LP_LLM_REQUEST_TIMEOUT_SECONDS", "300"),
        "manifest_max_tokens": os.environ.get("LP_LLM_MANIFEST_MAX_TOKENS", "1800"),
        "article_max_tokens": os.environ.get("LP_LLM_ARTICLE_MAX_TOKENS", "2600"),
        "repair_max_tokens": os.environ.get("LP_LLM_REPAIR_MAX_TOKENS", "3200"),
        "allow_local_llm": os.environ.get("LP_ALLOW_LOCAL_LLM", "false"),
    }

    if config_path:
        file_raw = json.loads(Path(config_path).read_text(encoding="utf-8"))
        raw = {
            key: file_raw.get(key) if str(file_raw.get(key, "")).strip() else env_raw.get(key)
            for key in env_raw
        }
    else:
        raw = env_raw

    missing = [key for key in ("base_url", "api_key", "model") if not str(raw.get(key, "")).strip()]
    if missing:
        raise ValueError(f"Missing LLM config value(s): {', '.join(missing)}")

    config = LlmConfig(
        base_url=str(raw["base_url"]).rstrip("/"),
        api_key=str(raw["api_key"]),
        model=str(raw["model"]),
        temperature=float(raw.get("temperature", 0.4)),
        request_timeout_seconds=float(raw.get("request_timeout_seconds", 300)),
        manifest_max_tokens=int(raw.get("manifest_max_tokens", 1800)),
        article_max_tokens=int(raw.get("article_max_tokens", 2600)),
        repair_max_tokens=int(raw.get("repair_max_tokens", 3200)),
        allow_local_llm=str(raw.get("allow_local_llm", "false")).strip().lower() in {"1", "true", "yes", "on"},
    )
    validate_llm_config_policy(config)
    return config


def validate_llm_config_policy(config: LlmConfig) -> None:
    parsed = parse.urlparse(config.base_url)
    hostname = (parsed.hostname or "").lower()
    if hostname in {"127.0.0.1", "localhost"} and not config.allow_local_llm:
        raise ValueError(
            "Local Ollama/local LLM configuration is disabled by project default. "
            "Use an external OpenAI-compatible API, or set allow_local_llm=true only for explicit fallback/test mode."
        )


def load_prompt_bundle() -> dict[str, str]:
    files = {
        "instructions": SYSTEM_DIR / "Instructions_editoriales_officielles.md",
        "prompt_architecture": PROMPTS_DIR / "Prompt_actualite_vers_architecture_editoriale_v1.md",
        "prompt_triptyque": PROMPTS_DIR / "Prompt_triptyque_v6.md",
        "prompt_actu": PROMPTS_DIR / "Prompt_article_actualite_quotidien.md",
        "prompt_cycle": PROMPTS_DIR / "Prompt_cadrage_cycle_editorial_v6.md",
        "modele_entete": SYSTEM_DIR / "Modele_Entete_Article.md",
    }
    return {key: path.read_text(encoding="utf-8") for key, path in files.items()}


def build_editorial_rules_summary() -> str:
    return (
        "Le Phare = slow journalism, pas de sensationnalisme, faits avant interpretations, "
        "analyse nuancee, lien explicite avec le Sentier du Savoir, structure claire, "
        "SEO integre, liens internes, sources fiables, publisable sur WordPress."
    )


def normalize_generation_mode(mode: str) -> str:
    if mode == "architecture_editoriale":
        return "triptyque"
    return mode


def normalize_output_profile(requested_mode: str, output_profile: str) -> str:
    if requested_mode == "mini_encyclopedie":
        return "reseau_5_contenus"
    if requested_mode != "architecture_editoriale":
        return "triptyque_minimal"
    return output_profile


def output_profile_triptych_count(requested_mode: str, output_profile: str) -> int:
    if requested_mode != "architecture_editoriale":
        return 1
    if output_profile == "dossier_2_triptyques":
        return 2
    if output_profile == "dossier_3_triptyques":
        return 3
    return 1


def build_manifest_prompt_summary(requested_mode: str) -> str:
    if requested_mode == "architecture_editoriale":
        return (
            "Generer une architecture editoriale minimale a partir d'une actualite, puis en extraire "
            "un triptyque minimal compose de 3 articles: ACTU, TF, SENTIER. "
            "Le triptyque doit rester la plus petite forme publiable coherente et s'inscrire dans "
            "un cycle de comprehension du Sentier."
        )
    return (
        "Generer un triptyque editorial compose de 3 articles: ACTU, TF, SENTIER. "
        "Le triptyque doit s'inscrire dans un cycle de comprehension et activer une posture "
        "du Sentier parmi Observer, Questionner, Comprendre, Analyser, Relier."
    )


def build_mini_encyclopedie_prompt_summary() -> str:
    return (
        "Generer une mini-encyclopedie a partir d'une actualite, sous forme d'un seul DOSSIER structuré en 10 parties : "
        "evenement, chronologie, acteurs, contextes historique/geopolitique/economique, analyse du phenomene, "
        "decryptage des biais, concepts cles, histoire des idees, comparaisons historiques, carte globale du sujet, "
        "sentier du savoir, explorer plus loin. Le dossier doit etre factuel, pedagogique, nuance et non sensationnaliste."
    )


def build_architecture_manifest_schema() -> dict[str, Any]:
    return {
        "question_centrale": "string",
        "architecture_summary": "2-4 sentences",
        "knowledge_layer": {
            "central_nodes": ["1-3 node labels"],
            "nodes": [
                {
                    "node_id": "string",
                    "label": "string",
                    "node_type": "Evenement|Concept|Acteur|Systeme|Temporalite|Tension|Reference|Piste",
                    "definition": "string",
                    "editorial_role": "string",
                    "reuse_potential": "faible|moyen|fort",
                }
            ],
            "relations": [
                {
                    "source": "node_id",
                    "relation": "explique|revele|cause|aggrave|depend_de|s_oppose_a|prolonge|historise|incarne|ralentit|accelere",
                    "target": "node_id",
                }
            ],
            "editorial_tensions": ["2-3 tensions editoriales"],
            "durable_pivots": ["concepts or references to stabilize"],
        },
        "publication_layer": {
            "recommended_entrypoint": "ACTU|CLE|ANALYSE|TF|SENTIER",
            "content_candidates": [
                {
                    "content_id": "string",
                    "type_code": "ACTU|TF|SENTIER|CLE|ANALYSE|CHRONO|ACTEURS",
                    "title": "string",
                    "question": "string",
                    "covered_nodes": ["node_id"],
                    "editorial_function": "porte_entree|clarification|approfondissement|mise_en_tension|historicisation|exercice_critique|ouverture",
                }
            ],
            "triptych_candidates": [
                {
                    "triptych_id": "string",
                    "label": "string",
                    "function": "minimal|structurel|temps_long|acteurs|prospectif",
                    "core_tension": "string",
                    "covered_nodes": ["node_id"],
                    "recommended_order": 1,
                }
            ],
            "recommended_triptych_id": "string",
            "publication_sequence": ["triptych_id-1", "triptych_id-2"],
        },
    }


def ensure_architecture_layer_defaults(manifest: dict[str, Any]) -> None:
    question = sanitize_inline(str(manifest.get("cycle_question", "")))
    summary = sanitize_inline(str(manifest.get("topic_summary", "")))
    theme_code = sanitize_inline(str(manifest.get("theme_code", "")))
    triptych_role = sanitize_inline(str(manifest.get("triptych_role", "")))

    default_nodes = [
        {
            "node_id": "evt_1",
            "label": sanitize_inline(str(manifest.get("source_topic", "Actualite"))),
            "node_type": "Evenement",
            "definition": summary or "Evenement d'actualite servant de point d'entree editorial.",
            "editorial_role": "porte d'entree",
            "reuse_potential": "moyen",
        }
    ]
    default_relations: list[dict[str, str]] = []
    default_tensions = [question] if question else []
    default_pivots = [theme_code] if theme_code else []

    knowledge_layer = manifest.get("knowledge_layer")
    if not isinstance(knowledge_layer, dict):
        knowledge_layer = {}
    knowledge_layer.setdefault("central_nodes", [default_nodes[0]["label"]])
    knowledge_layer.setdefault("nodes", default_nodes)
    knowledge_layer.setdefault("relations", default_relations)
    knowledge_layer.setdefault("editorial_tensions", default_tensions)
    knowledge_layer.setdefault("durable_pivots", default_pivots)
    manifest["knowledge_layer"] = knowledge_layer

    first_article_title = sanitize_inline(str(manifest["articles"][0]["title"])) if manifest.get("articles") else "Triptyque minimal"
    publication_layer = manifest.get("publication_layer")
    if not isinstance(publication_layer, dict):
        publication_layer = {}
    publication_layer.setdefault("recommended_entrypoint", "ACTU")
    publication_layer.setdefault(
        "content_candidates",
        [
            {
                "content_id": sanitize_inline(str(article.get("type_code", ""))).lower(),
                "type_code": sanitize_inline(str(article.get("type_code", ""))),
                "title": sanitize_inline(str(article.get("title", ""))),
                "question": sanitize_inline(str(article.get("objective", ""))),
                "covered_nodes": ["evt_1"],
                "editorial_function": "porte_entree" if article.get("type_code") == "ACTU" else "approfondissement",
            }
            for article in manifest.get("articles", [])
        ],
    )
    publication_layer.setdefault(
        "triptych_candidates",
        [
            {
                "triptych_id": "triptyque_minimal_1",
                "label": first_article_title,
                "function": "minimal",
                "core_tension": question or triptych_role,
                "covered_nodes": ["evt_1"],
                "recommended_order": 1,
            }
        ],
    )
    publication_layer.setdefault("recommended_triptych_id", "triptyque_minimal_1")
    publication_layer.setdefault("publication_sequence", ["triptyque_minimal_1"])
    manifest["publication_layer"] = publication_layer

    manifest.setdefault("question_centrale", question or manifest.get("cycle_question", ""))
    manifest.setdefault("architecture_summary", summary or "Architecture editoriale minimale construite depuis l'actualite.")
    manifest.setdefault("output_profile", "triptyque_minimal")
    manifest.setdefault(
        "guardrails",
        {
            "max_triptychs": 1,
            "max_overlap_ratio": 0.35,
            "require_distinct_function": True,
            "require_sentier_link": True,
        },
    )


def normalize_triptych_articles(manifest: dict[str, Any], expected_triptych_count: int) -> None:
    articles = manifest.get("articles", [])
    if not isinstance(articles, list) or not articles:
        return

    current_triptych_id = ""
    current_order = 0
    local_index = 0
    for article in articles:
        triptych_id = sanitize_inline(str(article.get("triptych_id", "")))
        if triptych_id:
            if triptych_id != current_triptych_id:
                current_triptych_id = triptych_id
                current_order += 1
                local_index = 0
        else:
            if local_index % 3 == 0:
                current_order += 1
                current_triptych_id = f"triptyque_{current_order}"
            article["triptych_id"] = current_triptych_id
        if not article.get("triptych_label"):
            article["triptych_label"] = f"Triptyque {current_order}"
        article["triptych_order"] = int(article.get("triptych_order") or current_order)
        local_index += 1

    publication_layer = manifest.get("publication_layer")
    if isinstance(publication_layer, dict) and expected_triptych_count > 1:
        sequence = publication_layer.get("publication_sequence")
        if not sequence:
            publication_layer["publication_sequence"] = [f"triptyque_{idx}" for idx in range(1, expected_triptych_count + 1)]
        if not publication_layer.get("recommended_triptych_id"):
            publication_layer["recommended_triptych_id"] = "triptyque_1"
        manifest["publication_layer"] = publication_layer


def build_article_prompt_summary(type_code: str) -> str:
    if type_code == "ACTU":
        return (
            "Article d'actualite Le Phare: exposer le fait, le contexte, l'analyse, "
            "les biais et le lien avec le Sentier. Ton pedagogique, rigoureux, non sensationnaliste."
        )
    if type_code == "DOSSIER":
        return (
            "Mini-encyclopedie Le Phare: produire un DOSSIER unique, tres structure, pedagogique et nuance, "
            "en 10 parties couvrant evenement, contextes, causes, dynamiques, scenarios, biais, concepts, "
            "textes fondateurs, comparaisons historiques, sentier du savoir et pistes d'approfondissement."
        )
    if type_code == "TF":
        return (
            "Texte fondateur Le Phare: presenter un auteur, une oeuvre ou un concept, "
            "expliquer en quoi cela eclaire directement l'actualite et extraire un outil de lecture durable."
        )
    return (
        "Article Sentier Le Phare: proposer un outil cognitif ou critique, "
        "un exercice de reflexion guide et un lien explicite avec une etape du Sentier."
    )


def generate_manifest(
    topic: str,
    mode: str,
    output_profile: str,
    angle: str,
    forced_theme: str,
    llm_config: LlmConfig,
) -> dict[str, Any]:
    generation_mode = normalize_generation_mode(mode)
    normalized_output_profile = normalize_output_profile(mode, output_profile)
    expected_triptych_count = output_profile_triptych_count(mode, normalized_output_profile)
    manifest_schema: dict[str, Any] = {
        "cycle_question": "string",
        "cycle_status": "exploratoire|critique|fondateur",
        "active_posture": "Observer|Questionner|Comprendre|Analyser|Relier",
        "triptych_role": "ouverture|mise_en_tension|approfondissement|recul",
        "theme_code": "MONDE|POL|ECON|TECH|CLIMAT|SCIENCE|CULTURE",
        "category_label": "human readable category label",
        "angle": "string",
        "topic_summary": "2-3 sentences",
        "articles": []
    }
    if mode == "architecture_editoriale":
        manifest_schema.update(build_architecture_manifest_schema())

    if generation_mode == "triptyque":
        manifest_schema["articles"] = [
            {
                "triptych_id": "triptyque_1",
                "triptych_label": "string",
                "triptych_order": 1,
                "type_code": "ACTU|TF|SENTIER",
                "title": "string",
                "objective": "string",
                "summary": "string",
                "keywords": ["3-6 short keywords"],
                "primary_sources": ["3-6 source names"],
                "etape_sentier": FULL_SENTIER_ENUM,
                "wp_categories": ["slug-1", "slug-2"],
                "wp_tags": ["slug-1", "slug-2", "slug-3"],
                "relative_folder": "exact relative path inside the repository"
            }
        ]
    else:
        manifest_schema["articles"] = [
            {
                "type_code": "DOSSIER",
                "title": "string",
                "objective": "string",
                "summary": "string",
                "keywords": ["4-8 short keywords"],
                "primary_sources": ["4-8 source names"],
                "etape_sentier": FULL_SENTIER_ENUM,
                "wp_categories": ["slug-1", "slug-2"],
                "wp_tags": ["slug-1", "slug-2", "slug-3"],
                "relative_folder": "exact relative path inside the repository"
            }
        ]

    prompt = f"""
Tu dois produire UNIQUEMENT un JSON valide, sans markdown, sans commentaires.

Contexte utilisateur:
- Sujet d'actualite: {topic}
- Angle prefere: {angle or "Aucun angle impose"}
- Theme force: {forced_theme or "Aucun theme impose"}
- Profil de sortie demande: {normalized_output_profile}

Resume editorial:
{build_editorial_rules_summary()}

Mode editorial demande: {mode}
Mode generation effectif: {generation_mode}
Profil de sortie normalise: {normalized_output_profile}

Resume de generation:
{build_manifest_prompt_summary(mode) if generation_mode == "triptyque" else build_mini_encyclopedie_prompt_summary()}

Referentiel autorise:
- theme_code parmi: {", ".join(THEME_CODES)}
- active_posture parmi: Observer, Questionner, Comprendre, Analyser, Relier
- etape_sentier parmi: {", ".join(SENTIER_POSTURES)}
- relative_folder pour ACTU parmi: {", ".join(sorted(ACTU_FOLDERS.values()))}
- relative_folder pour TF: 04_Textes_fondateurs/Auteurs
- relative_folder pour SENTIER parmi: {", ".join(SENTIER_FOLDERS)}
- relative_folder pour DOSSIER parmi: {", ".join(sorted(DOSSIER_FOLDERS.values()))} + un sous-dossier dedie au sujet
- si mode effectif triptyque: exactement 3 articles, un de chaque type: ACTU, TF, SENTIER
- si mode effectif mini_encyclopedie: exactement 1 article de type DOSSIER
- si mode demande architecture_editoriale: fournir aussi question_centrale, architecture_summary, knowledge_layer et publication_layer
- si mode demande architecture_editoriale: output_profile doit etre coherent avec {", ".join(OUTPUT_PROFILES)}
- si output_profile = triptyque_minimal: produire exactement 1 triptyque
- si output_profile = dossier_2_triptyques: produire exactement 2 triptyques, donc 6 articles groupes par triptych_id
- si output_profile = dossier_3_triptyques: produire exactement 3 triptyques, donc 9 articles groupes par triptych_id
- les wp_categories et wp_tags doivent etre des slugs ASCII en minuscules, separes ensuite par JSON array

Schema cible:
{json.dumps(manifest_schema, ensure_ascii=False, indent=2)}
""".strip()

    raw = call_llm_json(
        llm_config=llm_config,
        system_prompt="Tu es un architecte editorial pour Le Phare Info. Tu renvoies uniquement du JSON valide.",
        user_prompt=prompt,
        max_tokens=llm_config.manifest_max_tokens,
    )
    validate_manifest(raw, generation_mode, forced_theme, mode, normalized_output_profile)
    normalize_manifest(
        raw,
        mode,
        generation_mode,
        normalized_output_profile,
        expected_triptych_count,
        topic,
        angle,
        forced_theme,
    )
    return raw


def validate_manifest(
    manifest: dict[str, Any],
    mode: str,
    forced_theme: str,
    requested_mode: str,
    output_profile: str,
) -> None:
    required_top = (
        "cycle_question",
        "cycle_status",
        "active_posture",
        "triptych_role",
        "theme_code",
        "category_label",
        "angle",
        "topic_summary",
        "articles",
    )
    for key in required_top:
        if key not in manifest:
            raise ValueError(f"Manifest missing key: {key}")

    if forced_theme and manifest["theme_code"] != forced_theme:
        manifest["theme_code"] = forced_theme

    if manifest["theme_code"] not in THEME_CODES:
        raise ValueError(f"Unsupported theme_code in manifest: {manifest['theme_code']}")
    if manifest["active_posture"] not in SENTIER_POSTURES[:5]:
        raise ValueError(f"Unsupported active_posture in manifest: {manifest['active_posture']}")

    articles = manifest["articles"]
    expected_triptychs = output_profile_triptych_count(requested_mode, output_profile)
    expected_count = (3 * expected_triptychs) if mode == "triptyque" else 1
    if not isinstance(articles, list) or len(articles) != expected_count:
        raise ValueError(f"Manifest must contain exactly {expected_count} article(s) for mode {mode}")

    seen = {item.get("type_code") for item in articles}
    if mode == "triptyque" and expected_triptychs == 1 and seen != set(TYPE_ORDER):
        raise ValueError("Manifest articles must contain ACTU, TF and SENTIER exactly once")
    if mode == "triptyque" and expected_triptychs > 1:
        grouped: dict[str, list[str]] = {}
        for index, item in enumerate(articles, start=1):
            triptych_id = sanitize_inline(str(item.get("triptych_id") or f"triptyque_{((index - 1) // 3) + 1}"))
            grouped.setdefault(triptych_id, []).append(sanitize_inline(str(item.get("type_code", ""))))
        if len(grouped) != expected_triptychs:
            raise ValueError(f"Manifest must contain exactly {expected_triptychs} triptych group(s)")
        for triptych_id, type_codes in grouped.items():
            if set(type_codes) != set(TYPE_ORDER) or len(type_codes) != len(TYPE_ORDER):
                raise ValueError(f"Triptych group {triptych_id} must contain ACTU, TF and SENTIER exactly once")
    if mode == "mini_encyclopedie" and seen != set(MINI_TYPE_ORDER):
        raise ValueError("Manifest mini_encyclopedie must contain exactly one DOSSIER")


def normalize_manifest(
    manifest: dict[str, Any],
    requested_mode: str,
    generation_mode: str,
    output_profile: str,
    expected_triptych_count: int,
    topic: str,
    angle: str,
    forced_theme: str,
) -> None:
    manifest["source_topic"] = topic
    manifest["requested_mode"] = requested_mode
    manifest["content_mode"] = generation_mode
    manifest["output_profile"] = output_profile
    if angle:
        manifest["source_angle"] = angle
    manifest["theme_code"] = forced_theme or manifest["theme_code"]
    manifest["category_label"] = THEME_LABELS.get(manifest["theme_code"], manifest["category_label"])
    if requested_mode == "architecture_editoriale":
        ensure_architecture_layer_defaults(manifest)
    if generation_mode == "triptyque":
        normalize_triptych_articles(manifest, expected_triptych_count)

    for article in manifest["articles"]:
        article["relative_folder"] = normalize_relative_folder(
            type_code=article["type_code"],
            relative_folder=article.get("relative_folder", ""),
            etape_sentier=article.get("etape_sentier", ""),
            theme_code=manifest["theme_code"],
            topic=topic,
        )
        article["wp_categories"] = normalize_slug_list(article.get("wp_categories", []))
        article["wp_tags"] = normalize_slug_list(article.get("wp_tags", []))
        article["keywords"] = normalize_keyword_list(article.get("keywords", []))
        article["primary_sources"] = normalize_keyword_list(article.get("primary_sources", []))
        article["etape_sentier"] = article.get("etape_sentier") or manifest["active_posture"]


def normalize_relative_folder(type_code: str, relative_folder: str, etape_sentier: str, theme_code: str, topic: str) -> str:
    if type_code == "ACTU":
        for folder in ACTU_FOLDERS.values():
            if relative_folder == folder:
                return folder
        return ACTU_FOLDERS["POL"]
    if type_code == "DOSSIER":
        dossier_root = DOSSIER_FOLDERS.get(theme_code, DOSSIER_FOLDERS["POL"])
        normalized_topic = slugify(topic).replace("-", "_")[:80] or "mini_encyclopedie"
        if relative_folder.startswith(dossier_root):
            return relative_folder
        return f"{dossier_root}/{normalized_topic}_Mini_Encyclopedie"
    if type_code == "TF":
        return "04_Textes_fondateurs/Auteurs"
    if type_code == "SENTIER":
        if relative_folder in SENTIER_FOLDERS:
            return relative_folder
        return DEFAULT_SENTIER_FOLDERS.get(etape_sentier, DEFAULT_SENTIER_CRITIQUE_FOLDER)
    raise ValueError(f"Unsupported type_code: {type_code}")


def normalize_slug_list(values: list[Any]) -> list[str]:
    cleaned = []
    for value in values:
        slug = slugify(str(value))
        if slug:
            cleaned.append(slug)
    return unique_preserve_order(cleaned)


def normalize_keyword_list(values: list[Any]) -> list[str]:
    cleaned = []
    for value in values:
        item = sanitize_inline(str(value))
        if item:
            cleaned.append(item)
    return unique_preserve_order(cleaned)


def reserve_article_ids(index_path: Path, count: int) -> list[str]:
    year = date.today().year
    max_number = 0
    if index_path.exists():
        with index_path.open("r", encoding="utf-8-sig", newline="") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                article_id = row.get("ID", "").strip()
                match = re.match(rf"^{year}-(\d+)$", article_id)
                if match:
                    max_number = max(max_number, int(match.group(1)))

    return [f"{year}-{value:03d}" for value in range(max_number + 1, max_number + count + 1)]


def build_publish_folder_name(topic: str, mode: str) -> str:
    if mode == "mini_encyclopedie":
        suffix = "mini_encyclopedie"
    elif mode == "architecture_editoriale":
        suffix = "architecture_editoriale"
    else:
        suffix = "triptyque"
    return f"{_today_iso()}_{slugify(topic)[:60]}_{suffix}"


def write_manifest(manifest: dict[str, Any], publish_folder_name: str, assigned_ids: list[str]) -> Path:
    MANIFESTS_DIR.mkdir(parents=True, exist_ok=True)
    payload = json.loads(json.dumps(manifest))
    payload["assigned_article_ids"] = assigned_ids
    payload["generated_on"] = _today_iso()
    payload["publish_folder_name"] = publish_folder_name
    path = MANIFESTS_DIR / f"{publish_folder_name}.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def build_triptych_worker_briefs(
    manifest: dict[str, Any],
    ordered_articles: list[dict[str, Any]],
    article_ids: dict[int, str],
) -> list[TriptychWorkerBrief]:
    grouped_articles: dict[str, list[dict[str, Any]]] = {}
    for article in ordered_articles:
        triptych_id = sanitize_inline(str(article.get("triptych_id", "triptyque_1")))
        grouped_articles.setdefault(triptych_id, []).append(article)

    publication_layer = manifest.get("publication_layer")
    candidate_map: dict[str, dict[str, Any]] = {}
    sequence: list[str] = []
    if isinstance(publication_layer, dict):
        for candidate in publication_layer.get("triptych_candidates", []):
            if isinstance(candidate, dict):
                candidate_triptych_id = sanitize_inline(str(candidate.get("triptych_id", "")))
                if candidate_triptych_id:
                    candidate_map[candidate_triptych_id] = candidate
        sequence = [
            sanitize_inline(str(item))
            for item in publication_layer.get("publication_sequence", [])
            if sanitize_inline(str(item)) in grouped_articles
        ]

    if not sequence:
        sequence = sorted(
            grouped_articles.keys(),
            key=lambda triptych_id: int(grouped_articles[triptych_id][0].get("triptych_order", 1)),
        )
    else:
        for triptych_id in sorted(
            grouped_articles.keys(),
            key=lambda item: int(grouped_articles[item][0].get("triptych_order", 1)),
        ):
            if triptych_id not in sequence:
                sequence.append(triptych_id)

    briefs: list[TriptychWorkerBrief] = []
    for triptych_id in sequence:
        triptych_articles = sorted(
            grouped_articles[triptych_id],
            key=lambda item: TYPE_ORDER.index(item["type_code"]),
        )
        first_article = triptych_articles[0]
        candidate = candidate_map.get(triptych_id, {})
        triptych_order = int(first_article.get("triptych_order", len(briefs) + 1))
        triptych_label = sanitize_inline(str(first_article.get("triptych_label", ""))) or f"Triptyque {triptych_order}"
        direct_links = [
            sanitize_inline(str(item))
            for item in candidate.get("links_to_triptychs", [])
            if sanitize_inline(str(item)) in grouped_articles and sanitize_inline(str(item)) != triptych_id
        ]
        if not direct_links:
            direct_links = [other_id for other_id in sequence if other_id != triptych_id]

        related_triptychs = []
        for other_id in sequence:
            if other_id == triptych_id:
                continue
            other_articles = grouped_articles[other_id]
            other_first = other_articles[0]
            other_candidate = candidate_map.get(other_id, {})
            related_triptychs.append(
                {
                    "triptych_id": other_id,
                    "label": sanitize_inline(str(other_first.get("triptych_label", ""))) or f"Triptyque {other_first.get('triptych_order', 1)}",
                    "recommended_order": int(other_first.get("triptych_order", 1)),
                    "function": sanitize_inline(str(other_candidate.get("function", ""))),
                    "core_tension": sanitize_inline(str(other_candidate.get("core_tension", ""))),
                    "is_directly_linked": other_id in direct_links,
                }
            )

        article_blueprints = []
        for article in triptych_articles:
            article_blueprints.append(
                {
                    "article_id": article_ids[id(article)],
                    "type_code": article["type_code"],
                    "title": article["title"],
                    "objective": article["objective"],
                    "summary": article["summary"],
                    "keywords": article["keywords"],
                    "primary_sources": article["primary_sources"],
                    "etape_sentier": article["etape_sentier"],
                    "wp_categories": article["wp_categories"],
                    "wp_tags": article["wp_tags"],
                    "relative_folder": article["relative_folder"],
                }
            )

        briefs.append(
            TriptychWorkerBrief(
                triptych_id=triptych_id,
                triptych_label=triptych_label,
                triptych_order=triptych_order,
                function=sanitize_inline(str(candidate.get("function", ""))) or "minimal",
                core_tension=sanitize_inline(str(candidate.get("core_tension", ""))) or sanitize_inline(str(manifest.get("question_centrale", manifest.get("cycle_question", "")))),
                covered_nodes=[
                    sanitize_inline(str(node_id))
                    for node_id in candidate.get("covered_nodes", [])
                    if sanitize_inline(str(node_id))
                ],
                links_to_triptychs=direct_links,
                article_blueprints=article_blueprints,
                related_triptychs=related_triptychs,
            )
        )

    return briefs


def generate_triptych_payloads(
    manifest: dict[str, Any],
    brief: TriptychWorkerBrief,
    llm_config: LlmConfig,
) -> dict[str, dict[str, Any]]:
    article_schema = {
        "triptych_id": brief.triptych_id,
        "triptych_label": brief.triptych_label,
        "articles": [
            {
                "article_id": "string",
                "type_code": "ACTU|TF|SENTIER",
                "title": "string",
                "objective": "string",
                "summary": "string under 500 characters",
                "keywords": ["3-6 keywords"],
                "primary_sources": ["3-6 source names"],
                "etape_sentier": "Observer|Questionner|Comprendre|Analyser|Relier|Transmettre",
                "seo_keyword": "string",
                "meta_description": "150-160 characters target",
                "slug": "ascii-slug",
                "image_suggestion": "string",
                "image_caption": "string",
                "body_markdown": "markdown body starting with # Title and using H2/H3 sections only",
            }
        ],
    }
    knowledge_layer = manifest.get("knowledge_layer") if isinstance(manifest.get("knowledge_layer"), dict) else {}
    worker_context = {
        "triptych_id": brief.triptych_id,
        "triptych_label": brief.triptych_label,
        "triptych_order": brief.triptych_order,
        "function": brief.function,
        "core_tension": brief.core_tension,
        "covered_nodes": brief.covered_nodes,
        "links_to_triptychs": brief.links_to_triptychs,
    }

    prompt = f"""
Tu dois produire UNIQUEMENT un JSON valide, sans markdown de commentaire externe.

Resume editorial Le Phare:
{build_editorial_rules_summary()}

Contexte d'architecture editoriale:
- Question centrale: {manifest.get("question_centrale", manifest["cycle_question"])}
- Resume d'architecture: {manifest.get("architecture_summary", manifest.get("topic_summary", ""))}
- Sujet initial: {manifest["source_topic"]}
- Angle: {manifest.get("source_angle", manifest["angle"])}
- Theme code: {manifest["theme_code"]}
- Categorie: {manifest["category_label"]}
- Statut du cycle: {manifest["cycle_status"]}
- Posture active: {manifest["active_posture"]}
- Role editorial global: {manifest["triptych_role"]}

Knowledge layer utile:
{json.dumps({
    "central_nodes": knowledge_layer.get("central_nodes", []),
    "editorial_tensions": knowledge_layer.get("editorial_tensions", []),
    "durable_pivots": knowledge_layer.get("durable_pivots", []),
    "relations": knowledge_layer.get("relations", []),
}, ensure_ascii=False, indent=2)}

Worker triptyque a executer:
{json.dumps(worker_context, ensure_ascii=False, indent=2)}

Autres triptyques de l'architecture:
{json.dumps(brief.related_triptychs, ensure_ascii=False, indent=2)}

Articles a produire dans CE triptyque:
{json.dumps(brief.article_blueprints, ensure_ascii=False, indent=2)}

Contraintes de sortie:
- produire exactement 3 articles et exactement un ACTU, un TF, un SENTIER
- conserver exactement les `article_id` et `type_code` fournis
- conserver les titres cibles si possible, et rester tres proche des objectifs/resumes fournis
- chaque article doit rester publiable seul, mais l'ensemble doit former un triptyque coherent
- la fonction propre du triptyque doit etre perceptible dans les trois articles
- les autres triptyques peuvent etre mentionnes comme perspectives voisines, sans diluer ce triptyque
- pour chaque article, `body_markdown` doit deja inclure:
  - # Titre
  - des sections H2/H3 coherentes avec la methode Le Phare
  - une section "## Reperes de sources"
  - une section "## Liens internes du dossier"
- dans "## Liens internes du dossier", utiliser une liste a puces avec les deux autres titres du meme triptyque uniquement
- ne pas inclure les blocs WordPress finaux dans `body_markdown`; ils seront ajoutes par le script

Schema cible:
{json.dumps(article_schema, ensure_ascii=False, indent=2)}
""".strip()

    raw = call_llm_json(
        llm_config=llm_config,
        system_prompt="Tu es un worker editorial de haut niveau pour Le Phare Info. Tu produis un triptyque coherent et tu renvoies uniquement du JSON valide.",
        user_prompt=prompt,
        max_tokens=max(llm_config.article_max_tokens, llm_config.article_max_tokens * len(brief.article_blueprints)),
    )
    raw_articles = raw.get("articles")
    if not isinstance(raw_articles, list) or len(raw_articles) != len(brief.article_blueprints):
        raise ValueError(f"Triptych worker {brief.triptych_id} must return exactly {len(brief.article_blueprints)} article payload(s)")

    raw_by_type = {
        sanitize_inline(str(item.get("type_code", ""))): item
        for item in raw_articles
        if isinstance(item, dict)
    }
    payloads: dict[str, dict[str, Any]] = {}
    for article_data in brief.article_blueprints:
        type_code = article_data["type_code"]
        if type_code not in raw_by_type:
            raise ValueError(f"Triptych worker {brief.triptych_id} missing payload for type {type_code}")
        payload = normalize_article_payload(raw_by_type[type_code], article_data, manifest)
        payload["worker_function"] = brief.function
        payload["worker_core_tension"] = brief.core_tension
        payload["linked_triptych_ids"] = brief.links_to_triptychs
        payload["linked_triptych_labels"] = [
            item["label"]
            for item in brief.related_triptychs
            if item["triptych_id"] in brief.links_to_triptychs
        ]
        payloads[type_code] = payload

    return payloads


def generate_articles_from_manifest(
    manifest: dict[str, Any],
    assigned_ids: list[str],
    publish_folder_name: str,
    llm_config: LlmConfig,
) -> list[PlannedArticle]:
    content_mode = manifest.get("content_mode", "triptyque")
    if content_mode == "triptyque":
        ordered_articles = sorted(
            manifest["articles"],
            key=lambda item: (
                int(item.get("triptych_order", 1)),
                TYPE_ORDER.index(item["type_code"]),
            ),
        )
        article_ids = {id(item): article_id for item, article_id in zip(ordered_articles, assigned_ids)}
    else:
        ordered_articles = sorted(
            manifest["articles"],
            key=lambda item: MINI_TYPE_ORDER.index(item["type_code"]),
        )
        article_ids = {id(item): article_id for item, article_id in zip(ordered_articles, assigned_ids)}

    generated_articles: list[PlannedArticle] = []
    triptych_ids = {
        sanitize_inline(str(article.get("triptych_id", "triptyque_1")))
        for article in ordered_articles
        if content_mode == "triptyque"
    }
    use_triptych_workers = content_mode == "triptyque" and len(triptych_ids) > 1

    if use_triptych_workers:
        # In API mode, the script can still generate one triptych block at a time.
        # Agent-first multi-triptych orchestration is handled outside this script.
        worker_briefs = build_triptych_worker_briefs(manifest, ordered_articles, article_ids)
        total_workers = len(worker_briefs)
        for worker_index, brief in enumerate(worker_briefs, start=1):
            print(
                f"Generating triptych block {worker_index}/{total_workers}: "
                f"{brief.triptych_id} [{brief.function}] {brief.triptych_label}",
                flush=True,
            )
            payloads_by_type = generate_triptych_payloads(manifest, brief, llm_config)
            for article_data in brief.article_blueprints:
                type_code = article_data["type_code"]
                article_id = article_data["article_id"]
                payload = payloads_by_type[type_code]
                print(
                    f"Consolidating worker article: {article_id} [{type_code}] {payload['title']}",
                    flush=True,
                )
                filename = build_filename(article_id, type_code, manifest["theme_code"], payload["title"])
                generated_articles.append(
                    PlannedArticle(
                        article_id=article_id,
                        triptych_id=brief.triptych_id,
                        triptych_label=brief.triptych_label,
                        triptych_order=brief.triptych_order,
                        type_code=type_code,
                        theme_code=manifest["theme_code"],
                        title=payload["title"],
                        objective=payload["objective"],
                        summary=payload["summary"],
                        keywords=payload["keywords"],
                        primary_sources=payload["primary_sources"],
                        etape_sentier=payload["etape_sentier"],
                        wp_categories=payload["wp_categories"],
                        wp_tags=payload["wp_tags"],
                        relative_folder=article_data["relative_folder"],
                        filename=filename,
                        slug=payload["slug"],
                        generated=payload,
                    )
                )
    else:
        total_articles = len(ordered_articles)
        for article_index, article_data in enumerate(ordered_articles, start=1):
            type_code = article_data["type_code"]
            article_id = article_ids[id(article_data)]
            triptych_id = sanitize_inline(str(article_data.get("triptych_id", "triptyque_1")))
            triptych_label = sanitize_inline(str(article_data.get("triptych_label", "Triptyque 1")))
            triptych_order = int(article_data.get("triptych_order", 1))
            print(
                f"Generating article {article_index}/{total_articles}: {article_id} [{type_code}] {article_data['title']}",
                flush=True,
            )
            if content_mode == "triptyque":
                sibling_candidates = [
                    item
                    for item in ordered_articles
                    if sanitize_inline(str(item.get("triptych_id", "triptyque_1"))) == triptych_id and id(item) != id(article_data)
                ]
            else:
                sibling_candidates = [item for item in ordered_articles if id(item) != id(article_data)]
            other_links = [
                {"article_id": article_ids[id(item)], "title": item["title"], "type_code": item["type_code"]}
                for item in sibling_candidates
            ]
            payload = generate_article_payload(
                manifest=manifest,
                article_data=article_data,
                article_id=article_id,
                linked_articles=other_links,
                llm_config=llm_config,
            )
            filename = build_filename(article_id, type_code, manifest["theme_code"], payload["title"])
            generated_articles.append(
                PlannedArticle(
                    article_id=article_id,
                    triptych_id=triptych_id,
                    triptych_label=triptych_label,
                    triptych_order=triptych_order,
                    type_code=type_code,
                    theme_code=manifest["theme_code"],
                    title=payload["title"],
                    objective=payload["objective"],
                    summary=payload["summary"],
                    keywords=payload["keywords"],
                    primary_sources=payload["primary_sources"],
                    etape_sentier=payload["etape_sentier"],
                    wp_categories=payload["wp_categories"],
                    wp_tags=payload["wp_tags"],
                    relative_folder=article_data["relative_folder"],
                    filename=filename,
                    slug=payload["slug"],
                    generated=payload,
                )
            )

    for article in generated_articles:
        same_triptych = [
            item
            for item in generated_articles
            if item.triptych_id == article.triptych_id and item.article_id != article.article_id
        ]
        linked_ids = [item.article_id for item in same_triptych]
        architecture_siblings = [
            item
            for item in generated_articles
            if item.triptych_id != article.triptych_id and item.article_id != article.article_id
        ]
        article.generated["linked_ids"] = linked_ids
        article.generated["linked_titles"] = [item.title for item in same_triptych]
        article.generated["architecture_related_ids"] = [item.article_id for item in architecture_siblings]
        article.generated["architecture_related_titles"] = [item.title for item in architecture_siblings]
        article.generated["triptych_id"] = article.triptych_id
        article.generated["triptych_label"] = article.triptych_label
        article.generated["triptych_order"] = article.triptych_order
        article.generated["publish_folder_name"] = publish_folder_name

    return generated_articles


def generate_article_payload(
    manifest: dict[str, Any],
    article_data: dict[str, Any],
    article_id: str,
    linked_articles: list[dict[str, str]],
    llm_config: LlmConfig,
) -> dict[str, Any]:
    article_schema = {
        "title": "string",
        "objective": "string",
        "summary": "string under 500 characters",
        "keywords": ["3-6 keywords"],
        "primary_sources": ["3-6 source names"],
        "etape_sentier": "Observer|Questionner|Comprendre|Analyser|Relier|Transmettre",
        "seo_keyword": "string",
        "meta_description": "150-160 characters target",
        "slug": "ascii-slug",
        "image_suggestion": "string",
        "image_caption": "string",
        "body_markdown": "markdown body starting with # Title and using H2/H3 sections only"
    }

    prompt = f"""
Tu dois produire UNIQUEMENT un JSON valide, sans markdown de commentaire externe.

Resume editorial Le Phare:
{build_editorial_rules_summary()}

Resume du type d'article:
{build_article_prompt_summary(article_data["type_code"])}

Cycle en cours:
- Question centrale: {manifest["cycle_question"]}
- Statut du cycle: {manifest["cycle_status"]}
- Posture active: {manifest["active_posture"]}
- Role du triptyque: {manifest["triptych_role"]}
- Sujet initial: {manifest["source_topic"]}
- Angle: {manifest.get("source_angle", manifest["angle"])}
- Theme code: {manifest["theme_code"]}
- Categorie: {manifest["category_label"]}

Article a generer:
- ID article: {article_id}
- Type: {article_data["type_code"]}
- Titre cible: {article_data["title"]}
- Objectif: {article_data["objective"]}
- Resume vise: {article_data["summary"]}
- Etape sentier ciblee: {article_data["etape_sentier"]}
- Mots-cles de depart: {", ".join(article_data["keywords"])}
- Sources a mobiliser: {", ".join(article_data["primary_sources"])}
- Categories WordPress: {", ".join(article_data["wp_categories"])}
- Tags WordPress: {", ".join(article_data["wp_tags"])}

Liens internes a mentionner dans une section "## Liens internes du dossier":
{json.dumps(linked_articles, ensure_ascii=False, indent=2)}

Contraintes de sortie:
- conserver exactement le titre cible si possible
- produire un texte de bonne qualite, publirable en brouillon WordPress
- integrer une structure claire, nuancee, non sensationnaliste
- mentionner explicitement le cycle et le Sentier dans le corps
- `body_markdown` doit deja inclure:
  - # Titre
  - des sections H2/H3 coherentes avec la methode Le Phare
  - une section "## Reperes de sources"
- si type != DOSSIER: une section "## Liens internes du dossier"
- si type != DOSSIER: dans "## Liens internes du dossier", utiliser une liste a puces avec les titres des autres articles
- si type == DOSSIER: structurer le corps comme une mini-encyclopedie en 10 grandes parties issues du prompt
- ne pas inclure les blocs WordPress finaux dans `body_markdown`; ils seront ajoutes par le script

Schema cible:
{json.dumps(article_schema, ensure_ascii=False, indent=2)}
""".strip()

    raw = call_llm_json(
        llm_config=llm_config,
        system_prompt="Tu es un redacteur de haut niveau pour Le Phare Info. Tu renvoies uniquement du JSON valide.",
        user_prompt=prompt,
        max_tokens=llm_config.article_max_tokens,
    )
    return normalize_article_payload(raw, article_data, manifest)


def normalize_article_payload(raw: dict[str, Any], article_data: dict[str, Any], manifest: dict[str, Any]) -> dict[str, Any]:
    title = sanitize_inline(str(raw.get("title") or article_data["title"]))
    objective = sanitize_inline(str(raw.get("objective") or article_data["objective"]))
    summary = sanitize_inline(str(raw.get("summary") or article_data["summary"]))
    seo_keyword = sanitize_inline(str(raw.get("seo_keyword") or title))
    meta_description = sanitize_inline(str(raw.get("meta_description") or summary[:160]))
    image_suggestion = sanitize_inline(str(raw.get("image_suggestion") or f"Illustration editoriale sobre autour de {manifest['source_topic']}"))
    image_caption = sanitize_inline(str(raw.get("image_caption") or summary))
    body_markdown = str(raw.get("body_markdown") or "").strip()
    if not body_markdown.startswith("# "):
        raise ValueError(f"Generated article body is invalid for {title}")

    return {
        "title": title,
        "objective": objective,
        "summary": summary[:500],
        "keywords": normalize_keyword_list(raw.get("keywords") or article_data["keywords"]),
        "primary_sources": normalize_keyword_list(raw.get("primary_sources") or article_data["primary_sources"]),
        "etape_sentier": sanitize_inline(str(raw.get("etape_sentier") or article_data["etape_sentier"] or manifest["active_posture"])),
        "seo_keyword": seo_keyword,
        "meta_description": meta_description[:160],
        "slug": slugify(str(raw.get("slug") or title)),
        "image_suggestion": image_suggestion,
        "image_caption": image_caption,
        "body_markdown": body_markdown.replace("\r\n", "\n"),
        "wp_categories": normalize_slug_list(article_data.get("wp_categories", [])),
        "wp_tags": normalize_slug_list(article_data.get("wp_tags", [])),
    }


def write_articles(planned_articles: list[PlannedArticle]) -> None:
    for article in planned_articles:
        absolute_folder = ROOT_DIR / article.relative_folder
        absolute_folder.mkdir(parents=True, exist_ok=True)
        absolute_path = absolute_folder / article.filename
        absolute_path.write_text(render_article_markdown(article), encoding="utf-8")


def render_article_markdown(article: PlannedArticle) -> str:
    meta = article.generated
    lines = [
        f"ID article : {article.article_id}",
        f"Triptyque ID : {article.triptych_id}",
        f"Triptyque titre : {article.triptych_label}",
        f"Triptyque ordre : {article.triptych_order}",
        f"Fonction du triptyque : {meta.get('worker_function', '')}",
        f"Tension centrale du triptyque : {meta.get('worker_core_tension', '')}",
        f"Triptyques lies : {';'.join(meta.get('linked_triptych_ids', []))}",
        f"Titre : {article.title}",
        f"Type : {article.type_code}",
        f"Theme : {article.theme_code}",
        "Statut : pret_a_publier",
        "Version : V1",
        f"Date de creation : {_today_iso()}",
        f"Date de derniere mise a jour : {_today_iso()}",
        "Auteur : Le Phare Info",
        f"Etape du Sentier liee : {meta['etape_sentier']}",
        f"Articles lies (IDs) : {';'.join(meta['linked_ids'])}",
        f"Mots-cles : {','.join(meta['keywords'])}",
        f"Resume court (500 caracteres max) : {meta['summary']}",
        f"Objectif de l'article : {meta['objective']}",
        f"Sources principales : {', '.join(meta['primary_sources'])}",
        "URL WordPress (si publie) : ",
        "",
        "# SEO",
        f"Mot-cle principal : {meta['seo_keyword']}",
        f"Meta-description : {meta['meta_description']}",
        "",
        "---",
        "",
        meta["body_markdown"].strip(),
        "",
        "## Bloc image WordPress",
        f"Suggestion image : {meta['image_suggestion']}",
        f"Legende proposee : {meta['image_caption']}",
        "",
        "## Bloc publication",
        "Statut publication : pret_a_publier",
        f"Date cible publication : {_today_iso()}",
        f"Slug propose : {article.slug}",
        "",
    ]
    return "\n".join(lines)


def duplicate_to_publish_folder(planned_articles: list[PlannedArticle], publish_folder_name: str) -> Path:
    publish_dir = PUBLISH_DIR_ROOT / publish_folder_name
    publish_dir.mkdir(parents=True, exist_ok=True)
    multiple_triptychs = len({article.triptych_id for article in planned_articles}) > 1
    for article in planned_articles:
        source = ROOT_DIR / article.relative_folder / article.filename
        if multiple_triptychs:
            triptych_folder = publish_dir / f"{article.triptych_order:02d}_{slugify(article.triptych_label)[:50] or article.triptych_id}"
            triptych_folder.mkdir(parents=True, exist_ok=True)
            target = triptych_folder / article.filename
        else:
            target = publish_dir / article.filename
        shutil.copy2(source, target)
    return publish_dir


def append_rows_to_index(index_path: Path, planned_articles: list[PlannedArticle]) -> None:
    if not index_path.exists():
        raise FileNotFoundError(f"Index file not found: {index_path}")

    with index_path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        fieldnames = reader.fieldnames or []

    existing_ids = {row.get("ID", "").strip() for row in rows}
    new_rows = []
    for article in planned_articles:
        if article.article_id in existing_ids:
            raise ValueError(f"Article ID already exists in index: {article.article_id}")
        new_rows.append(build_index_row(article))

    with index_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows + new_rows)


def build_index_row(article: PlannedArticle) -> dict[str, str]:
    return {
        "ID": article.article_id,
        "Titre": article.title,
        "Type": article.type_code,
        "Theme": article.theme_code,
        "Statut": "pret_a_publier",
        "Version": "V1",
        "Date_creation": _today_iso(),
        "Date_derniere_maj": _today_iso(),
        "Auteur": "Le Phare Info",
        "Etape_sentier": article.etape_sentier,
        "Articles_lies": ";".join(article.generated["linked_ids"]),
        "Mots_cles": ";".join(article.keywords),
        "Resume_court": article.summary,
        "Objectif": article.objective,
        "Nom_fichier": article.filename,
        "Chemin_dossier": article.relative_folder,
        "Date_publication_WP": "",
        "URL_WordPress": "",
        "Slug_WordPress": article.slug,
        "Categorie_WP": ";".join(article.wp_categories),
        "Tags_WP": ";".join(article.wp_tags),
        "Remarques": f"Genere via editorial_pipeline.py | {article.generated['publish_folder_name']}",
    }


def push_to_wordpress_drafts(publish_dir: Path, index_path: Path, wp_config_path: Path) -> None:
    command = [
        sys.executable,
        str(TOOLS_DIR / "wp_push_draft.py"),
        str(publish_dir),
        "--config",
        str(wp_config_path),
        "--index",
        str(index_path),
    ]
    result = subprocess.run(command, cwd=str(ROOT_DIR), capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "wp_push_draft.py failed")


def build_filename(article_id: str, type_code: str, theme_code: str, title: str) -> str:
    short_title = slugify(title).replace("-", "_")
    return f"{article_id}_{type_code}_{theme_code}_{short_title[:90]}_V1.md"


def call_llm_json(llm_config: LlmConfig, system_prompt: str, user_prompt: str, max_tokens: int | None = None) -> dict[str, Any]:
    endpoint = f"{llm_config.base_url}/chat/completions"
    payload = {
        "model": llm_config.model,
        "temperature": llm_config.temperature,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }
    if max_tokens:
        payload["max_tokens"] = max_tokens
    req = request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {llm_config.api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=llm_config.request_timeout_seconds) as response:
            data = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"LLM API error {exc.code}: {detail}") from exc
    except (error.URLError, TimeoutError, socket.timeout) as exc:
        raise RuntimeError(
            f"LLM request failed or timed out after {llm_config.request_timeout_seconds}s: {exc}"
        ) from exc

    content = data["choices"][0]["message"]["content"]
    return parse_llm_json_content(content, llm_config)


def extract_json_block(content: str) -> str:
    stripped = content.strip()
    if stripped.startswith("{") or stripped.startswith("["):
        return stripped
    fenced = re.search(r"```(?:json)?\s*(\{.*\}|\[.*\])\s*```", stripped, flags=re.DOTALL)
    if fenced:
        return fenced.group(1)
    raise ValueError("LLM response does not contain valid JSON")


def parse_llm_json_content(content: str, llm_config: LlmConfig) -> dict[str, Any]:
    raw_json = extract_json_block(content)
    try:
        return json.loads(raw_json)
    except json.JSONDecodeError:
        repaired = repair_json_control_characters(raw_json)
        try:
            return json.loads(repaired)
        except json.JSONDecodeError:
            cleaned = repair_json_with_llm(repaired, llm_config)
            return json.loads(cleaned)


def repair_json_control_characters(raw_json: str) -> str:
    repaired: list[str] = []
    in_string = False
    escaped = False

    for char in raw_json:
        if in_string:
            if escaped:
                repaired.append(char)
                escaped = False
                continue

            if char == "\\":
                repaired.append(char)
                escaped = True
                continue

            if char == '"':
                repaired.append(char)
                in_string = False
                continue

            codepoint = ord(char)
            if char == "\n":
                repaired.append("\\n")
                continue
            if char == "\r":
                repaired.append("\\r")
                continue
            if char == "\t":
                repaired.append("\\t")
                continue
            if codepoint < 32:
                repaired.append(" ")
                continue

            repaired.append(char)
            continue

        repaired.append(char)
        if char == '"':
            in_string = True

    return "".join(repaired)


def repair_json_with_llm(raw_json: str, llm_config: LlmConfig) -> str:
    prompt = f"""
Fix the following invalid JSON.

Rules:
- Return ONLY valid JSON
- Keep the original meaning and fields
- Do not add commentary
- Escape quotes and control characters correctly

Broken JSON:
{raw_json}
""".strip()

    endpoint = f"{llm_config.base_url}/chat/completions"
    payload = {
        "model": llm_config.model,
        "temperature": 0,
        "messages": [
            {"role": "system", "content": "You repair invalid JSON and return only valid JSON."},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": llm_config.repair_max_tokens,
    }
    req = request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {llm_config.api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=llm_config.request_timeout_seconds) as response:
            data = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"LLM JSON repair error {exc.code}: {detail}") from exc
    except (error.URLError, TimeoutError, socket.timeout) as exc:
        raise RuntimeError(
            f"LLM JSON repair request failed or timed out after {llm_config.request_timeout_seconds}s: {exc}"
        ) from exc

    return extract_json_block(data["choices"][0]["message"]["content"])


def sanitize_inline(value: str) -> str:
    return " ".join(value.replace("\r", " ").replace("\n", " ").split()).strip()


def slugify(value: str) -> str:
    ascii_value = value.lower()
    replacements = {
        "a": "àáâäãå",
        "c": "ç",
        "e": "èéêë",
        "i": "ìíîï",
        "n": "ñ",
        "o": "òóôöõ",
        "u": "ùúûü",
        "y": "ýÿ",
        "ae": "æ",
        "oe": "œ",
    }
    for replacement, chars in replacements.items():
        for char in chars:
            ascii_value = ascii_value.replace(char, replacement)
    ascii_value = re.sub(r"[^a-z0-9]+", "-", ascii_value)
    ascii_value = re.sub(r"-{2,}", "-", ascii_value)
    return ascii_value.strip("-")


def unique_preserve_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        if value not in seen:
            ordered.append(value)
            seen.add(value)
    return ordered


def _today_iso() -> str:
    return date.today().isoformat()


if __name__ == "__main__":
    raise SystemExit(main())
