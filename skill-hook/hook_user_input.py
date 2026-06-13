#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bark Notify User Input Hook
用户输入请求时发送推送提醒
"""

import os
import sys
import json

# 获取 skill 目录
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SKILL_DIR)

try:
    from bark_send import send_bark
except ImportError:
    # 静默退出
    sys.exit(0)


def main():
    device_key = os.environ.get("BARK_DEVICE_KEY")
    if not device_key:
        # 静默退出
        sys.exit(0)

    # 读取 hook 传入的 JSON 参数（从 stdin）
    try:
        hook_data = json.load(sys.stdin)
        session_id = hook_data.get("session_id", "unknown")
        # 提取问题或提示信息（如果有）
        question = hook_data.get("question", "")

    except (json.JSONDecodeError, Exception):
        # 如果没有 JSON 输入，使用默认值
        session_id = "unknown"
        question = ""

    # 标题：固定为 Claude Code
    title = "Claude Code"

    # 内容：session_id + 状态
    if question:
        body = f"🆔 {session_id}\n💬 等待输入\n\n{question[:100]}"
    else:
        body = f"🆔 {session_id}\n💬 等待输入"

    # 发送推送（使用提醒设置）
    try:
        result = send_bark(
            device_key,
            title,
            body,
            group="claude-input",
            sound="bell",           # 使用清脆的铃声
            level="timeSensitive",  # 时效性通知
            is_archive=0,           # 不归档，需要立即处理
            icon="https://cdn.jsdelivr.net/gh/yz1128/MyImageRepository@main/image/20260613092240368.png"
        )
        if result.get("code") == 200:
            sys.exit(0)
        else:
            sys.exit(1)
    except Exception:
        sys.exit(1)


if __name__ == "__main__":
    main()
