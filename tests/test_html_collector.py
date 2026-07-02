import unittest

from everydaynews.collectors.html_list import extract_html_items
from everydaynews.models import Source


class HtmlCollectorTests(unittest.TestCase):
    def test_extract_html_items_filters_navigation_and_allows_url_patterns(self):
        source = Source(
            id="anthropic",
            name="Anthropic",
            category_hint="ai",
            type="html_list",
            url="https://www.anthropic.com/news",
        )
        source.metadata = {
            "include_url_contains": ["/news/"],
            "exclude_title_contains": ["skip to", "press@"],
        }
        html = """
        <a href="#main-content">Skip to main content</a>
        <a href="mailto:press@anthropic.com">press@anthropic.com</a>
        <a href="/research">Research</a>
        <a href="/news/claude-sonnet-5">Introducing Claude Sonnet 5</a>
        """

        items = extract_html_items(source, html)

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].title, "Introducing Claude Sonnet 5")
        self.assertEqual(items[0].url, "https://www.anthropic.com/news/claude-sonnet-5")


if __name__ == "__main__":
    unittest.main()
