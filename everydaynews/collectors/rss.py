from __future__ import annotations

from everydaynews.models import NewsItem, Source


def collect_rss(source: Source) -> list[NewsItem]:
    import feedparser

    feed = feedparser.parse(source.rss_url or source.url)
    items: list[NewsItem] = []
    for entry in feed.entries[: source.max_results]:
        title = str(getattr(entry, "title", "")).strip()
        url = str(getattr(entry, "link", "")).strip()
        if not title or not url:
            continue
        published = getattr(entry, "published", None) or getattr(entry, "updated", None)
        summary = str(getattr(entry, "summary", "") or "").strip()
        items.append(
            NewsItem(
                title=title,
                url=url,
                source_id=source.id,
                source_name=source.name,
                published_at=published,
                category=source.category_hint,
                summary=summary[:240],
                is_conference=source.category_hint == "conference",
            )
        )
    return items
