import json
import tempfile
import unittest
from pathlib import Path

from everydaynews.run_daily import run_daily


class RunnerTests(unittest.TestCase):
    def test_run_daily_writes_markdown_html_and_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config_path = root / "sources.json"
            output_dir = root / "output"
            config_path.write_text(
                json.dumps(
                    {
                        "sources": [
                            {
                                "id": "sample",
                                "name": "Sample",
                                "category_hint": "ai",
                                "type": "static",
                                "url": "https://sample.local",
                                "items": [
                                    {
                                        "title": "OpenAI 发布医疗 AI 进展",
                                        "url": "https://sample.local/a",
                                        "summary": "公开资讯摘要",
                                    }
                                ],
                            }
                        ]
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            paths = run_daily(config_path=config_path, output_dir=output_dir, report_date="2026-07-02")

            self.assertTrue(paths["markdown"].exists())
            self.assertTrue(paths["html"].exists())
            self.assertTrue(paths["json"].exists())
            self.assertIn("OpenAI 发布医疗 AI 进展", paths["markdown"].read_text(encoding="utf-8"))
            data = json.loads(paths["json"].read_text(encoding="utf-8"))
            self.assertEqual(data[0]["category"], "ai")


if __name__ == "__main__":
    unittest.main()
