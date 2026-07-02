from __future__ import annotations

import json
import os
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from everydaynews.models import NewsItem, Source


X_RECENT_SEARCH_URL = "https://api.x.com/2/tweets/search/recent"


def build_recent_search_url(query: str, max_results: int = 20) -> str:
    params = {
        "query": query,
        "max_results": max(10, min(max_results, 100)),
        "tweet.fields": "created_at,public_metrics,lang,author_id",
    }
    return f"{X_RECENT_SEARCH_URL}?{urlencode(params)}"


def parse_recent_search_response(payload: dict, source_id: str, source_name: str = "X Recent Search") -> list[NewsItem]:
    items: list[NewsItem] = []
    for post in payload.get("data", []) or []:
        post_id = str(post.get("id", "")).strip()
        text = str(post.get("text", "")).strip()
        if not post_id or not text:
            continue
        items.append(
            NewsItem(
                title=text[:120],
                summary=text,
                url=f"https://x.com/i/web/status/{post_id}",
                source_id=source_id,
                source_name=source_name,
                published_at=post.get("created_at"),
                category="other",
                metadata={"x_metrics": post.get("public_metrics", {})},
            )
        )
    return items


def collect_x_recent_search(source: Source, bearer_token: str | None = None) -> list[NewsItem]:
    token = bearer_token or os.getenv("X_BEARER_TOKEN")
    if not token:
        return []
    query = source.query or source.url
    request = Request(
        build_recent_search_url(query, source.max_results),
        headers={"Authorization": f"Bearer {token}", "User-Agent": "everydaynews/0.1"},
    )
    with urlopen(request, timeout=20) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return parse_recent_search_response(payload, source.id, source.name)
