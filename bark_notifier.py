#!/usr/bin/env python3
"""
DeepSeek Token Monitor → Bark 推送 (GitHub Actions 版)
每小时自动运行，不依赖本地电脑在线
"""

import os
import sys
from datetime import datetime

import requests

# ── Config (从 GitHub Secrets 读取) ──────────────────────
DEEPSEEK_API_KEY = os.environ["DEEPSEEK_API_KEY"]
BARK_URL = os.environ["BARK_URL"]


def get_balance():
    resp = requests.get(
        "https://api.deepseek.com/user/balance",
        headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}"},
        timeout=15,
    )
    data = resp.json()
    if not resp.ok:
        msg = data.get("error", {}).get("message", f"HTTP {resp.status_code}")
        raise RuntimeError(msg)
    return [
        {
            "currency": b.get("currency", "?"),
            "total": float(b.get("total_balance", 0)),
            "granted": float(b.get("granted_balance", 0)),
            "topped_up": float(b.get("topped_up_balance", 0)),
        }
        for b in data.get("balance_infos", [])
    ]


def send_bark(title, body):
    payload = {
        "title": title,
        "body": body,
        "sound": "birdsong",
        "group": "DeepSeek",
        "icon": "https://cdn.deepseek.com/logo.png",
    }
    resp = requests.post(BARK_URL, json=payload, timeout=10)
    return resp.ok


def main():
    try:
        balances = get_balance()
        total = sum(b["total"] for b in balances)

        title = f"DeepSeek 余额 ¥{total:.2f}"

        now_str = datetime.now().strftime("%m/%d %H:%M")
        body = now_str
        for b in balances:
            body += f"  |  {b['currency']} {b['total']:.4f}"
            if b.get("granted"):
                body += f" (赠送 {b['granted']:.2f})"

        ok = send_bark(title, body)
        status = "✅" if ok else "⚠️"
        print(f"{status} {title}")

    except Exception as e:
        print(f"❌ {e}", file=sys.stderr)
        send_bark("DeepSeek ⚠️ 查询失败", str(e))


if __name__ == "__main__":
    main()
