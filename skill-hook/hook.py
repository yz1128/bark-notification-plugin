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
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
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

        # 提取项目目录作为上下文
        cwd = hook_data.get("cwd", "")
        project_name = os.path.basename(cwd) if cwd else "ClaudeCode"

        # 获取最后一条消息作为 session 名称
        last_message = hook_data.get("last_assistant_message", "")

        # 截取前50个字符作为任务描述
        task_desc = ""
        if last_message:
            # 提取第一行或前50个字符
            first_line = last_message.split('\n')[0]
            task_desc = first_line[:50] + "..." if len(first_line) > 50 else first_line

        if not task_desc:
            task_desc = "任务处理中"

    except (json.JSONDecodeError, Exception):
        # 如果没有 JSON 输入，使用默认值
        hook_event = "unknown"
        project_name = "ClaudeCode"
        task_desc = "任务处理中"

    # 标题：当前 agent 名称
    title = project_name

    # 内容：会话名称 + 状态
    body = f"🤖 {task_desc}\n✅ 任务完成"

    # 发送推送
    try:
        result = send_bark(
            device_key,
            title,
            body,
            group="claude",
            sound="minuet",
            is_archive=1,
            icon="https://cdn.jsdelivr.net/gh/yz1128/MyImageRepository@main/image/20260613092240368.png"
        )
        # 无论成功失败都静默退出，不影响 Claude 正常工作
        sys.exit(0)
    except Exception:
        # 失败也静默退出
        sys.exit(0)


if __name__ == "__main__":
    main()
