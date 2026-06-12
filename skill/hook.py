#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bark Notify Hook - 自动在会话结束时发送推送
从环境变量或最后的 AI 响应中提取内容并推送
"""

import os
import sys

# 获取 skill 目录
SKILL_DIR = os.path.expanduser("~/.claude/skills/bark-notify")
sys.path.insert(0, SKILL_DIR)

try:
    from bark_send import send_bark
except ImportError:
    print("Error: Cannot import bark_send module", file=sys.stderr)
    sys.exit(1)


def main():
    device_key = os.environ.get("BARK_DEVICE_KEY")
    if not device_key:
        # 静默退出，不打扰用户
        sys.exit(0)

    # 标题
    title = "Claude 任务完成"

    # 内容：从命令行参数获取，或使用默认
    if len(sys.argv) > 1:
        body = " ".join(sys.argv[1:])
    else:
        body = "✅ 任务已完成"

    # 发送推送
    try:
        result = send_bark(device_key, title, body, group="claude", sound="minuet")
        if result.get("code") == 200:
            # 成功，静默
            sys.exit(0)
        else:
            # 失败，静默
            sys.exit(1)
    except Exception:
        # 失败，静默
        sys.exit(1)


if __name__ == "__main__":
    main()
