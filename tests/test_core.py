import unittest

from everydaynews.classifier import classify_item
from everydaynews.dedupe import dedupe_items
from everydaynews.models import NewsItem
from everydaynews.render import render_markdown


class CorePipelineTests(unittest.TestCase):
    def test_classifies_ai_health_cross_item(self):
        item = NewsItem(title="医院发布大模型辅助诊疗平台", url="https://source/item")

        classified = classify_item(item)

        self.assertEqual(classified.category, "health")
        self.assertIn("ai", classified.tags)
        self.assertIn("ai_health", classified.tags)

    def test_dedupes_by_url_and_normalized_title(self):
        items = [
            NewsItem(title="OpenAI 发布新模型", url="https://a/item"),
            NewsItem(title=" OpenAI发布新模型 ", url="https://b/item"),
            NewsItem(title="不同标题", url="https://a/item"),
        ]

        deduped = dedupe_items(items)

        self.assertEqual(len(deduped), 1)
        self.assertEqual(deduped[0].title, "OpenAI 发布新模型")

    def test_render_markdown_groups_sections(self):
        markdown = render_markdown(
            [NewsItem(title="WAIC 开幕", url="https://waic", category="conference")],
            "2026-07-02",
        )

        self.assertIn("# 每日情报 2026-07-02", markdown)
        self.assertIn("## 国内会议", markdown)
        self.assertIn("[WAIC 开幕](https://waic)", markdown)


if __name__ == "__main__":
    unittest.main()
