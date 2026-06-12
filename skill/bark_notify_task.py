#!/usr/bin/env python3
"""
Bark Notify Task Wrapper
在命令执行完成后发送 Bark 通知
"""

import os
import sys
import subprocess
import time
from bark_send import send_bark


def main():
    if len(sys.argv) < 2:
        print("用法: bark_notify_task <command> [args...]", file=sys.stderr)
        print("", file=sys.stderr)
        print("示例:", file=sys.stderr)
        print("  bark_notify_task npm test", file=sys.stderr)
        print("  bark_notify_task make build", file=sys.stderr)
        sys.exit(1)

    device_key = os.environ.get("BARK_DEVICE_KEY")
    if not device_key:
        print("⚠️  警告: BARK_DEVICE_KEY 未设置，任务完成后不会发送通知", file=sys.stderr)
        # 仍然执行命令，只是不推送
        device_key = None

    # 执行命令
    cmd = sys.argv[1:]
    cmd_str = " ".join(cmd)

    print(f"🚀 执行任务: {cmd_str}")
    print("=" * 60)

    start_time = time.time()

    try:
        result = subprocess.run(cmd, check=False)
        exit_code = result.returncode
    except Exception as e:
        print(f"❌ 执行失败: {e}", file=sys.stderr)
        exit_code = 1

    elapsed = time.time() - start_time
    elapsed_str = f"{int(elapsed)}秒" if elapsed < 60 else f"{int(elapsed/60)}分{int(elapsed%60)}秒"

    print("=" * 60)

    # 发送通知
    if device_key:
        if exit_code == 0:
            title = "✅ 任务成功"
            body = f"{cmd_str}\n用时: {elapsed_str}"
            sound = "minuet"
        else:
            title = "❌ 任务失败"
            body = f"{cmd_str}\n退出码: {exit_code}\n用时: {elapsed_str}"
            sound = "alarm"

        try:
            print(f"\n📤 发送推送通知...")
            send_bark(device_key, title, body, group="task", sound=sound)
            print("✅ 通知已发送")
        except Exception as e:
            print(f"⚠️  通知发送失败: {e}", file=sys.stderr)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
