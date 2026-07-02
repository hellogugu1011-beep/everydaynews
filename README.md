# Everyday News

AI、医疗健康资讯和国内会议的每日情报采集项目。

当前阶段是需求与技术评审，尚未进入脚本实现。

## 文档

- [需求与技术评审](docs/requirements-technical-review.md)
- [项目规则](CLAUDE.md)
- [进度记录](PROGRESS.md)
- [记忆索引](MEMORY.md)

## 当前方向

- 支持 GitHub Actions 定时运行。
- 支持本地运行并落 Markdown、HTML、JSON 文件。
- 首版优先使用公开 RSS、公开网页和公开数据文件。
- 社交媒体默认作为后续增强源，不使用个人登录态自动化。
- 模型调用默认关闭，先用普通脚本跑通采集、分类、去重和日报渲染。
