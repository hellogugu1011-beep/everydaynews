from __future__ import annotations

import json
import os
from urllib.request import Request, urlopen


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
            }
        )
    return (
        "请为以下情报生成中文日报增强内容。要求：\n"
        "1. 每条只输出一句不超过60字的摘要。\n"
        "2. 标注 tags，尤其识别 ai_health 交叉内容。\n"
        "3. 不编造原文没有的信息。\n"
        "4. 输出 JSON 数组，每个对象包含 title、summary、tags。\n\n"
        f"{json.dumps(compact, ensure_ascii=False)}"
    )


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
