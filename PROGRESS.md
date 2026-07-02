# PROGRESS.md

## 2026-07-02

- 启动 AI/医疗健康/国内会议每日情报脚本项目。
- 已确认当前工作区顶层不是 git 仓库，因此首版设计需同时支持：
  - 推到 GitHub 后用 GitHub Actions 定时运行。
  - 不上 GitHub 时在本地运行并落文件。
- 已调研 GitHub 参考项目：
  - `LearnPrompt/ai-news-radar`：适合作为轻量 RSS/公开页面/JSON 到静态数据的管道参考。
  - `sansan0/TrendRadar`：适合作为多渠道推送和热点监控参考，但首版不建议照搬。
  - `zhaoolee/garss`：适合作为中文 RSS 聚合与 GitHub Actions 采集参考。
  - 若干 AI 日报项目：适合作为邮件摘要和定时任务参考。
- 根据评审补充方向，文档新增：
  - X / Twitter、小红书、微信公众号等社交媒体来源边界。
  - 普通脚本与模型调用的职责边界。
  - 模型增强模式的每日 token 预估。

### 决策：首版采用轻量脚本而非完整平台

**背景**：需求是每天获取三类情报，而不是建设复杂舆情系统。  
**选项**：完整 Web 平台、多渠道推送平台、轻量脚本。  
**决定**：首版采用轻量 Python 脚本 + 文件输出 + 可选 GitHub Actions。  
**原因**：上线快、可审计、维护成本低，后续可平滑扩展邮件/飞书/企微。  
**影响**：首版不做后台 UI、不做登录、不做实时监控。

### 决策：社交媒体默认作为后续增强源

**背景**：咕咕希望补充 X / Twitter、小红书、微信公众号等社交媒体来源。  
**选项**：直接模拟人工抓取、使用官方/合规 API、先保留人工种子链接。  
**决定**：首版不使用个人登录态自动化；X 预留官方 API；小红书和公众号先支持人工链接或合规数据服务。  
**原因**：社交平台反爬和条款风险高，GitHub Actions 不适合跑个人登录态模拟操作。  
**影响**：首版社交媒体覆盖不作为核心验收，第二阶段再按具体 API/服务接入。

### 决策：模型调用默认关闭

**背景**：需要明确哪些环节用模型，以及每日 token 成本。  
**选项**：全流程用模型、只在摘要/总述用模型、完全不用模型。  
**决定**：首版默认 `SCRIPT_ONLY`，模型增强作为可选 `AI_ENHANCED` 模式。  
**原因**：采集、解析、去重、渲染都能用普通脚本完成；模型最适合做摘要、标签和日报总述。  
**影响**：首版运行 token 为 0；开启轻量模型增强后预计每日总 token 约 6 万到 8 万。

## 下一步

- 配置 GitHub Secrets：`X_BEARER_TOKEN` 和可选 `DEEPSEEK_API_KEY`。
- 根据实际抓取质量调整 `config/sources.yaml`。
- 若需要模型增强，运行时加 `--enhance` 并观察 token/费用。

## 2026-07-02 实现进展

- 新增 Python 包 `everydaynews`。
- 新增核心模块：
  - `models.py`：Source、NewsItem、SourceStatus。
  - `classifier.py`：关键词分类与 `ai_health` 交叉标签。
  - `dedupe.py`：URL 和标题去重。
  - `render.py`：Markdown/HTML/JSON 输出。
  - `run_daily.py`：CLI 入口。
- 新增采集器：
  - RSS。
  - HTML 列表页。
  - static 测试源。
  - X Recent Search，默认关闭。
- 新增可选增强：
  - DeepSeek Chat Completions 调用，默认关闭。
- 新增 GitHub Actions：`.github/workflows/daily.yml`。
- 新增测试 7 个，覆盖分类、去重、渲染、X API 解析、DeepSeek prompt、CLI 输出。
