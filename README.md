# Everyday News

AI、医疗健康资讯和国内会议的每日情报采集项目。

当前已经有第一版可运行脚本：支持公开 RSS/网页采集、本地日报输出、GitHub Actions 定时运行、可选 X API 和 DeepSeek 增强。

## 文档

- [需求与技术评审](docs/requirements-technical-review.md)
- [X API 接入说明](docs/x-api.md)
- [项目规则](CLAUDE.md)
- [进度记录](PROGRESS.md)
- [记忆索引](MEMORY.md)

## 当前方向

- 支持 GitHub Actions 定时运行。
- 支持本地运行并落 Markdown、HTML、JSON 文件。
- 首版优先使用公开 RSS、公开网页和公开数据文件。
- X API 已预留 Recent Search 采集器，默认关闭。
- DeepSeek 摘要增强已预留，默认关闭。

## 本地运行

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
python -m everydaynews.run_daily --days 2 --output-dir output --max-items 200
```

输出：

- `output/YYYY-MM-DD.md`
- `output/YYYY-MM-DD.html`
- `output/YYYY-MM-DD.json`
- `data/source-status.json`

默认采集会保留原文标题。要让报告主体变成中文标题和中文摘要，请配置 `DEEPSEEK_API_KEY` 后运行：

```powershell
$env:DEEPSEEK_API_KEY="你的 DeepSeek API Key"
python -m everydaynews.run_daily --days 2 --output-dir output --max-items 80 --enhance
```

GitHub Actions 已默认加 `--enhance`；如果仓库没有配置 `DEEPSEEK_API_KEY`，脚本会自动跳过模型增强，不产生 token 费用。

## 可选环境变量

- `X_BEARER_TOKEN`：开启 X Recent Search 时需要。
- `DEEPSEEK_API_KEY`：运行 `--enhance` 时需要。

## 测试

```powershell
python -m unittest discover -s tests -v
```
