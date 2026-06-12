#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bark Push Notification Sender
发送 iOS Bark 推送通知
"""

import os
import sys
import json
import urllib.request
import urllib.parse
import ssl
import argparse
import io

# Windows 环境下设置 stdout 编码为 UTF-8
if sys.platform == 'win32':
    if hasattr(sys.stdout, 'buffer') and sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
    if hasattr(sys.stderr, 'buffer') and sys.stderr.encoding != 'utf-8':
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', line_buffering=True)


def send_bark(device_key: str, title: str, body: str = "", **kwargs):
    """
    发送 Bark 推送通知

    Args:
        device_key: Bark 设备密钥
        title: 通知标题
        body: 通知内容
        **kwargs: 其他参数 (group, sound, url, icon, badge, isArchive)

    Returns:
        dict: API 响应
    """
    url = f"https://api.day.app/{device_key}"

    payload = {
        "title": title,
        "body": body or "✅ 任务已完成",
    }

    # 添加可选参数
    if "group" in kwargs:
        payload["group"] = kwargs["group"]
    else:
        payload["group"] = "claude"

    if "sound" in kwargs:
        payload["sound"] = kwargs["sound"]
    else:
        payload["sound"] = "minuet"

    if "url" in kwargs:
        payload["url"] = kwargs["url"]

    if "icon" in kwargs:
        payload["icon"] = kwargs["icon"]

    if "badge" in kwargs:
        payload["badge"] = int(kwargs["badge"])

    if "level" in kwargs:
        payload["level"] = kwargs["level"]

    # 支持 isArchive 和 is_archive 两种形式
    if "isArchive" in kwargs:
        payload["isArchive"] = int(kwargs["isArchive"])
    elif "is_archive" in kwargs:
        payload["isArchive"] = int(kwargs["is_archive"])
    else:
        payload["isArchive"] = 1  # 默认归档

    # 创建 SSL 上下文
    ctx = ssl.create_default_context()

    # 准备请求
    payload_bytes = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload_bytes,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        raise Exception(f"HTTP {e.code}: {error_body}")
    except Exception as e:
        raise Exception(f"Failed to send notification: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="发送 Bark iOS 推送通知",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s "任务完成"
  %(prog)s "编译完成" "所有测试通过"
  %(prog)s "部署成功" "v2.1.0 已上线" --group deploy --sound bell
  %(prog)s "PR 已创建" --url "https://github.com/user/repo/pull/123"
        """
    )

    parser.add_argument("title", help="通知标题")
    parser.add_argument("body", nargs="?", default="", help="通知内容（可选）")
    parser.add_argument("--group", default="claude", help="分组名称 (默认: claude)")
    parser.add_argument("--sound", default="minuet", help="铃声 (默认: minuet)")
    parser.add_argument("--url", help="点击通知后打开的 URL")
    parser.add_argument("--icon", help="自定义图标 URL")
    parser.add_argument("--badge", type=int, help="角标数字")
    parser.add_argument("--no-archive", action="store_true", help="不归档此通知")
    parser.add_argument("--device-key", help="Bark 设备密钥（默认从环境变量读取）")

    args = parser.parse_args()

    # 获取 device key
    device_key = args.device_key or os.environ.get("BARK_DEVICE_KEY")
    if not device_key:
        print("❌ 错误: 未设置 BARK_DEVICE_KEY", file=sys.stderr)
        print("", file=sys.stderr)
        print("请设置环境变量或使用 --device-key 参数:", file=sys.stderr)
        print("  export BARK_DEVICE_KEY=your_key", file=sys.stderr)
        print("  或在 ~/.claude/settings.json 中配置", file=sys.stderr)
        sys.exit(1)

    # 准备参数
    kwargs = {
        "group": args.group,
        "sound": args.sound,
        "isArchive": 0 if args.no_archive else 1,
    }

    if args.url:
        kwargs["url"] = args.url
    if args.icon:
        kwargs["icon"] = args.icon
    if args.badge is not None:
        kwargs["badge"] = args.badge

    # 发送通知
    try:
        print(f"📤 发送推送: {args.title}")
        if args.body:
            print(f"   内容: {args.body[:50]}{'...' if len(args.body) > 50 else ''}")

        result = send_bark(device_key, args.title, args.body, **kwargs)

        if result.get("code") == 200:
            print("✅ 推送发送成功")
            if args.url:
                print(f"   链接: {args.url}")
            return 0
        else:
            print(f"⚠️  API 返回: {result}", file=sys.stderr)
            return 1

    except Exception as e:
        print(f"❌ 发送失败: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
