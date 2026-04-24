#!/usr/bin/env python3
"""
Daily Le Phare routine.

Behavior:
- choose a topic automatically from current news RSS feeds unless provided
- avoid repeating very recent topics when possible
- run the editorial pipeline
- optionally push drafts to WordPress
- log each run to 00_Systeme/Logs
"""

from __future__ import annotations

import argparse
import json
import re
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
EDITORIAL_CONFIG = TOOLS_DIR / "editorial_config.local.json"
WP_CONFIG = TOOLS_DIR / "wp_config.local.json"
INDEX_PATH = ROOT_DIR / "index_editorial.csv"

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
    parser.add_argument("--force", action="store_true", help="Run even if today's routine already succeeded")
    parser.add_argument("--use-api-llm", action="store_true", help="Use the technical API pipeline explicitly instead of the default assisted-agent workflow")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    state_path = LOGS_DIR / f"daily_run_{today_iso()}.json"
    log_path = LOGS_DIR / f"daily_run_{today_iso()}.log"

    if state_path.exists() and not args.force:
        existing = json.loads(state_path.read_text(encoding="utf-8"))
        if existing.get("status") == "success":
            write_log(log_path, f"Daily routine already completed today for topic: {existing.get('topic')}")
            print(f"Daily routine already completed today: {existing.get('topic')}")
            return 0

    try:
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
            use_api_llm=args.use_api_llm,
        )
        write_log(log_path, f"Running command: {' '.join(command)}")
        result = run_logged_command(command, log_path, "PIPELINE")

        linking_stdout = ""
        linking_stderr = ""
        failure_message = ""
        publish_dir = extract_publish_dir(result.stdout)
        overall_returncode = result.returncode
        if result.returncode == 0 and should_run_triptych_linking(args.mode, args.output_profile) and not args.no_publish_drafts:
            if not publish_dir:
                raise RuntimeError("Unable to locate triptych publish directory from pipeline output")
            linking_command = build_post_linking_command(
                triptych_dir=publish_dir,
                index_path=Path(args.index),
                wp_config_path=Path(args.wp_config),
            )
            write_log(log_path, f"Running post-linking command: {' '.join(linking_command)}")
            linking_result = run_logged_command(linking_command, log_path, "POST-LINKING")
            linking_stdout = linking_result.stdout
            linking_stderr = linking_result.stderr

            if linking_result.returncode != 0:
                overall_returncode = linking_result.returncode
                failure_message = linking_stderr.strip() or linking_stdout.strip() or "Post-linking failed"

        status = "success" if overall_returncode == 0 else "error"
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
            "completed_at": datetime.now().isoformat(timespec="seconds"),
        }
        state_path.write_text(json.dumps(state_payload, ensure_ascii=False, indent=2), encoding="utf-8")

        if overall_returncode != 0:
            print(failure_message or result.stderr.strip() or result.stdout.strip() or "Daily routine failed")
            return overall_returncode

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


def should_run_triptych_linking(mode: str, output_profile: str) -> bool:
    if mode == "triptyque":
        return True
    if mode == "architecture_editoriale":
        return output_profile == "triptyque_minimal"
    return False


def build_post_linking_command(triptych_dir: Path, index_path: Path, wp_config_path: Path) -> list[str]:
    return [
        sys.executable,
        str(POST_LINKING_PATH),
        str(triptych_dir),
        "--index",
        str(index_path),
        "--config",
        str(wp_config_path),
    ]


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


if __name__ == "__main__":
    raise SystemExit(main())
