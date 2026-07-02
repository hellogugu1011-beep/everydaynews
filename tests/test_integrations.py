import unittest

from everydaynews.collectors.x_api import build_recent_search_url, parse_recent_search_response
from everydaynews.enhancers.deepseek import build_digest_prompt


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

        self.assertIn("请为以下情报生成", prompt)
        self.assertIn("https://a", prompt)


if __name__ == "__main__":
    unittest.main()
