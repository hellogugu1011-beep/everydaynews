from __future__ import annotations

import hashlib
import re
from urllib.parse import urldefrag, urlsplit, urlunsplit

from .models import NewsItem


TRACKING_PREFIXES = ("utm_",)
TRACKING_KEYS = {"spm", "from", "source", "ref", "fbclid", "gclid"}


def normalize_url(url: str) -> str:
    clean, _fragment = urldefrag(url.strip())
    parts = urlsplit(clean)
    query_parts = []
    for pair in parts.query.split("&"):
        if not pair:
            continue
        key = pair.split("=", 1)[0].lower()
        if key in TRACKING_KEYS or any(key.startswith(prefix) for prefix in TRACKING_PREFIXES):
            continue
        query_parts.append(pair)
    return urlunsplit((parts.scheme, parts.netloc.lower(), parts.path.rstrip("/"), "&".join(query_parts), ""))


def normalize_title(title: str) -> str:
    return re.sub(r"[\s\u3000:：｜|\-—_]+", "", title).lower()


def item_fingerprint(item: NewsItem) -> str:
    basis = normalize_url(item.url) or normalize_title(item.title)
    return hashlib.sha256(basis.encode("utf-8")).hexdigest()


def dedupe_items(items: list[NewsItem]) -> list[NewsItem]:
    seen_urls: set[str] = set()
    seen_titles: set[str] = set()
    deduped: list[NewsItem] = []
    for item in items:
        url_key = normalize_url(item.url)
        title_key = normalize_title(item.title)
        if url_key in seen_urls or title_key in seen_titles:
            continue
        seen_urls.add(url_key)
        seen_titles.add(title_key)
        deduped.append(item)
    return deduped
