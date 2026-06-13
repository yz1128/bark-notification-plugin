#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bark Notify Hook Skill Runner
自动安装/卸载 Stop hook
"""

import os
import sys
import json
import shutil
from datetime import datetime

# Windows 环境下设置 stdout 编码为 UTF-8
if sys.platform == 'win32':
    import io
    if hasattr(sys.stdout, 'buffer') and sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
    if hasattr(sys.stderr, 'buffer') and sys.stderr.encoding != 'utf-8':
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', line_buffering=True)

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.expanduser("~/.claude/settings.json")
HOOK_SESSION_END = "python ~/.claude/skills/bark-notify-hook/hook.py"
HOOK_PERMISSION = "python ~/.claude/skills/bark-notify-hook/hook_permission.py"
HOOK_USER_INPUT = "python ~/.claude/skills/bark-notify-hook/hook_user_input.py"

# 所有需要安装的 hooks
HOOKS_CONFIG = {
    "Stop": {
        "command": HOOK_SESSION_END,
        "description": "回复完成"
    },
    "PermissionRequest": {
        "command": HOOK_PERMISSION,
        "description": "权限请求"
    },
    "Elicitation": {
        "command": HOOK_USER_INPUT,
        "description": "用户输入请求"
    }
}


def backup_settings():
    """备份 settings.json"""
    if os.path.exists(SETTINGS_FILE):
        backup_file = f"{SETTINGS_FILE}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(SETTINGS_FILE, backup_file)
        print(f"✅ 已备份配置文件: {backup_file}")
        return backup_file
    return None


def load_settings():
    """加载 settings.json"""
    if not os.path.exists(SETTINGS_FILE):
        return {}

    try:
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ 读取配置文件失败: {e}")
        return None


def save_settings(settings):
    """保存 settings.json"""
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)

        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"❌ 保存配置文件失败: {e}")
        return False


def is_hook_installed(settings):
    """检查所有 hooks 是否已安装"""
    if not settings or 'hooks' not in settings:
        return

    hooks = settings.get('hooks', {})
    installed = {}

    for hook_event, hook_config in HOOKS_CONFIG.items():
        hook_command = hook_config["command"]
        is_installed = False

        event_hooks = hooks.get(hook_event, [])
        for item in event_hooks:
            for hook in item.get('hooks', []):
                if hook.get('command') == hook_command:
                    is_installed = True
                    break
            if is_installed:
                break

        installed[hook_event] = is_installed

    return installed


def install_hook():
    """安装所有交互相关的 hooks"""
    print("📦 正在安装 Bark Notify Hooks...")
    print("")

    # 备份
    backup_settings()

    # 加载配置
    settings = load_settings()
    if settings is None:
        return False

    # 检查是否已安装
    installed = is_hook_installed(settings)
    if not installed:
        print("❌ 无法读取配置状态")
        return False

    all_installed = all(installed.values())
    if all_installed:
        print("⚠️  所有 Hooks 已安装，无需重复安装")
        return True

    # 添加 hooks
    if 'hooks' not in settings:
        settings['hooks'] = {}

    # 遍历安装每个 hook
    for hook_event, hook_config in HOOKS_CONFIG.items():
        if not installed[hook_event]:
            if hook_event not in settings['hooks']:
                settings['hooks'][hook_event] = []

            settings['hooks'][hook_event].append({
                "hooks": [
                    {
                        "type": "command",
                        "command": hook_config["command"]
                    }
                ]
            })
            print(f"✅ {hook_event} ({hook_config['description']}) hook 已添加")

    # 保存
    if save_settings(settings):
        print("")
        print("✅ Hooks 安装成功！")
        print("")
        print("功能说明：")
        print("  📱 回复完成时 → 自动发送完成通知")
        print("  ⚠️  权限请求时 → 紧急提醒需要确认")
        print("  💬 需要输入时 → 提醒返回终端回答")
        print("")
        print("下一步：")
        print("  1. 确保已配置 BARK_DEVICE_KEY")
        print("  2. 运行 /bark-notify-hook test 测试推送")
        return True

    return False


def uninstall_hook():
    """卸载所有 hooks"""
    print("🗑️  正在卸载 Bark Notify Hooks...")
    print("")

    # 备份
    backup_settings()

    # 加载配置
    settings = load_settings()
    if settings is None:
        return False

    # 检查是否已安装
    installed = is_hook_installed(settings)
    if not installed:
        print("❌ 无法读取配置状态")
        return False

    any_installed = any(installed.values())
    if not any_installed:
        print("⚠️  Hooks 未安装，无需卸载")
        return True

    # 遍历移除每个 hook
    for hook_event, hook_config in HOOKS_CONFIG.items():
        if installed[hook_event] and 'hooks' in settings and hook_event in settings['hooks']:
            new_hooks = []
            for item in settings['hooks'][hook_event]:
                item_hooks = []
                for hook in item.get('hooks', []):
                    if hook.get('command') != hook_config["command"]:
                        item_hooks.append(hook)

                if item_hooks:
                    item['hooks'] = item_hooks
                    new_hooks.append(item)

            if new_hooks:
                settings['hooks'][hook_event] = new_hooks
            else:
                del settings['hooks'][hook_event]
            print(f"✅ {hook_event} ({hook_config['description']}) hook 已移除")

    # 如果 hooks 为空，删除整个 hooks 字段
    if 'hooks' in settings and not settings['hooks']:
        del settings['hooks']

    # 保存
    if save_settings(settings):
        print("")
        print("✅ Hooks 卸载成功！")
        print("")
        print("所有自动推送通知已停止")
        return True

    return False


def test_notification():
    """测试推送"""
    print("🧪 测试 Bark 推送...")
    print("")

    # 检查 device key
    device_key = os.environ.get("BARK_DEVICE_KEY")
    if not device_key:
        print("❌ 错误: BARK_DEVICE_KEY 未设置")
        print("")
        print("请在 ~/.claude/settings.json 的 env 中添加:")
        print('  "BARK_DEVICE_KEY": "your_device_key_here"')
        return False

    print(f"✅ Device Key: {device_key[:8]}...")
    print("")

    # 导入发送模块
    sys.path.insert(0, SKILL_DIR)
    try:
        from bark_send import send_bark

        print("📤 发送测试推送...")
        result = send_bark(
            device_key,
            "Bark Notify Hook 测试",
            "✅ Hook 工作正常！推送功能已就绪。",
            group="claude",
            sound="minuet"
        )

        if result.get("code") == 200:
            print("✅ 推送发送成功！")
            print("")
            print("请查看你的 iPhone 通知")
            return True
        else:
            print(f"⚠️  API 返回: {result}")
            return False

    except Exception as e:
        print(f"❌ 发送失败: {e}")
        return False


def show_status():
    """显示状态"""
    print("📊 Bark Notify Hook 状态")
    print("=" * 50)
    print("")

    # Hook 安装状态
    settings = load_settings()
    if settings is None:
        print("❌ 无法读取配置文件")
        return

    installed = is_hook_installed(settings)
    if not installed:
        print("❌ 无法读取配置状态")
        return

    print("Hook 状态:")
    for hook_event, hook_config in HOOKS_CONFIG.items():
        is_installed = installed[hook_event]
        status = "✅ 已安装" if is_installed else "❌ 未安装"
        print(f"  {hook_event} ({hook_config['description']}): {status}")

    # Device Key 状态
    device_key = os.environ.get("BARK_DEVICE_KEY")
    if device_key:
        print(f"\nDevice Key: ✅ 已配置 ({device_key[:8]}...)")
    else:
        print("\nDevice Key: ❌ 未配置")

    print("")
    print("配置文件: " + SETTINGS_FILE)
    print("Hook 脚本:")
    print("  - " + os.path.join(SKILL_DIR, "hook.py"))
    print("  - " + os.path.join(SKILL_DIR, "hook_permission.py"))
    print("  - " + os.path.join(SKILL_DIR, "hook_user_input.py"))
    print("")

    all_installed = all(installed.values())
    if all_installed and device_key:
        print("✅ 一切就绪！")
        print("   📱 回复完成时 → 自动推送")
        print("   ⚠️  权限请求时 → 紧急提醒")
        print("   💬 需要输入时 → 提醒返回")
    elif all_installed and not device_key:
        print("⚠️  Hooks 已安装，但需要配置 BARK_DEVICE_KEY")
    elif not all_installed and device_key:
        print("⚠️  Device Key 已配置，但 Hooks 未完全安装")
        print("   运行: /bark-notify-hook install")
    else:
        print("⚠️  需要安装 Hooks 并配置 Device Key")
        print("   1. 运行: /bark-notify-hook install")
        print("   2. 配置 BARK_DEVICE_KEY")


def main():
    if len(sys.argv) < 2:
        print("📱 Bark Notify Hook - 自动推送通知")
        print("")
        print("用法:")
        print("  /bark-notify-hook install   - 安装所有 hooks（回复完成 + 权限请求 + 用户输入）")
        print("  /bark-notify-hook uninstall - 卸载所有 hooks")
        print("  /bark-notify-hook test      - 测试推送")
        print("  /bark-notify-hook status    - 查看状态")
        print("")
        return 0

    command = sys.argv[1].lower()

    if command == "install":
        return 0 if install_hook() else 1
    elif command == "uninstall":
        return 0 if uninstall_hook() else 1
    elif command == "test":
        return 0 if test_notification() else 1
    elif command == "status":
        show_status()
        return 0
    else:
        print(f"❌ 未知命令: {command}")
        print("")
        print("可用命令: install, uninstall, test, status")
        return 1


if __name__ == "__main__":
    sys.exit(main())
