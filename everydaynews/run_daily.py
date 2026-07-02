from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

from .classifier import classify_items
from .collectors.html_list import collect_html_list
from .collectors.rss import collect_rss
from .collectors.static import collect_static
from .collectors.x_api import collect_x_recent_search
from .config import load_sources
from .dedupe import dedupe_items
from .enhancers.deepseek import call_deepseek_digest
from .models import NewsItem, Source, SourceStatus
from .render import write_report_files


def collect_source(source: Source) -> tuple[list[NewsItem], SourceStatus]:
    try:
        if source.type == "static":
            items = collect_static(source)
        elif source.type == "rss":
            items = collect_rss(source)
        elif source.type == "rss_or_html":
            try:
                items = collect_rss(source)
            except Exception:
                items = collect_html_list(source)
        elif source.type == "html_list":
            items = collect_html_list(source)
        elif source.type == "x_recent_search":
            items = collect_x_recent_search(source)
        else:
            return [], SourceStatus(source.id, False, 0, f"unsupported source type: {source.type}")
        return items, SourceStatus(source.id, True, len(items), "ok")
    except Exception as exc:
        return [], SourceStatus(source.id, False, 0, str(exc))


def run_daily(
    config_path: Path,
    output_dir: Path,
    report_date: str | None = None,
    max_items: int = 200,
    enhance: bool = False,
) -> dict[str, Path]:
    report_date = report_date or date.today().isoformat()
    sources = [source for source in load_sources(config_path) if source.enabled]
    all_items: list[NewsItem] = []
    statuses: list[SourceStatus] = []
    for source in sources:
        items, status = collect_source(source)
        statuses.append(status)
        all_items.extend(items)

    items = classify_items(dedupe_items(all_items))[:max_items]
    paths = write_report_files(items, report_date, output_dir, statuses)

    data_dir = output_dir.parent / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    (data_dir / "source-status.json").write_text(
        json.dumps([status.to_dict() for status in statuses], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    if enhance:
        digest = call_deepseek_digest([item.to_dict() for item in items])
        if digest:
            deepseek_path = output_dir / f"{report_date}.deepseek.txt"
            deepseek_path.write_text(digest, encoding="utf-8")
            paths["deepseek"] = deepseek_path
    return paths


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate daily AI/health/conference intelligence reports.")
    parser.add_argument("--config", type=Path, default=Path("config/sources.yaml"))
    parser.add_argument("--output-dir", type=Path, default=Path("output"))
    parser.add_argument("--date", dest="report_date", default=None)
    parser.add_argument("--days", type=int, default=2, help="Reserved for future lookback filtering.")
    parser.add_argument("--max-items", type=int, default=200)
    parser.add_argument("--enhance", action="store_true", help="Call DeepSeek if DEEPSEEK_API_KEY is set.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    paths = run_daily(
        config_path=args.config,
        output_dir=args.output_dir,
        report_date=args.report_date,
        max_items=args.max_items,
        enhance=args.enhance,
    )
    for kind, path in paths.items():
        print(f"{kind}: {path}")


if __name__ == "__main__":
    main()
