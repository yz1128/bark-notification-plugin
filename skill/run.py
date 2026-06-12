#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bark Notify Skill Runner
Claude Code skill 接口
"""

import os
import sys

# 获取 skill 目录
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SKILL_DIR)

from bark_send import send_bark


def main():
    """
    处理来自 Claude Code 的调用

    支持的命令格式:
    1. bark-notify "标题"
    2. bark-notify "标题" "内容"
    3. bark-notify "标题" "内容" --group xxx --sound xxx
    """
    if len(sys.argv) < 2:
        print("📱 Bark Notify Skill")
        print("")
        print("用法:")
        print("  /bark-notify <title> [body] [options]")
        print("")
        print("示例:")
        print("  /bark-notify '任务完成'")
        print("  /bark-notify '测试通过' '所有 127 个测试用例已通过'")
        print("  /bark-notify '部署成功' 'v2.1.0 已上线' --group deploy")
        print("")
        print("选项:")
        print("  --group <name>   分组名称 (默认: claude)")
        print("  --sound <name>   铃声名称 (默认: minuet)")
        print("  --url <url>      点击通知后打开的 URL")
        print("")
        return 0

    device_key = os.environ.get("BARK_DEVICE_KEY")
    if not device_key:
        print("❌ 错误: BARK_DEVICE_KEY 未设置")
        print("")
        print("请在 ~/.claude/settings.json 的 env 中添加:")
        print('  "BARK_DEVICE_KEY": "your_device_key_here"')
        print("")
        print("获取 device key: 打开 Bark App -> 复制推送 URL 中的 key")
        return 1

    # 解析参数
    args = sys.argv[1:]
    title = args[0] if len(args) > 0 else "通知"
    body = ""
    group = "claude"
    sound = "minuet"
    url = None

    # 简单参数解析
    i = 1
    while i < len(args):
        arg = args[i]
        if arg.startswith("--"):
            if arg == "--group" and i + 1 < len(args):
                group = args[i + 1]
                i += 2
            elif arg == "--sound" and i + 1 < len(args):
                sound = args[i + 1]
                i += 2
            elif arg == "--url" and i + 1 < len(args):
                url = args[i + 1]
                i += 2
            else:
                i += 1
        else:
            # 第一个非选项参数是 body
            if not body:
                body = arg
            i += 1

    # 发送通知
    try:
        print(f"📤 正在发送推送...")
        print(f"   标题: {title}")
        if body:
            preview = body[:60] + "..." if len(body) > 60 else body
            print(f"   内容: {preview}")
        print(f"   分组: {group}")

        kwargs = {"group": group, "sound": sound}
        if url:
            kwargs["url"] = url
            print(f"   链接: {url}")

        result = send_bark(device_key, title, body, **kwargs)

        if result.get("code") == 200:
            print("")
            print("✅ 推送发送成功！")
            print("   请查看你的 iPhone Bark 通知")
            return 0
        else:
            print("")
            print(f"⚠️  API 响应: {result}")
            return 1

    except Exception as e:
        print("")
        print(f"❌ 发送失败: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
