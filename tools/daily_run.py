#!/usr/bin/env python3
"""
Daily Le Phare routine.

V2 (routine quotidienne V2):
- garde-fou amélioré : bloque uniquement si statut = "success" ET topic identique ; affiche
  conseil --force explicite dans le log quand le run du jour est déjà réussi.
- ajout de 'parent_refresh_reminder' dans le JSON de run : chemin canonique du SENTIER atelier
  publié + rappel de rafraîchir le fondamental parent sur WP (étape manuelle).
- extraction du SENTIER canonical path depuis linking_stdout pour alimenter le reminder.

Behavior:
- default (assistant-first): RSS topic suggestion + reminder (assistant workflow below)
- --publish-existing DIR (assistant triptych already under 07_A_Publier):
  sequential by default: wp_push_draft.py then post_linking.py (WP drafts + maillage + publication).
  Optional --seo-enrich-after-link: after successful post_linking, run post_seo_enrich.py (API, Rank Math / body)
  then wp_push --refresh-body per article; requires seo_enrich_api_enabled + api_key in editorial_config.
  Use --no-publish-final to keep drafts after linking. Use --wp-push-only to skip post_linking;
  use --skip-wp-push for a second pass (refresh content / linking only).
  Use --sync-featured-media / --refresh-body with --publish-existing for PATCH-only (image mise en avant, corps HTML depuis les .md, sans nouveaux posts).
  After a full successful run (WP push + post_linking when applicable), the triptych staging
  subfolder under 07_A_Publier is removed by default; use --keep-publish-folder to retain it.
  Staging is kept after --wp-push-only or --no-publish-drafts (incomplete / local-only paths).
- with --use-api-llm: editorial_pipeline.py (requires LLM API config)
- log each run to 00_Systeme/Logs
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any
from urllib import error, request
from xml.etree import ElementTree


ROOT_DIR = Path(__file__).resolve().parent.parent
TOOLS_DIR = ROOT_DIR / "tools"
SYSTEM_DIR = ROOT_DIR / "00_Systeme"
MANIFESTS_DIR = SYSTEM_DIR / "Manifests"
LOGS_DIR = SYSTEM_DIR / "Logs"
PIPELINE_PATH = TOOLS_DIR / "editorial_pipeline.py"
POST_LINKING_PATH = TOOLS_DIR / "post_linking.py"
POST_SEO_ENRICH_PATH = TOOLS_DIR / "post_seo_enrich.py"
WP_PUSH_PATH = TOOLS_DIR / "wp_push_draft.py"
EDITORIAL_CONFIG = TOOLS_DIR / "editorial_config.local.json"
WP_CONFIG = TOOLS_DIR / "wp_config.local.json"
INDEX_PATH = ROOT_DIR / "index_editorial.csv"
PUBLISH_ROOT = ROOT_DIR / "07_A_Publier"

GOOGLE_NEWS_RSS = "https://news.google.com/rss?hl=fr&gl=FR&ceid=FR:fr"
CONTENT_MODES = ("architecture_editoriale", "triptyque", "mini_encyclopedie")
OUTPUT_PROFILES = ("triptyque_minimal", "dossier_2_triptyques", "dossier_3_triptyques", "reseau_5_contenus")

POSITIVE_KEYWORDS = {
    "MONDE": ("guerre", "iran", "israel", "ukraine", "chine", "taiwan", "otan", "diplomatie", "conflit"),
    "POL": ("election", "parlement", "gouvernement", "loi", "societe", "immigration", "justice", "manifestation"),
    "ECON": ("inflation", "economie", "taux", "bce", "banque", "budget", "emploi", "commerce", "petrole"),
    "TECH": ("ia", "intelligence artificielle", "openai", "google", "microsoft", "meta", "semi-conducteur", "cyber"),
    "CLIMAT": ("climat", "canicule", "incendie", "inondation", "cop", "emissions", "secheresse", "biodiversite"),
    "SCIENCE": ("science", "sante", "vaccin", "recherche", "medical", "hopital", "etude", "espace"),
}

NEGATIVE_KEYWORDS = (
    "football",
    "mercato",
    "ligue 1",
    "nba",
    "tennis",
    "people",
    "celebrite",
    "mode",
    "television",
    "serie",
    "cinema",
    "horoscope",
    "recette",
)


@dataclass
class CandidateTopic:
    title: str
    source: str
    link: str
    summary: str
    theme_code: str
    score: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Le Phare daily editorial routine.")
    parser.add_argument("--topic", help="Manual topic override")
    parser.add_argument("--mode", choices=CONTENT_MODES, default="architecture_editoriale", help="Editorial generation mode")
    parser.add_argument("--output-profile", choices=OUTPUT_PROFILES, default="triptyque_minimal", help="Requested editorial output profile")
    parser.add_argument("--theme", help="Optional theme override for the pipeline")
    parser.add_argument("--angle", help="Optional editorial angle override")
    parser.add_argument("--config", default=str(EDITORIAL_CONFIG), help="Path to editorial config JSON")
    parser.add_argument("--wp-config", default=str(WP_CONFIG), help="Path to WordPress config JSON")
    parser.add_argument("--index", default=str(INDEX_PATH), help="Path to index_editorial.csv")
    parser.add_argument("--no-publish-drafts", action="store_true", help="Generate locally but do not push WordPress drafts")
    parser.add_argument(
        "--no-publish-final",
        action="store_true",
        help="After post_linking, keep WordPress posts as drafts instead of publishing",
    )
    parser.add_argument("--force", action="store_true", help="Run even if today's routine already succeeded")
    parser.add_argument(
        "--publish-existing",
        metavar="DIR",
        help="Triptych folder under 07_A_Publier: push WP drafts then post_linking (sequential by default)",
    )
    parser.add_argument(
        "--skip-wp-push",
        action="store_true",
        help="With --publish-existing: only post_linking (WP posts already exist; second pass after local edits)",
    )
    parser.add_argument(
        "--wp-push-only",
        action="store_true",
        help="With --publish-existing: only wp_push_draft, skip post_linking",
    )
    parser.add_argument(
        "--sync-featured-media",
        action="store_true",
        help="With --publish-existing: wp_push_draft --sync-featured-media only (PATCH image mise en avant depuis l index, sans recréer les posts)",
    )
    parser.add_argument(
        "--refresh-body",
        action="store_true",
        help="With --publish-existing: wp_push_draft --refresh-body (PATCH contenu HTML depuis les markdown + Rank Math)",
    )
    parser.add_argument(
        "--keep-publish-folder",
        action="store_true",
        help="With --publish-existing: after success, keep the triptych staging folder under 07_A_Publier (default is to remove it when the full assisted workflow succeeded)",
    )
    parser.add_argument(
        "--cleanup-publish-folder",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--publish-final",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--use-api-llm",
        action="store_true",
        help="Generate manifest and articles via editorial_pipeline.py + external LLM API (requires api_key in config)",
    )
    parser.add_argument(
        "--seo-enrich-after-link",
        action="store_true",
        help="With --publish-existing: après post_linking réussi, appeler post_seo_enrich.py (API) puis refresh WP ; "
        "exige seo_enrich_api_enabled + api_key dans editorial_config (voir tools/editorial_config.example.json)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    state_path = LOGS_DIR / f"daily_run_{today_iso()}.json"
    log_path = LOGS_DIR / f"daily_run_{today_iso()}.log"

    if state_path.exists() and not args.force:
        existing = json.loads(state_path.read_text(encoding="utf-8"))
        if existing.get("status") == "success":
            topic_done = existing.get("topic", "")
            msg = (
                f"Routine quotidienne déjà réussie aujourd'hui (sujet : {topic_done}). "
                f"Relancer avec --force pour un second triptyque ou une correction."
            )
            write_log(log_path, msg)
            print(msg)
            return 0
        else:
            write_log(
                log_path,
                f"Statut précédent : {existing.get('status')} — relance autorisée sans --force.",
            )

    if args.publish_existing and args.use_api_llm:
        print("Utilisez soit --publish-existing (triptyque deja redige), soit --use-api-llm, pas les deux.", file=sys.stderr)
        return 2

    if args.skip_wp_push and not args.publish_existing:
        print("Erreur: --skip-wp-push requiert --publish-existing DIR.", file=sys.stderr)
        return 2
    if args.wp_push_only and not args.publish_existing:
        print("Erreur: --wp-push-only requiert --publish-existing DIR.", file=sys.stderr)
        return 2
    if args.sync_featured_media and not args.publish_existing:
        print("Erreur: --sync-featured-media requiert --publish-existing DIR.", file=sys.stderr)
        return 2
    if args.refresh_body and not args.publish_existing:
        print("Erreur: --refresh-body requiert --publish-existing DIR.", file=sys.stderr)
        return 2
    if args.refresh_body and args.skip_wp_push:
        print("Erreur: --refresh-body est incompatible avec --skip-wp-push.", file=sys.stderr)
        return 2
    if args.sync_featured_media and args.skip_wp_push:
        print("Erreur: --sync-featured-media est incompatible avec --skip-wp-push.", file=sys.stderr)
        return 2
    if args.skip_wp_push and args.wp_push_only:
        print("Erreur: ne pas combiner --skip-wp-push et --wp-push-only.", file=sys.stderr)
        return 2
    if args.seo_enrich_after_link and args.wp_push_only:
        print("Erreur: --seo-enrich-after-link est incompatible avec --wp-push-only (maillage requis avant enrichissement).", file=sys.stderr)
        return 2
    if args.skip_wp_push and args.no_publish_drafts:
        print("Erreur: --skip-wp-push avec --no-publish-drafts est incoherent.", file=sys.stderr)
        return 2
    if args.keep_publish_folder and not args.publish_existing:
        print("Erreur: --keep-publish-folder requiert --publish-existing DIR.", file=sys.stderr)
        return 2
    if args.seo_enrich_after_link and not args.publish_existing:
        print("Erreur: --seo-enrich-after-link requiert --publish-existing DIR.", file=sys.stderr)
        return 2
    if args.cleanup_publish_folder and args.publish_existing:
        write_log(
            log_path,
            "Note: --cleanup-publish-folder est deprece (nettoyage par defaut); utilisez --keep-publish-folder pour garder le staging sous 07_A_Publier.",
        )

    try:
        linking_stdout = ""
        linking_stderr = ""
        failure_message = ""
        publish_dir: Path | None = None
        result: subprocess.CompletedProcess[str]
        linking_executed = False
        seo_phase_ok = True

        if args.publish_existing:
            publish_dir = resolve_publish_existing(args.publish_existing)
            topic = args.topic or publish_dir.name
            theme = args.theme or ""
            source = "agent_written"
            source_link = ""
            write_log(log_path, f"Publish-existing folder: {publish_dir}")
            write_log(log_path, f"Selected topic label: {topic}")
            if theme:
                write_log(log_path, f"Theme: {theme}")

            synthetic_stdout = f"Triptych generated locally in: {publish_dir}\n"

            if args.no_publish_drafts:
                result = subprocess.CompletedProcess(
                    ["publish-existing"],
                    0,
                    stdout=synthetic_stdout,
                    stderr="",
                )
                overall_returncode = 0
            elif args.skip_wp_push:
                result = subprocess.CompletedProcess(
                    ["publish-existing", "skip-wp-push"],
                    0,
                    stdout=synthetic_stdout,
                    stderr="",
                )
                overall_returncode = 0
            else:
                wp_command = build_wp_push_command(
                    publish_dir=publish_dir,
                    wp_config_path=Path(args.wp_config),
                    index_path=Path(args.index),
                    sync_featured_media=args.sync_featured_media,
                    refresh_body=args.refresh_body,
                )
                write_log(log_path, f"Running command: {' '.join(wp_command)}")
                result = run_logged_command(wp_command, log_path, "WP-PUSH")
                overall_returncode = result.returncode

            run_linking = (
                should_run_triptych_linking(args.mode, args.output_profile)
                and not args.no_publish_drafts
                and overall_returncode == 0
                and (args.skip_wp_push or not args.wp_push_only)
            )
            if run_linking:
                linking_command = build_post_linking_command(
                    triptych_dir=publish_dir,
                    index_path=Path(args.index),
                    wp_config_path=Path(args.wp_config),
                    publish_final=assisted_linking_publish_final(args),
                )
                write_log(log_path, f"Running post-linking command: {' '.join(linking_command)}")
                linking_result = run_logged_command(linking_command, log_path, "POST-LINKING")
                linking_stdout = linking_result.stdout
                linking_stderr = linking_result.stderr
                if linking_result.returncode != 0:
                    overall_returncode = linking_result.returncode
                    failure_message = linking_stderr.strip() or linking_stdout.strip() or "Post-linking failed"

            linking_executed = run_linking and overall_returncode == 0

            if (
                getattr(args, "seo_enrich_after_link", False)
                and publish_dir is not None
                and linking_executed
                and overall_returncode == 0
            ):
                cfg_path = Path(args.config)
                if not editorial_seo_enrich_api_enabled(cfg_path):
                    write_log(
                        log_path,
                        "SEO enrich: option --seo-enrich-after-link ignoree (activer seo_enrich_api_enabled + api_key dans editorial_config.local.json).",
                    )
                else:
                    article_ids = extract_article_ids_from_triptych_dir(publish_dir)
                    if len(article_ids) != 3:
                        write_log(
                            log_path,
                            f"SEO enrich: ignore (IDs detectes dans le dossier: {article_ids!r}, attendu 3).",
                        )
                    else:
                        enrich_cmd = build_post_seo_enrich_command(
                            article_ids=article_ids,
                            editorial_config=cfg_path,
                            wp_config=Path(args.wp_config),
                            index_path=Path(args.index),
                        )
                        write_log(log_path, f"Running command: {' '.join(enrich_cmd)}")
                        enrich_result = run_logged_command(enrich_cmd, log_path, "POST-SEO-ENRICH")
                        if enrich_result.returncode != 0:
                            overall_returncode = enrich_result.returncode
                            failure_message = (
                                enrich_result.stdout.strip() or "post_seo_enrich.py failed"
                            )
                            seo_phase_ok = False
                        else:
                            seo_phase_ok = True

        elif args.use_api_llm:
            if args.topic:
                topic = args.topic
                theme = args.theme or ""
                source = "manual"
                source_link = ""
            else:
                candidate = choose_topic_of_the_day()
                topic = candidate.title
                theme = args.theme or candidate.theme_code
                source = candidate.source
                source_link = candidate.link

            write_log(log_path, f"Selected topic: {topic}")
            if source_link:
                write_log(log_path, f"Source: {source} | {source_link}")
            if theme:
                write_log(log_path, f"Theme: {theme}")

            command = build_pipeline_command(
                topic=topic,
                mode=args.mode,
                output_profile=args.output_profile,
                theme=theme,
                angle=args.angle or "",
                config_path=Path(args.config),
                wp_config_path=Path(args.wp_config),
                index_path=Path(args.index),
                publish_drafts=not args.no_publish_drafts,
                use_api_llm=True,
            )
            write_log(log_path, f"Running command: {' '.join(command)}")
            result = run_logged_command(command, log_path, "PIPELINE")

            publish_dir = extract_publish_dir(result.stdout)
            overall_returncode = result.returncode
            if result.returncode == 0 and should_run_triptych_linking(args.mode, args.output_profile) and not args.no_publish_drafts:
                if not publish_dir:
                    raise RuntimeError("Unable to locate triptych publish directory from pipeline output")
                linking_command = build_post_linking_command(
                    triptych_dir=publish_dir,
                    index_path=Path(args.index),
                    wp_config_path=Path(args.wp_config),
                    publish_final=not args.no_publish_final,
                )
                write_log(log_path, f"Running post-linking command: {' '.join(linking_command)}")
                linking_result = run_logged_command(linking_command, log_path, "POST-LINKING")
                linking_stdout = linking_result.stdout
                linking_stderr = linking_result.stderr

                if linking_result.returncode != 0:
                    overall_returncode = linking_result.returncode
                    failure_message = linking_stderr.strip() or linking_stdout.strip() or "Post-linking failed"

        else:
            suggestion = ""
            try:
                candidate = choose_topic_of_the_day()
                suggestion = (
                    f"Sujet du jour (suggestion pour la redaction assistee dans Cursor) :\n"
                    f"  {candidate.title}\n"
                    f"  Source : {candidate.source}\n"
                    f"  Lien : {candidate.link}\n"
                )
            except Exception as exc:
                suggestion = f"(Impossible de suggerer un sujet via flux RSS : {exc})\n"

            msg = (
                f"{suggestion}\n"
                "Routine quotidienne (assistant Cursor) : rediger le triptyque, copier sous 07_A_Publier, puis UNE commande :\n\n"
                '  python tools/daily_run.py --publish-existing "07_A_Publier/<dossier_triptyque>"\n\n'
                "  -> enchaine automatiquement : brouillons WordPress + post_linking + publication en ligne,\n"
                "     puis suppression du sous-dossier triptyque dans 07_A_Publier apres succes complet.\n"
                "  Verifier les trois articles sur le site (ou en admin). Ajoutez --force si la meme journee bloque un nouvel essai.\n\n"
                "Options utiles :\n"
                "  --keep-publish-folder      conserver le dossier sous 07_A_Publier apres succes\n"
                "  --no-publish-final       garder les brouillons apres le maillage (ne pas publier)\n"
                "  --wp-push-only             seulement creer/mettre a jour les brouillons WP (sans post_linking)\n"
                "  --skip-wp-push             seulement post_linking (apres retouches locales des .md)\n"
                "  --seo-enrich-after-link    apres maillage : passe API post_seo_enrich (Rank Math / contenu) puis refresh WP ; "
                "exige seo_enrich_api_enabled + api_key dans tools/editorial_config.local.json\n\n"
                "Generation technique par API : python tools/daily_run.py --use-api-llm\n"
            )
            print(msg, file=sys.stderr)
            return 2

        status = "success" if overall_returncode == 0 else "error"
        parent_refresh_reminder = _build_parent_refresh_reminder(
            linking_stdout=linking_stdout,
            index_path=Path(args.index),
            success=(overall_returncode == 0 and linking_executed),
        )
        state_payload = {
            "date": today_iso(),
            "status": status,
            "topic": topic,
            "theme": theme,
            "source": source,
            "source_link": source_link,
            "publish_drafts": not args.no_publish_drafts,
            "publish_dir": str(publish_dir) if publish_dir else "",
            "stdout": result.stdout,
            "stderr": result.stderr,
            "linking_stdout": linking_stdout,
            "linking_stderr": linking_stderr,
            "returncode": overall_returncode,
            "workflow": "publish_existing" if args.publish_existing else "api_pipeline",
            "completed_at": datetime.now().isoformat(timespec="seconds"),
            "seo_enrich_after_link": getattr(args, "seo_enrich_after_link", False),
            "seo_phase_ok": seo_phase_ok,
            "parent_refresh_reminder": parent_refresh_reminder,
        }
        state_path.write_text(json.dumps(state_payload, ensure_ascii=False, indent=2), encoding="utf-8")
        if parent_refresh_reminder.get("needed"):
            write_log(
                log_path,
                f"[V2] Rappel fondamental parent : {parent_refresh_reminder.get('parent_fundamental')} — "
                f"rafraîchir WP manuellement pour afficher ## Ateliers.",
            )

        if overall_returncode != 0:
            print(failure_message or result.stderr.strip() or result.stdout.strip() or "Daily routine failed")
            return overall_returncode

        if (
            args.publish_existing
            and publish_dir is not None
            and overall_returncode == 0
            and should_remove_publish_staging_after_success(
                args, linking_executed, seo_phase_ok=seo_phase_ok
            )
        ):
            try:
                safe_remove_publish_staging_folder(publish_dir, log_path)
            except ValueError as exc:
                write_log(log_path, f"Cleanup refused: {exc}")
                print(f"Avertissement: {exc}", file=sys.stderr)
            except OSError as exc:
                write_log(log_path, f"Cleanup failed: {exc}")
                print(f"Avertissement: nettoyage incomplet : {exc}", file=sys.stderr)

        print(f"Daily routine completed for topic: {topic}")
        return 0
    except Exception as exc:
        write_log(log_path, f"Unhandled error: {exc}")
        state_path.write_text(
            json.dumps(
                {
                    "date": today_iso(),
                    "status": "error",
                    "topic": args.topic or "",
                    "error": str(exc),
                    "completed_at": datetime.now().isoformat(timespec="seconds"),
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        print(f"Daily routine error: {exc}", file=sys.stderr)
        return 1


def build_pipeline_command(
    topic: str,
    mode: str,
    output_profile: str,
    theme: str,
    angle: str,
    config_path: Path,
    wp_config_path: Path,
    index_path: Path,
    publish_drafts: bool,
    use_api_llm: bool,
) -> list[str]:
    command = [
        sys.executable,
        str(PIPELINE_PATH),
        topic,
        "--mode",
        mode,
        "--output-profile",
        output_profile,
        "--config",
        str(config_path),
        "--index",
        str(index_path),
    ]
    if use_api_llm:
        command.append("--use-api-llm")
    if theme:
        command.extend(["--theme", theme])
    if angle:
        command.extend(["--angle", angle])
    if publish_drafts:
        command.extend(["--publish-drafts", "--wp-config", str(wp_config_path)])
    return command


def editorial_seo_enrich_api_enabled(config_path: Path) -> bool:
    """True when post_seo_enrich.py is allowed to call a paid API (explicit gate + key)."""
    try:
        raw = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return bool(raw.get("seo_enrich_api_enabled")) and bool(str(raw.get("api_key", "")).strip())


def extract_article_ids_from_triptych_dir(publish_dir: Path) -> list[str]:
    ids: list[str] = []
    for md in sorted(publish_dir.glob("*.md")):
        text = md.read_text(encoding="utf-8")
        for line in text.splitlines()[:60]:
            m = re.match(r"^ID article\s*:\s*(\S+)", line.strip(), re.IGNORECASE)
            if m:
                ids.append(m.group(1).strip())
                break
    return ids


def build_post_seo_enrich_command(
    *,
    article_ids: list[str],
    editorial_config: Path,
    wp_config: Path,
    index_path: Path,
) -> list[str]:
    return [
        sys.executable,
        str(POST_SEO_ENRICH_PATH),
        "--article-ids",
        ",".join(article_ids),
        "--editorial-config",
        str(editorial_config),
        "--wp-config",
        str(wp_config),
        "--index",
        str(index_path),
    ]


def should_remove_publish_staging_after_success(
    args: argparse.Namespace, linking_executed: bool, *, seo_phase_ok: bool = True
) -> bool:
    """Remove staging under 07_A_Publier after full success unless user opts out or run was incomplete."""
    if args.keep_publish_folder:
        return False
    if args.no_publish_drafts:
        return False
    if args.wp_push_only:
        return False
    if getattr(args, "seo_enrich_after_link", False) and editorial_seo_enrich_api_enabled(Path(args.config)):
        if not seo_phase_ok:
            return False
    return linking_executed


def safe_remove_publish_staging_folder(publish_dir: Path, log_path: Path) -> None:
    """Remove a triptych staging directory under 07_A_Publier only (never the queue root)."""
    resolved = publish_dir.resolve()
    root = PUBLISH_ROOT.resolve()
    if resolved == root:
        raise ValueError("Suppression refusee : ne pas effacer la racine 07_A_Publier.")
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"Suppression refusee : le dossier doit etre sous 07_A_Publier ({resolved}).") from exc
    if resolved.exists():
        shutil.rmtree(resolved)
        write_log(log_path, f"Staging folder removed: {resolved}")


def resolve_publish_existing(raw: str) -> Path:
    path = Path(raw)
    if not path.is_absolute():
        path = (ROOT_DIR / path).resolve()
    else:
        path = path.resolve()
    if not path.exists():
        raise ValueError(f"Dossier introuvable : {path}")
    return path


def assisted_linking_publish_final(args: argparse.Namespace) -> bool:
    """WordPress status after post_linking for --publish-existing (mirrors API pipeline: publish unless --no-publish-final)."""
    return not args.no_publish_final


def build_wp_push_command(
    publish_dir: Path,
    wp_config_path: Path,
    index_path: Path,
    *,
    sync_featured_media: bool = False,
    refresh_body: bool = False,
) -> list[str]:
    cmd = [
        sys.executable,
        str(WP_PUSH_PATH),
        str(publish_dir),
        "--config",
        str(wp_config_path),
        "--index",
        str(index_path),
    ]
    if sync_featured_media:
        cmd.append("--sync-featured-media")
    if refresh_body:
        cmd.append("--refresh-body")
    return cmd


def should_run_triptych_linking(mode: str, output_profile: str) -> bool:
    if mode == "triptyque":
        return True
    if mode == "architecture_editoriale":
        return output_profile == "triptyque_minimal"
    return False


def build_post_linking_command(
    triptych_dir: Path,
    index_path: Path,
    wp_config_path: Path,
    *,
    publish_final: bool = True,
) -> list[str]:
    command = [
        sys.executable,
        str(POST_LINKING_PATH),
        str(triptych_dir),
        "--index",
        str(index_path),
        "--config",
        str(wp_config_path),
    ]
    if publish_final:
        command.append("--publish-final")
    return command


def extract_publish_dir(stdout: str) -> Path | None:
    matches = re.findall(r"(?:WordPress drafts pushed from|Triptych generated locally in):\s*(.+)", stdout)
    if not matches:
        return None
    return Path(matches[-1].strip())


def run_logged_command(command: list[str], log_path: Path, label: str) -> subprocess.CompletedProcess[str]:
    write_log(log_path, f"--- {label} OUTPUT ---")
    process = subprocess.Popen(
        command,
        cwd=str(ROOT_DIR),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        bufsize=1,
    )
    collected_lines: list[str] = []
    assert process.stdout is not None
    for line in process.stdout:
        cleaned = line.rstrip()
        collected_lines.append(line)
        if cleaned:
            write_log(log_path, cleaned)
    returncode = process.wait()
    stdout = "".join(collected_lines)
    return subprocess.CompletedProcess(command, returncode, stdout=stdout, stderr="")


def choose_topic_of_the_day() -> CandidateTopic:
    items = fetch_google_news_topics()
    if not items:
        raise RuntimeError("No news topics could be fetched from RSS")

    recent_topics = load_recent_topics()
    for item in items:
        if normalize_text(item.title) not in recent_topics:
            return item
    return items[0]


def fetch_google_news_topics() -> list[CandidateTopic]:
    try:
        with request.urlopen(GOOGLE_NEWS_RSS) as response:
            xml_text = response.read().decode("utf-8", errors="replace")
    except error.URLError as exc:
        raise RuntimeError(f"Unable to fetch Google News RSS: {exc}") from exc

    root = ElementTree.fromstring(xml_text)
    candidates: list[CandidateTopic] = []
    for item in root.findall(".//item"):
        title = text_or_empty(item.findtext("title"))
        link = text_or_empty(item.findtext("link"))
        description = strip_html(text_or_empty(item.findtext("description")))
        clean_title, source = split_title_and_source(title)
        if not clean_title:
            continue
        scored = score_candidate(clean_title, description)
        if scored is None:
            continue
        theme_code, score = scored
        candidates.append(
            CandidateTopic(
                title=clean_title,
                source=source,
                link=link,
                summary=description,
                theme_code=theme_code,
                score=score,
            )
        )

    candidates.sort(key=lambda item: item.score, reverse=True)
    return candidates[:10]


def split_title_and_source(title: str) -> tuple[str, str]:
    parts = [part.strip() for part in title.rsplit(" - ", 1)]
    if len(parts) == 2:
        return parts[0], parts[1]
    return title.strip(), ""


def score_candidate(title: str, description: str) -> tuple[str, int] | None:
    haystack = normalize_text(f"{title} {description}")
    if any(keyword in haystack for keyword in NEGATIVE_KEYWORDS):
        return None

    best_theme = ""
    best_score = 0
    for theme_code, keywords in POSITIVE_KEYWORDS.items():
        score = sum(4 for keyword in keywords if keyword in haystack)
        if any(word in haystack for word in ("analyse", "crise", "guerre", "tension", "strategie", "politique")):
            score += 2
        if score > best_score:
            best_score = score
            best_theme = theme_code

    if best_score == 0:
        return None
    return best_theme, best_score


def load_recent_topics() -> set[str]:
    recent: set[str] = set()
    manifests = sorted(MANIFESTS_DIR.glob("*.json"), key=lambda path: path.stat().st_mtime, reverse=True)[:20]
    for manifest in manifests:
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        except Exception:
            continue
        topic = text_or_empty(data.get("source_topic", ""))
        if topic:
            recent.add(normalize_text(topic))
    return recent


def write_log(path: Path, message: str) -> None:
    timestamp = datetime.now().isoformat(timespec="seconds")
    with path.open("a", encoding="utf-8") as fh:
        fh.write(f"[{timestamp}] {message}\n")


def normalize_text(value: str) -> str:
    lowered = value.lower()
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
            lowered = lowered.replace(char, replacement)
    lowered = re.sub(r"\s+", " ", lowered)
    return lowered.strip()


def strip_html(value: str) -> str:
    return re.sub(r"<[^>]+>", " ", value)


def text_or_empty(value: Any) -> str:
    return str(value or "").strip()


def today_iso() -> str:
    return date.today().isoformat()


def _build_parent_refresh_reminder(
    linking_stdout: str,
    index_path: Path,
    success: bool,
) -> dict:
    """Build a reminder dict for the parent fundamental WP refresh (V2).

    After a SENTIER atelier is published, the parent fundamental's ## Ateliers section
    must be manually refreshed on WordPress so it appears on the site. This helper
    extracts the SENTIER canonical path from linking_stdout and finds the parent
    fundamental reference from its Tags_WP (fondamental-XXXX tag).
    """
    if not success or not linking_stdout.strip():
        return {"needed": False}

    try:
        linking_data = json.loads(linking_stdout)
    except ValueError:
        return {"needed": False}

    sentier_item = None
    for item in linking_data.get("items", []):
        if item.get("type") == "SENTIER":
            sentier_item = item
            break

    if not sentier_item:
        return {"needed": False}

    # canonical path is the second entry in updated_paths (local source file)
    updated_paths = sentier_item.get("updated_paths", [])
    if len(updated_paths) >= 2:
        canonical_path = updated_paths[1]
    elif updated_paths:
        canonical_path = updated_paths[0]
    else:
        canonical_path = ""

    parent_fundamental = ""
    try:
        import csv as _csv
        if index_path.exists():
            sentier_id = sentier_item.get("article_id", "")
            with index_path.open("r", encoding="utf-8-sig", newline="") as fh:
                reader = _csv.DictReader(fh)
                for row in reader:
                    if row.get("ID", "").strip() == sentier_id:
                        tags_raw = row.get("Tags_WP", "")
                        for tag in (t.strip() for t in tags_raw.split(";")):
                            if tag.startswith("fondamental-"):
                                parent_fundamental = tag
                                break
                        break
    except Exception:
        pass

    parent_ref = parent_fundamental or "fondamental non identifié"
    action = (
        "1. wp_push_draft --refresh-body sur le fichier SENTIER canonique (05_Sentier/…) "
        "si le corps a évolué après maillage. "
        f"2. Rafraîchir manuellement le fondamental parent ({parent_ref}) sur WP "
        "pour afficher la rubrique ## Ateliers sur le site."
    )
    return {
        "needed": True,
        "sentier_article_id": sentier_item.get("article_id", ""),
        "sentier_canonical_path": canonical_path,
        "sentier_wp_url": sentier_item.get("wordpress_url", ""),
        "parent_fundamental": parent_fundamental,
        "action": action,
    }


if __name__ == "__main__":
    raise SystemExit(main())
