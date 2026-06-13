#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bark Notify Permission Request Hook
权限请求时发送推送提醒
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

        # 提取工具信息
        tool_name = hook_data.get("tool_name", "未知工具")

        # 提取项目目录作为上下文
        cwd = hook_data.get("cwd", "")
        project_name = os.path.basename(cwd) if cwd else "ClaudeCode"

    except (json.JSONDecodeError, Exception):
        # 如果没有 JSON 输入，使用默认值
        tool_name = "未知操作"
        project_name = "ClaudeCode"

    # 标题：Agent 名称
    title = project_name

    # 内容：操作描述 + 状态
    body = f"🔐 {tool_name}\n⚠️ 权限请求"

    # 发送推送（使用更紧急的设置）
    try:
        result = send_bark(
            device_key,
            title,
            body,
            group="claude-permission",
            sound="alarm",          # 使用警报铃声
            level="timeSensitive",  # 时效性通知
            is_archive=0,           # 不归档，需要立即处理
            icon="https://cdn.jsdelivr.net/gh/yz1128/MyImageRepository@main/image/20260613092240368.png"
        )
        # 无论成功失败都静默退出
        sys.exit(0)
    except Exception:
        sys.exit(0)


if __name__ == "__main__":
    main()
