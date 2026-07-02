from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Source:
    id: str
    name: str
    category_hint: str
    type: str
    url: str
    enabled: bool = True
    rss_url: str | None = None
    priority: str = "P1"
    query: str | None = None
    max_results: int = 20
    rate_limit_seconds: float = 1.0


@dataclass
class NewsItem:
    title: str
    url: str
    source_id: str = ""
    source_name: str = ""
    published_at: str | None = None
    discovered_at: str = field(default_factory=utc_now_iso)
    category: str = "unknown"
    tags: list[str] = field(default_factory=list)
    summary: str = ""
    confidence: float = 0.0
    is_conference: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class SourceStatus:
    source_id: str
    ok: bool
    count: int = 0
    message: str = ""
    checked_at: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
