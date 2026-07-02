# MEMORY.md

- 项目目标：每天自动收集 AI、医疗健康资讯和国内会议信息，生成结构化日报。
- 当前阶段：需求/技术评审，未开始写脚本实现。
- 首版倾向：Python 脚本、本地 Markdown/HTML/JSON 输出、可选 GitHub Actions 定时运行。
- 合规边界：只抓公开页面/RSS/公开 JSON，不登录、不绕反爬、不全文转载。
- GitHub 仓库目标：https://github.com/hellogugu1011-beep/everydaynews.git
- 社交媒体边界：X 预留官方 API；小红书/微信公众号默认不做登录态模拟抓取，优先人工种子链接、已授权 API 或合规数据服务。
- 模型边界：首版默认纯脚本 0 token；可选 DeepSeek 增强用于摘要、标签、交叉主题识别和日报总述，轻量模式预计每日 6 万到 8 万 token，按 deepseek-chat 约 ¥0.15-¥0.22/天。
- 待确认：首版信源清单、输出渠道、是否第一版接入任何社交媒体 API。
