# X / Twitter API 接入说明

## 当前结论

X 对开发者 API 采用 pay-per-use 的信用额度计费方式，不再按固定订阅作为唯一入口。实际消耗与 endpoint、返回资源量和 Developer Console 中的当前价格有关，因此本项目默认关闭 X 源，避免误产生费用。

## 获取 API

1. 打开 X Developer Platform。
2. 注册或登录开发者账号。
3. 创建 Project / App。
4. 在 Developer Console 的 Keys and tokens 中复制 Bearer Token。
5. 在 GitHub 仓库中添加 Secret：
   - Name: `X_BEARER_TOKEN`
   - Value: 你的 Bearer Token
6. 修改 `config/sources.yaml`，把 `x_ai_health.enabled` 改为 `true`。

## 本项目如何使用

默认使用 Recent Search endpoint：

```text
GET https://api.x.com/2/tweets/search/recent
```

配置项：

```yaml
  - id: x_ai_health
    type: x_recent_search
    query: "(AI OR artificial intelligence OR 大模型) (health OR 医疗 OR 医院 OR 药物) -is:retweet lang:zh"
    enabled: false
    max_results: 25
```

## 成本控制

- `enabled: false` 是默认值。
- `max_results` 默认 25，最高限制在 100。
- 不在代码里保存 Bearer Token，只从环境变量或 GitHub Secrets 读取。
- 建议先在 Developer Console 设置预算/支出限制，再开启定时任务。

## 计费理解

按官方文档，X API 采用购买 credits、按请求/资源消耗的方式计费。官方概览页提到 X API 是 pay-per-use，getting started pricing 页说明 credits 会随 API request 扣减。具体到 Recent Search 返回 posts 的单价，建议以 Developer Console 当前报价为准，因为 X 的开发者产品和价格在 2025-2026 年变化较频繁。
