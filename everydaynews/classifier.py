from __future__ import annotations

from .models import NewsItem


AI_KEYWORDS = {
    "ai",
    "人工智能",
    "大模型",
    "llm",
    "agent",
    "机器人",
    "模型",
    "算力",
    "芯片",
    "openai",
    "claude",
    "gemini",
    "deepseek",
}

HEALTH_KEYWORDS = {
    "医疗",
    "健康",
    "医院",
    "药品",
    "器械",
    "医保",
    "临床",
    "指南",
    "疾病",
    "公共卫生",
    "数字医疗",
    "诊疗",
}

CONFERENCE_KEYWORDS = {
    "大会",
    "会议",
    "论坛",
    "峰会",
    "年会",
    "征文",
    "报名",
    "日程",
    "参会",
    "举办",
}


def _contains_any(text: str, words: set[str]) -> bool:
    lower = text.lower()
    return any(word.lower() in lower for word in words)


def classify_item(item: NewsItem) -> NewsItem:
    text = f"{item.title} {item.summary} {' '.join(item.tags)}"
    has_ai = _contains_any(text, AI_KEYWORDS)
    has_health = _contains_any(text, HEALTH_KEYWORDS)
    has_conference = _contains_any(text, CONFERENCE_KEYWORDS) or item.is_conference

    tags = set(item.tags)
    if has_ai:
        tags.add("ai")
    if has_health:
        tags.add("health")
    if has_conference:
        tags.add("conference")
    if has_ai and has_health:
        tags.add("ai_health")

    if item.category in {"ai", "health", "conference"}:
        category = item.category
    elif has_conference:
        category = "conference"
    elif has_health:
        category = "health"
    elif has_ai:
        category = "ai"
    else:
        category = "other"

    item.category = category
    item.tags = sorted(tags)
    item.is_conference = category == "conference" or has_conference
    item.confidence = 0.9 if category != "other" else 0.3
    return item


def classify_items(items: list[NewsItem]) -> list[NewsItem]:
    return [classify_item(item) for item in items]
