"""Optional notification helpers.

No credentials are stored in source code. Set SLACK_BOT_TOKEN and
SLACK_CHANNEL locally when Slack notifications are needed.
"""

from __future__ import annotations

import os

import requests


def notify_stock_signal(message: str) -> bool:
    token = os.getenv("SLACK_BOT_TOKEN")
    channel = os.getenv("SLACK_CHANNEL", "#stock")
    if not token:
        return False

    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={"Authorization": f"Bearer {token}"},
        json={"channel": channel, "text": message},
        timeout=10,
    )
    response.raise_for_status()
    payload = response.json()
    return bool(payload.get("ok"))
