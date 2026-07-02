from __future__ import annotations

import json
import os
from urllib.request import Request, urlopen

from everydaynews.models import NewsItem


DEEPSEEK_CHAT_COMPLETIONS_URL = "https://api.deepseek.com/chat/completions"


def build_digest_prompt(items: list[dict], max_items: int = 80) -> str:
    compact = []
    for item in items[:max_items]:
        compact.append(
            {
                "title": item.get("title", ""),
                "source": item.get("source_name", ""),
                "summary": item.get("summary", ""),
                "url": item.get("url", ""),
                "category": item.get("category", ""),
                "tags": item.get("tags", []),
            }
        )
    return (
        "请把以下情报整理成中文日报条目。要求：\n"
        "1. 将英文标题改写为自然中文标题；中文标题也可润色，但不要夸大。\n"
        "2. 每条只输出一句不超过60字的中文摘要。\n"
        "2. 标注 tags，尤其识别 ai_health 交叉内容。\n"
        "3. 不编造原文没有的信息。\n"
        "4. 输出 JSON 数组，每个对象包含 url、title、summary、tags。\n\n"
        f"{json.dumps(compact, ensure_ascii=False)}"
    )


def parse_digest_response(text: str) -> list[dict]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.startswith("json"):
            cleaned = cleaned[4:].strip()
    start = cleaned.find("[")
    end = cleaned.rfind("]")
    if start >= 0 and end >= start:
        cleaned = cleaned[start : end + 1]
    data = json.loads(cleaned)
    if not isinstance(data, list):
        return []
    return [entry for entry in data if isinstance(entry, dict)]


def apply_digest_to_items(items: list[NewsItem], digest_entries: list[dict]) -> list[NewsItem]:
    by_url = {str(entry.get("url", "")): entry for entry in digest_entries}
    for item in items:
        entry = by_url.get(item.url)
        if not entry:
            continue
        title = str(entry.get("title", "")).strip()
        summary = str(entry.get("summary", "")).strip()
        tags = entry.get("tags", [])
        if title:
            item.title = title
        if summary:
            item.summary = summary
        if isinstance(tags, list):
            item.tags = sorted(set(item.tags).union(str(tag) for tag in tags if str(tag).strip()))
    return items


def call_deepseek_digest(items: list[dict], api_key: str | None = None, model: str = "deepseek-chat") -> str | None:
    token = api_key or os.getenv("DEEPSEEK_API_KEY")
    if not token:
        return None
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "你是严谨的中文行业情报编辑。"},
            {"role": "user", "content": build_digest_prompt(items)},
        ],
        "temperature": 0.2,
    }
    request = Request(
        DEEPSEEK_CHAT_COMPLETIONS_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "everydaynews/0.1",
        },
        method="POST",
    )
    with urlopen(request, timeout=60) as response:
        data = json.loads(response.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"]
