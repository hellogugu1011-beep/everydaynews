import unittest

from everydaynews.collectors.x_api import build_recent_search_url, parse_recent_search_response
from everydaynews.enhancers.deepseek import apply_digest_to_items, build_digest_prompt, parse_digest_response
from everydaynews.models import NewsItem


class IntegrationTests(unittest.TestCase):
    def test_builds_x_recent_search_url(self):
        url = build_recent_search_url("AI 医疗", max_results=25)

        self.assertIn("https://api.x.com/2/tweets/search/recent", url)
        self.assertIn("max_results=25", url)
        self.assertIn("tweet.fields=", url)

    def test_parses_x_recent_search_response(self):
        payload = {
            "data": [
                {
                    "id": "1",
                    "text": "AI 医疗新进展",
                    "created_at": "2026-07-02T00:00:00Z",
                }
            ]
        }

        items = parse_recent_search_response(payload, "x_ai_health")

        self.assertEqual(items[0].source_id, "x_ai_health")
        self.assertEqual(items[0].url, "https://x.com/i/web/status/1")

    def test_deepseek_prompt_contains_limited_items(self):
        prompt = build_digest_prompt([{"title": "A", "summary": "B", "url": "https://a"}])

        self.assertIn("整理成中文日报条目", prompt)
        self.assertIn("中文标题", prompt)
        self.assertIn("https://a", prompt)

    def test_applies_chinese_digest_to_items(self):
        items = [NewsItem(title="Introducing GeneBench-Pro", url="https://openai.com/a", summary="English summary")]
        digest = '[{"url":"https://openai.com/a","title":"发布 GeneBench-Pro 基准","summary":"用于评估基因组学和生物科研 AI 能力。","tags":["ai","health"]}]'

        updated = apply_digest_to_items(items, parse_digest_response(digest))

        self.assertEqual(updated[0].title, "发布 GeneBench-Pro 基准")
        self.assertEqual(updated[0].summary, "用于评估基因组学和生物科研 AI 能力。")
        self.assertIn("health", updated[0].tags)


if __name__ == "__main__":
    unittest.main()
