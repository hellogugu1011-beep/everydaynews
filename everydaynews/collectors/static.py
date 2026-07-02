from __future__ import annotations

from everydaynews.models import NewsItem, Source


def collect_static(source: Source) -> list[NewsItem]:
    items = []
    for raw in getattr(source, "metadata", {}).get("items", []):
        items.append(
            NewsItem(
                title=raw["title"],
                url=raw["url"],
                source_id=source.id,
                source_name=source.name,
                published_at=raw.get("published_at"),
                category=raw.get("category", source.category_hint),
                tags=list(raw.get("tags", [])),
                summary=raw.get("summary", ""),
                is_conference=source.category_hint == "conference",
                metadata={k: v for k, v in raw.items() if k not in {"title", "url", "summary", "published_at", "category", "tags"}},
            )
        )
    return items
