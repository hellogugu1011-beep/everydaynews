from __future__ import annotations

from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen

from everydaynews.models import NewsItem, Source


DEFAULT_EXCLUDED_TITLE_PARTS = {
    "skip to",
    "press@",
    "ICP备",
    "版权所有",
    "隐私",
    "privacy",
    "terms",
    "cookie",
    "learn more",
    "page ",
    "下一页",
    "上一页",
}


def _allowed_by_patterns(url: str, title: str, source: Source) -> bool:
    metadata = getattr(source, "metadata", {})
    include_parts = metadata.get("include_url_contains", [])
    exclude_parts = metadata.get("exclude_title_contains", [])
    if include_parts and not any(part in url for part in include_parts):
        return False
    lowered_title = title.lower()
    for part in list(DEFAULT_EXCLUDED_TITLE_PARTS) + list(exclude_parts):
        if str(part).lower() in lowered_title:
            return False
    scheme = urlsplit(url).scheme
    return scheme in {"http", "https"}


def extract_html_items(source: Source, html: str) -> list[NewsItem]:
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    items: list[NewsItem] = []
    seen_urls: set[str] = set()
    for anchor in soup.find_all("a", href=True):
        title = " ".join(anchor.get_text(" ", strip=True).split())
        if len(title) < 6:
            continue
        url = urljoin(source.url, anchor["href"])
        if not _allowed_by_patterns(url, title, source):
            continue
        if url in seen_urls:
            continue
        seen_urls.add(url)
        items.append(
            NewsItem(
                title=title[:160],
                url=url,
                source_id=source.id,
                source_name=source.name,
                category=source.category_hint,
                is_conference=source.category_hint == "conference",
            )
        )
        if len(items) >= source.max_results:
            break
    return items


def collect_html_list(source: Source) -> list[NewsItem]:
    request = Request(
        source.url,
        headers={
            "User-Agent": "Mozilla/5.0 everydaynews/0.1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        },
    )
    with urlopen(request, timeout=25) as response:
        html = response.read().decode("utf-8", errors="ignore")
    return extract_html_items(source, html)
