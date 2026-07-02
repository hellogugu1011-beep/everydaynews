from __future__ import annotations

import html
import json
from collections import defaultdict
from pathlib import Path

from .models import NewsItem, SourceStatus


SECTION_NAMES = {
    "ai": "AI资讯",
    "health": "医疗健康资讯",
    "conference": "国内会议",
    "other": "其他线索",
    "unknown": "未分类",
}

SECTION_ORDER = ["ai", "health", "conference", "other", "unknown"]


def _group_items(items: list[NewsItem]) -> dict[str, list[NewsItem]]:
    groups: dict[str, list[NewsItem]] = defaultdict(list)
    for item in items:
        groups[item.category or "unknown"].append(item)
    return groups


def render_markdown(items: list[NewsItem], report_date: str, statuses: list[SourceStatus] | None = None) -> str:
    groups = _group_items(items)
    lines = [
        f"# 每日情报 {report_date}",
        "",
        "> 本日报为公开资讯摘要索引，不构成医疗建议。请以原文和官方发布为准。",
        "",
    ]
    for category in SECTION_ORDER:
        section_items = groups.get(category, [])
        if not section_items:
            continue
        lines.extend([f"## {SECTION_NAMES[category]}", ""])
        for item in section_items:
            summary = f" - {item.summary}" if item.summary else ""
            tags = f" `{'`, `'.join(item.tags)}`" if item.tags else ""
            source = f" 来源：{item.source_name}" if item.source_name else ""
            lines.append(f"- [{item.title}]({item.url}){summary}{source}{tags}")
        lines.append("")

    failed = [status for status in statuses or [] if not status.ok]
    if failed:
        lines.extend(["## 信源健康", ""])
        for status in failed:
            lines.append(f"- `{status.source_id}` 抓取失败：{status.message}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_html(items: list[NewsItem], report_date: str, statuses: list[SourceStatus] | None = None) -> str:
    markdown = render_markdown(items, report_date, statuses)
    body_lines = []
    for line in markdown.splitlines():
        if line.startswith("# "):
            body_lines.append(f"<h1>{html.escape(line[2:])}</h1>")
        elif line.startswith("## "):
            body_lines.append(f"<h2>{html.escape(line[3:])}</h2>")
        elif line.startswith("- "):
            body_lines.append(f"<p>{html.escape(line)}</p>")
        elif line.startswith("> "):
            body_lines.append(f"<blockquote>{html.escape(line[2:])}</blockquote>")
        elif line:
            body_lines.append(f"<p>{html.escape(line)}</p>")
    return "\n".join(
        [
            "<!doctype html>",
            '<html lang="zh-CN">',
            "<head>",
            '<meta charset="utf-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            f"<title>每日情报 {html.escape(report_date)}</title>",
            "<style>body{font-family:system-ui,sans-serif;max-width:980px;margin:32px auto;padding:0 20px;line-height:1.7;color:#1f2937}h1,h2{color:#111827}blockquote{border-left:4px solid #94a3b8;padding-left:12px;color:#475569}p{margin:8px 0}</style>",
            "</head>",
            "<body>",
            *body_lines,
            "</body>",
            "</html>",
        ]
    )


def write_report_files(
    items: list[NewsItem],
    report_date: str,
    output_dir: Path,
    statuses: list[SourceStatus] | None = None,
) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "markdown": output_dir / f"{report_date}.md",
        "html": output_dir / f"{report_date}.html",
        "json": output_dir / f"{report_date}.json",
    }
    paths["markdown"].write_text(render_markdown(items, report_date, statuses), encoding="utf-8")
    paths["html"].write_text(render_html(items, report_date, statuses), encoding="utf-8")
    paths["json"].write_text(
        json.dumps([item.to_dict() for item in items], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return paths
