#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bark Notify Hook - 自动在任务完成时发送推送
监听 Stop 事件，从 stdin 接收 JSON 参数
"""

import os
import sys
import json

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

    # 读取 hook 传入的 JSON 参数（从 stdin）
    try:
        hook_data = json.load(sys.stdin)
        hook_event = hook_data.get("hook_event_name", "unknown")
        session_id = hook_data.get("session_id", "")

        # 提取项目目录作为上下文
        cwd = hook_data.get("cwd", "")
        project_name = os.path.basename(cwd) if cwd else "Claude"

    except (json.JSONDecodeError, Exception):
        # 如果没有 JSON 输入，使用默认值
        hook_event = "unknown"
        project_name = "Claude"

    # 标题
    title = f"{project_name} 任务完成"

    # 内容：从命令行参数获取，或使用默认
    if len(sys.argv) > 1:
        body = " ".join(sys.argv[1:])
    else:
        body = "✅ 任务已完成，可以查看结果"

    # 发送推送
    try:
        result = send_bark(
            device_key,
            title,
            body,
            group="claude",
            sound="minuet",
            is_archive=1
        )
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
