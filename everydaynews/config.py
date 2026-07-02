from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import Source


def _load_mapping(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    try:
        import yaml
    except ImportError as exc:
        raise RuntimeError("PyYAML is required for YAML config files. Run: pip install -r requirements.txt") from exc
    return yaml.safe_load(text) or {}


def load_sources(path: Path) -> list[Source]:
    data = _load_mapping(path)
    sources = []
    for raw in data.get("sources", []):
        source = Source(
            id=raw["id"],
            name=raw.get("name", raw["id"]),
            category_hint=raw.get("category_hint", "unknown"),
            type=raw.get("type", "html_list"),
            url=raw.get("url", ""),
            enabled=raw.get("enabled", True),
            rss_url=raw.get("rss_url"),
            priority=raw.get("priority", "P1"),
            query=raw.get("query"),
            max_results=int(raw.get("max_results", 20)),
            rate_limit_seconds=float(raw.get("rate_limit_seconds", 1.0)),
        )
        source.metadata = raw
        sources.append(source)
    return sources
