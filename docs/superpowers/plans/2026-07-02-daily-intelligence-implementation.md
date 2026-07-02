# Daily Intelligence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first runnable version of the daily AI/health/conference intelligence collector with optional DeepSeek enhancement and X API support.

**Architecture:** Use a small Python package named `everydaynews`. Collectors produce normalized `NewsItem` objects; classifier/dedupe/render modules transform them into Markdown, HTML, and JSON reports. API-backed features are disabled unless environment variables are present.

**Tech Stack:** Python 3.11, stdlib `unittest`, optional runtime packages in `requirements.txt`, GitHub Actions.

---

### Task 1: Core Data Pipeline

**Files:**
- Create: `everydaynews/models.py`
- Create: `everydaynews/classifier.py`
- Create: `everydaynews/dedupe.py`
- Create: `everydaynews/render.py`
- Test: `tests/test_core.py`

- [ ] **Step 1: Write failing tests**

```python
from everydaynews.classifier import classify_item
from everydaynews.dedupe import dedupe_items
from everydaynews.models import NewsItem
from everydaynews.render import render_markdown

def test_classifies_ai_health_cross_item():
    item = NewsItem(title="医院发布大模型辅助诊疗平台", url="https://source/item")
    classified = classify_item(item)
    assert classified.category == "health"
    assert "ai" in classified.tags
    assert "ai_health" in classified.tags

def test_dedupes_by_url_and_normalized_title():
    items = [
        NewsItem(title="OpenAI 发布新模型", url="https://a/item"),
        NewsItem(title=" OpenAI发布新模型 ", url="https://b/item"),
        NewsItem(title="不同标题", url="https://a/item"),
    ]
    assert len(dedupe_items(items)) == 1

def test_render_markdown_groups_sections():
    md = render_markdown([NewsItem(title="WAIC 开幕", url="https://waic", category="conference")], "2026-07-02")
    assert "# 每日情报 2026-07-02" in md
    assert "## 国内会议" in md
    assert "[WAIC 开幕](https://waic)" in md
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m unittest tests.test_core -v`

Expected: import errors because `everydaynews` modules do not exist.

- [ ] **Step 3: Implement minimal modules**

Create focused modules with dataclasses, keyword classification, URL/title dedupe, and Markdown/HTML/JSON rendering.

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m unittest tests.test_core -v`

Expected: all tests pass.

### Task 2: API Integrations

**Files:**
- Create: `everydaynews/collectors/x_api.py`
- Create: `everydaynews/enhancers/deepseek.py`
- Test: `tests/test_integrations.py`

- [ ] **Step 1: Write failing tests**

```python
from everydaynews.collectors.x_api import build_recent_search_url, parse_recent_search_response
from everydaynews.enhancers.deepseek import build_digest_prompt

def test_builds_x_recent_search_url():
    url = build_recent_search_url("AI 医疗", max_results=25)
    assert "https://api.x.com/2/tweets/search/recent" in url
    assert "max_results=25" in url
    assert "tweet.fields=" in url

def test_parses_x_recent_search_response():
    payload = {"data": [{"id": "1", "text": "AI 医疗新进展", "created_at": "2026-07-02T00:00:00Z"}]}
    items = parse_recent_search_response(payload, "x_ai_health")
    assert items[0].source_id == "x_ai_health"
    assert items[0].url == "https://x.com/i/web/status/1"

def test_deepseek_prompt_contains_limited_items():
    prompt = build_digest_prompt([{"title": "A", "summary": "B", "url": "https://a"}])
    assert "请为以下情报生成" in prompt
    assert "https://a" in prompt
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m unittest tests.test_integrations -v`

Expected: import errors because integration modules do not exist.

- [ ] **Step 3: Implement minimal integrations**

Add X recent-search URL building and response parsing. Add DeepSeek prompt construction and an optional API client using `DEEPSEEK_API_KEY`.

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m unittest tests.test_integrations -v`

Expected: all tests pass without calling real APIs.

### Task 3: Runner, Config, Docs, GitHub Actions

**Files:**
- Create: `everydaynews/run_daily.py`
- Create: `config/sources.yaml`
- Create: `requirements.txt`
- Create: `.github/workflows/daily.yml`
- Modify: `README.md`
- Modify: `docs/requirements-technical-review.md`

- [ ] **Step 1: Add a CLI runner**

The runner loads sources, collects enabled sources, dedupes, classifies, optionally enhances, and writes `output/YYYY-MM-DD.{md,html,json}`.

- [ ] **Step 2: Add default config**

Default sources include RSS/API-friendly P0 sources and disabled X API sources that require `X_BEARER_TOKEN`.

- [ ] **Step 3: Add GitHub Actions**

The workflow installs dependencies and runs `python -m everydaynews.run_daily --days 2 --output-dir output`.

- [ ] **Step 4: Verify locally**

Run:

```powershell
python -m unittest discover -s tests -v
python -m everydaynews.run_daily --days 2 --output-dir output --max-items 30
```

Expected: tests pass and output files are generated.

### Self-Review

- Spec coverage: local files, GitHub Actions, X API optional source, DeepSeek optional model enhancement, Markdown/HTML/JSON output, source failure isolation.
- Placeholder scan: no unfinished markers or unspecified implementation steps.
- Type consistency: `NewsItem`, `Source`, `SourceStatus`, and category/tag fields are shared across collectors, classifiers, dedupe, and render.
