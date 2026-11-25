# some milk · DeepSeek 余额监控

每小时查一次 DeepSeek 账户余额，用 [Bark](https://github.com/Finb/Bark) 推到 iPhone。跑在 GitHub Actions 上，不需要本地电脑开着。

## 它做什么

- 每小时第 7 分钟（UTC）自动跑一次，也可以手动触发；
- 调 `https://api.deepseek.com/user/balance`，按币种汇总总额、赠送、充值；
- 推一条通知：标题是总额，正文带每个币种的明细；
- **查询失败也会推一条 ⚠️**，不会静默失败——余额查不到本身就是要知道的事。

## 用起来

1. Fork 或 clone 这个仓库；
2. 在 **Settings → Secrets and variables → Actions** 里加两个 secret：
   - `DEEPSEEK_API_KEY`：DeepSeek 平台创建的 API key；
   - `BARK_URL`：形如 `https://api.day.app/<你的 key>/`；
3. 到 **Actions → DeepSeek Token Monitor → Run workflow** 手动跑一次，确认能收到推送。

## 文件

```text
bark_notifier.py                         查余额 + 推送的全部逻辑
.github/workflows/token-monitor.yml      定时任务
```

本地跑：

```bash
DEEPSEEK_API_KEY=sk-xxx BARK_URL=https://api.day.app/xxx/ python bark_notifier.py
```

## 注意

- 只读余额接口，不会改动账户里的任何东西；
- 密钥只放在 GitHub Secrets，不进仓库、不进日志；
- 仓库连续 60 天没有提交时，GitHub 会自动停用定时任务，偶尔手动跑一次就能续上。

## License

MIT