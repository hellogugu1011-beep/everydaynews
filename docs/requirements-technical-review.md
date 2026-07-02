# AI/医疗健康/国内会议每日情报脚本 - 需求与技术评审

日期：2026-07-02  
状态：评审稿  
负责人：咕咕 + Codex

## 1. 背景与目标

每天从互联网上收集三类信息：

1. AI 相关资讯。
2. 医疗健康领域资讯。
3. 国内会议信息，重点包含 AI、医疗健康、医药产业和学术会议。

目标不是做“全网爬虫”，而是做一个可靠、可复核、低维护成本的情报日报脚本。每条信息必须保留来源链接和发布时间，方便继续核验和深挖。

## 2. 一句话问题

如何用一个可定时运行的轻量脚本，把分散在官网、RSS、公开列表页和会议网站中的 AI/医疗健康/会议信息，整理成每天可读、可追踪、可复核的日报？

## 3. 本期范围

### 做什么

- 每天拉取最近 24 小时到 72 小时内的新内容。
- 按 `AI资讯`、`医疗健康资讯`、`国内会议` 三类归档。
- 对标题、链接和相似标题做去重。
- 为每条记录保留：
  - 标题
  - 来源站点
  - 原文链接
  - 发布时间或发现时间
  - 分类
  - 关键词标签
  - 简短摘要
  - 抓取状态
- 输出本地文件：
  - `output/YYYY-MM-DD.md`
  - `output/YYYY-MM-DD.html`
  - `output/YYYY-MM-DD.json`
- 支持两种运行方式：
  - GitHub Actions 每天定时运行并提交日报文件。
  - 本地手动或系统计划任务运行，只落本地文件。

### 不做什么

- 不登录网站，不使用个人 cookies。
- 不绕过验证码、付费墙或强反爬机制。
- 不全文转载文章，只做标题、摘要、链接和结构化索引。
- 不做医疗建议，不对疾病诊疗内容给结论。
- 不做实时舆情大屏，不做复杂后台。
- 不在第一版抓取需登录的社交平台内容，除非使用官方 API、合规第三方数据服务或人工提供的种子链接。
- 不在第一版抓取任意微信公众号历史文章；只考虑已授权公众号、合规数据服务或人工维护链接。

## 4. 可以直接上 GitHub 吗？

可以，但要满足两个条件：

1. 有一个 GitHub 仓库承载脚本和输出文件。
2. 只使用公开信源，或把任何密钥放进 GitHub Secrets。

推荐设计为“GitHub 优先、本地兼容”：

- GitHub 方式：`schedule` 定时触发，每天运行脚本，生成 `output/` 和 `data/` 文件，自动 commit。需要展示网页时可再开 GitHub Pages。
- 本地方式：同一个脚本用 PowerShell 或任务计划程序运行，输出到本地目录。

当前工作区 `D:\市场分析` 不是 git 仓库，所以现在不能直接推送。实现时可以新建 GitHub 仓库，或者先在本地完成脚本后再初始化 git。

## 5. 首版信源覆盖

原则：首版优先覆盖稳定、公开、可复核的来源。每个信源先按低频率抓取，失败不影响整体日报。

### 5.1 AI 资讯

| 优先级 | 信源 | URL | 抓取方式 | 用途 |
|---|---|---|---|---|
| P0 | OpenAI News | https://openai.com/news/ | RSS 优先，HTML 兜底 | 官方产品、研究、政策动态 |
| P0 | Anthropic News | https://www.anthropic.com/news | HTML 列表页 | Claude、模型、安全与公司动态 |
| P0 | Google DeepMind Blog | https://deepmind.google/blog/ | HTML 列表页/RSS 探测 | 模型与研究进展 |
| P0 | arXiv AI/ML/NLP | https://rss.arxiv.org/rss/cs.AI 等 | RSS | 研究论文趋势 |
| P1 | Hugging Face Blog | https://huggingface.co/blog | RSS/HTML 探测 | 开源模型、数据集、工具 |
| P1 | 机器之心 | https://www.jiqizhixin.com/ | HTML/RSSHub 可选 | 中文 AI 产业与研究报道 |
| P1 | 量子位 | https://www.qbitai.com/ | HTML/RSSHub 可选 | 中文 AI 产品与产业报道 |
| P1 | 36氪 AI 相关内容 | https://36kr.com/ | 搜索/RSSHub 可选 | 国内 AI 创业和融资 |
| P2 | GitHub Trending AI 关键词 | https://github.com/trending | HTML/API 可选 | 开源项目趋势 |

首版建议先接 P0 + 2 个 P1 中文源。P2 放到第二阶段，避免首版噪声过大。

### 5.2 医疗健康资讯

| 优先级 | 信源 | URL | 抓取方式 | 用途 |
|---|---|---|---|---|
| P0 | 国家卫健委 | https://www.nhc.gov.cn/ | HTML 列表页 | 政策、新闻发布会、行业监管 |
| P0 | 国家药监局 | https://www.nmpa.gov.cn/ | HTML 列表页 | 药品、器械、审评审批政策 |
| P0 | 中国疾控中心 | https://www.chinacdc.cn/ | HTML 列表页 | 公共卫生、疾控信息 |
| P0 | 国家医保局 | https://www.nhsa.gov.cn/ | HTML 列表页 | 医保政策、支付与目录动态 |
| P1 | 医脉通 | https://www.medlive.cn/ | HTML 列表页 | 医学资讯、临床与学术信息 |
| P1 | 丁香园 | https://www.dxy.cn/ | HTML/RSSHub 可选 | 医疗行业、医生社区资讯 |
| P1 | 健康界 | https://www.cn-healthcare.com/ | HTML/RSSHub 可选 | 医院管理、健康产业 |
| P1 | 动脉网 | https://www.vbdata.cn/ | HTML/RSSHub 可选 | 医疗科技、数字健康、投融资 |
| P2 | 梅斯医学 | https://www.medsci.cn/ | HTML/RSSHub 可选 | 医学研究、指南、会议资讯 |

医疗健康类首版要明显区分“官方政策”和“行业媒体”。日报中官方政策排在前面，行业媒体只做线索。

### 5.3 国内会议

| 优先级 | 信源 | URL | 抓取方式 | 用途 |
|---|---|---|---|---|
| P0 | WAIC 世界人工智能大会 | https://www.worldaic.com.cn/ | HTML 列表页 | 国内 AI 旗舰会议 |
| P0 | InfoQ 技术大会/AICon/QCon | https://con.infoq.cn/ | HTML 列表页 | AI 工程与技术会议 |
| P0 | CCF Deadlines | https://github.com/ccfddl/ccf-deadlines | GitHub 数据/页面 | AI/计算机学术会议截止日期 |
| P0 | 医脉通会议 | https://meetings.medlive.cn/browse/0/1/1 | HTML 列表页 | 国内医学会议聚合 |
| P0 | 丁香会议 | https://meeting.dxy.cn/ | HTML 列表页 | 医学、药学、生命科学会议 |
| P1 | 美迪康会务通 | https://mm.sciconf.cn/ | HTML 列表页/搜索入口 | 中华医学会等会议页面 |
| P1 | 全球医学会议网 | https://www.globalconfs.com/meetinglist.html?country2_id=7 | HTML 列表页 | 中国境内医学会议补充 |
| P1 | 医药魔方医药日历 | https://bydrug.pharmcube.com/calendar | HTML/接口探测 | 医药产业会议、注册节点 |
| P2 | 各单项大会官网 | 例如 CCF、各医学分会官网 | 手工配置 | 重要会议专项跟踪 |

会议类不只抓“今天发布”，还要维护未来 3 到 12 个月会议池。日报展示新发现、日期变更、征稿/报名截止临近提醒。

### 5.4 社交媒体与内容社区

社交媒体可以补充“早期信号”和“讨论热度”，但合规和稳定性弱于官网/RSS。首版建议作为 P2 增强源，不作为日报主来源。

| 优先级 | 信源 | 推荐方式 | 是否适合 GitHub Actions | 说明 |
|---|---|---|---|---|
| P2 | X / Twitter | 官方 X API，关键词和账号列表查询 | 适合，API key 放 GitHub Secrets | 官方 API 可访问公开对话，但 2026 年已偏向按量计费；不建议网页爬取 |
| P2 | 小红书 | 官方开放平台、合规第三方数据服务、人工种子链接 | 取决于 API/服务；不建议用登录态跑 Actions | 官方开放平台主要面向商业/营销/电商等场景，通用搜索和笔记采集权限需要单独评估 |
| P2 | 微信公众号 | 已授权公众号素材 API、第三方合规数据服务、人工种子链接 | 已授权 API 适合；模拟人工不适合 | 官方接口能获取自己或授权公众号素材；不提供任意公众号全网搜索抓取接口 |
| P2 | 公众号文章搜索补充 | 搜狗微信/第三方索引服务 | 不建议作为稳定主链路 | 容易遇到验证码、失效、反爬和版权风险 |

社交媒体首版推荐策略：

1. X 只做可选 API 接入，默认关闭。
2. 小红书不做自动网页登录抓取，先支持人工维护关键词、账号、笔记链接。
3. 微信公众号不做模拟人工抓取，先支持人工维护文章 URL，或后续接入已授权公众号素材 API。
4. 社交媒体数据只保存标题/摘要/链接/互动指标，不保存全文和用户隐私字段。

### 5.5 微信公众号是否只能模拟人工获取？

不是“只能”，但要分场景：

- 如果是自己运营或已授权的公众号，可以通过微信公众平台/开放平台接口获取素材或已发布内容，需要 `appid`、`secret`、access token、IP 白名单等配置。
- 如果是任意第三方公众号，官方没有提供“按关键词搜索全网公众号文章”的通用接口。常见的搜狗微信、浏览器自动化、手机/PC 模拟人工方案都更脆弱，也更容易触碰验证码、平台条款和版权边界。
- 因此本项目默认不做模拟人工抓公众号。更稳的方式是人工维护关注账号/文章链接，或采购有授权的数据服务。

## 6. 数据流设计

```text
+-----------------+      +-----------------+      +------------------+
| sources.yaml    | ---> | collector        | ---> | raw items         |
| 信源配置        |      | RSS/HTML/API     |      | 原始抓取结果      |
+-----------------+      +-----------------+      +------------------+
                                                         |
                                                         v
+-----------------+      +-----------------+      +------------------+
| daily report     | <--- | renderer         | <--- | normalizer       |
| MD/HTML/JSON     |      | 模板渲染        |      | 字段归一化       |
+-----------------+      +-----------------+      +------------------+
                                                         |
                                                         v
                                                +------------------+
                                                | classifier       |
                                                | 分类/关键词/去重 |
                                                +------------------+
```

### 6.1 普通脚本与模型能力边界

默认首版可以做到“零模型调用”。模型只作为质量增强，不是运行必需项。

| 环节 | 默认实现 | 是否用模型 | 说明 |
|---|---|---|---|
| 定时运行 | GitHub Actions / 本地任务计划 | 否 | 纯脚本 |
| 抓取 RSS/HTML/API | `requests`、`feedparser`、`beautifulsoup4` | 否 | 纯脚本 |
| 字段归一化 | 规则解析、日期解析、URL 规范化 | 否 | 纯脚本 |
| 基础分类 | 信源默认分类 + 关键词规则 | 否 | 纯脚本 |
| 去重 | URL、规范化标题、相似度阈值 | 否 | 纯脚本 |
| 会议日期抽取 | 正则和日期解析 | 否，复杂时可选 | 首版先规则化 |
| 摘要 | 标题/描述截断或页面 meta description | 否，质量一般 | 首版可不调用模型 |
| 相关性评分 | 关键词命中和来源权重 | 否，质量一般 | 可先规则化 |
| 高质量摘要 | 文章摘要、会议摘要、中文改写 | 是，可选 | 需要调用模型 |
| 交叉主题识别 | 例如 `AI x 医疗健康` 置顶 | 可选 | 规则能做粗筛，模型能减少误判 |
| 日报总述 | 今日重点、趋势线、风险提醒 | 是，可选 | 最适合用模型的环节 |

推荐第一版分两档：

- `SCRIPT_ONLY`：默认模式，不消耗模型 token，稳定生成日报。
- `AI_ENHANCED`：可选模式，只对筛选后的候选内容调用模型，生成摘要、标签、日报总述。

### 6.2 Token 预估

以下只估算运行脚本时调用模型的 token，不包括开发过程中的对话 token。

| 模式 | 假设 | 预计每日 token |
|---|---|---|
| 纯脚本模式 | 不调用模型 | 0 |
| 轻量模型模式 | 60 到 80 条候选；每条只给标题、来源、摘要/片段；再生成日报总述 | 输入约 5 万到 7 万，输出约 6 千到 1 万 |
| 标准模型模式 | 150 到 200 条候选；每条做分类、摘要、标签；再做分组总述 | 输入约 15 万到 22 万，输出约 2 万到 3 万 |
| 重模型模式 | 抓取并压缩正文，100 篇左右，每篇 2000 到 4000 token | 输入约 25 万到 45 万，输出约 2 万到 5 万 |

我的建议：首版先用 `SCRIPT_ONLY` 跑通；后续开启 `AI_ENHANCED` 时，只把规则筛出的 50 到 80 条内容送模型。这样每天 token 可控在约 6 万到 8 万总量级。

## 7. 技术方案

### 7.1 技术栈

推荐首版使用 Python：

- `requests`：请求页面。
- `feedparser`：解析 RSS/Atom。
- `beautifulsoup4`：解析公开 HTML 列表页。
- `pyyaml`：读取信源配置。
- `jinja2`：渲染 HTML/Markdown 模板。
- 标准库 `sqlite3` 或 JSONL：保存历史抓取索引。

如果希望零依赖，也可以只用 Python 标准库，但 HTML 和 RSS 解析会更脆弱，不推荐。

### 7.2 目录结构

```text
ai-health-conference-intel/
  config/
    sources.yaml
    keywords.yaml
  src/
    collectors/
      rss.py
      html_list.py
      github_data.py
    normalize.py
    classify.py
    dedupe.py
    render.py
    run_daily.py
  templates/
    daily.md.j2
    daily.html.j2
  data/
    seen.jsonl
    source-status.json
  output/
    2026-07-02.md
    2026-07-02.html
    2026-07-02.json
  .github/
    workflows/
      daily.yml
```

### 7.3 信源配置模型

```yaml
sources:
  - id: openai_news
    name: OpenAI News
    category_hint: ai
    type: rss_or_html
    url: https://openai.com/news/
    rss_url: https://openai.com/news/rss.xml
    priority: P0
    enabled: true
    rate_limit_seconds: 3
```

字段说明：

- `id`：稳定唯一标识。
- `category_hint`：`ai`、`health`、`conference`。
- `type`：`rss`、`html_list`、`github_yaml`、`search`。
- `url`：官网或列表页。
- `rss_url`：可选；存在则优先 RSS。
- `priority`：P0/P1/P2。
- `enabled`：是否启用。
- `rate_limit_seconds`：同站点请求间隔。

### 7.4 输出数据模型

```json
{
  "id": "sha256:title+url",
  "title": "文章或会议标题",
  "source_id": "openai_news",
  "source_name": "OpenAI News",
  "url": "https://source.example/replace-with-real-item-url",
  "published_at": "2026-07-02T09:30:00+08:00",
  "discovered_at": "2026-07-02T10:00:00+08:00",
  "category": "ai",
  "tags": ["model", "policy"],
  "summary": "一句话摘要。",
  "confidence": 0.82,
  "is_conference": false
}
```

会议记录额外字段：

```json
{
  "event_name": "WAIC 2026",
  "event_start": "2026-07-17",
  "event_end": "2026-07-20",
  "city": "上海",
  "venue": "待解析",
  "organizer": "待解析",
  "deadline_type": "registration",
  "deadline_date": null
}
```

## 8. 分类与去重规则

### 分类

先用信源默认分类，再用关键词修正。

- AI 关键词：`AI`、`人工智能`、`大模型`、`LLM`、`Agent`、`机器人`、`模型`、`算力`、`芯片`、`OpenAI`、`Claude`、`Gemini`。
- 医疗健康关键词：`医疗`、`健康`、`医院`、`药品`、`器械`、`医保`、`临床`、`指南`、`疾病`、`公共卫生`、`数字医疗`。
- 会议关键词：`大会`、`会议`、`论坛`、`峰会`、`年会`、`征文`、`报名`、`日程`、`参会`、`举办`。

### 去重

首版使用三层去重：

1. URL 完全一致。
2. 标题标准化后完全一致。
3. 标题相似度超过阈值，例如 0.88。

保留多来源信息时，日报只显示主记录，但附上“其他来源”链接。

## 9. GitHub Actions 设计

```yaml
name: Daily Intelligence

on:
  schedule:
    - cron: "0 23 * * *"
  workflow_dispatch:

jobs:
  daily:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: python -m src.run_daily --days 2 --output-dir output
      - run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add output data
          git commit -m "chore: update daily intelligence" || echo "No changes"
          git push
```

时间说明：`23:00 UTC` 等于北京时间次日 `07:00`。如果要北京时间每天早上 8 点生成，可改成 `0 0 * * *`。

## 10. 本地运行设计

PowerShell 示例：

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
python -m src.run_daily --days 2 --output-dir output
```

输出后直接打开：

```text
output/YYYY-MM-DD.html
```

## 11. 错误处理

- 单个信源失败：记录到 `data/source-status.json`，不阻断日报。
- 页面结构变化：保留错误摘要，日报底部列出失败源。
- 时间解析失败：使用 `discovered_at`，并标记 `published_at_missing`。
- 内容太少：保留空日报，并提示“今日未发现新内容或抓取失败”。
- 请求失败：最多重试 2 次，指数退避。

## 12. 合规与风险

| 风险 | 处理 |
|---|---|
| 抓取违反站点规则 | 优先 RSS/公开页面，低频请求；必要时关闭该源 |
| 医疗内容被误解为建议 | 日报声明“仅资讯摘要，非医疗建议” |
| 文章版权风险 | 不存全文，不转载长段落，只保留短摘要和链接 |
| GitHub 泄露密钥 | 首版不需要密钥；后续密钥只放 Secrets |
| 页面结构频繁变动 | 每个 HTML 源单独适配，失败不影响全局 |
| 噪声过多 | P0 信源先跑，P1/P2 分阶段加入 |
| 社交平台账号风险 | 不使用个人登录态自动化；优先官方 API 或人工种子链接 |
| API 成本失控 | API 和模型调用默认关闭，设置每日最大条数和最大 token |

## 13. 验收标准

- 可以本地运行并生成当天 Markdown、HTML、JSON 三类文件。
- 至少 10 个 P0/P1 信源启用，其中包括：
  - AI 官方/研究源不少于 3 个。
  - 医疗健康官方源不少于 3 个。
  - 国内会议源不少于 3 个。
- 每条记录包含标题、来源、链接、分类、发现时间。
- 单个信源失败时，脚本仍能完成。
- 重复标题不会在日报主体重复出现。
- GitHub Actions 配置可手动触发并生成输出。

## 14. 推荐实施路线

### 阶段 1：本地最小可用版

- 配置 10 到 12 个 P0/P1 信源。
- 支持 RSS + HTML 列表页。
- 输出 Markdown/HTML/JSON。
- 保存历史去重文件。

### 阶段 2：GitHub Actions

- 添加 workflow。
- 自动提交 `output/` 和 `data/`。
- 可选开启 GitHub Pages 展示 HTML。

### 阶段 3：质量增强

- 增加会议日期结构化解析。
- 增加 LLM 摘要或关键词打标。
- 增加邮件、飞书、企微推送。
- 增加源健康报告。

## 15. 待评审问题

1. 首版是否只启用 P0 源，还是直接加入部分 P1 中文媒体？
2. 日报输出是否需要直接发邮件/飞书，还是先只落本地和 GitHub 文件？
3. 会议范围是否只要国内线下会议，还是包括国内主办的线上会议？
4. 医疗健康资讯是否更偏政策/产业，还是也包含临床研究和指南？
5. 是否需要把“AI + 医疗健康”交叉内容单独置顶，例如医疗 AI、AI 制药、医院 AI 应用？
6. 社交媒体是否第一版只做配置占位，第二版再接 X API/小红书/公众号？
7. 模型增强是否默认关闭，仅在日报质量不够时再开启？

## 16. 我的推荐

首版采用：

- GitHub Actions + 本地落文件双模式。
- 先启用 P0 信源，加少量 P1 中文源。
- 输出 Markdown、HTML、JSON，不先接推送。
- 单独置顶 `AI x 医疗健康` 交叉内容。

原因：这样可以最快得到稳定日报，同时保留后续上 GitHub Pages、邮件、飞书/企微推送的空间。
