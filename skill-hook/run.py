#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bark Notify Hook Skill Runner
自动安装/卸载 SessionEnd hook
"""

import os
import sys
import json
import shutil
from datetime import datetime

# Windows 环境下设置 stdout 编码为 UTF-8
if sys.platform == 'win32':
    import io
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.expanduser("~/.claude/settings.json")
HOOK_SESSION_END = "python ~/.claude/skills/bark-notify-hook/hook.py"
HOOK_PERMISSION = "python ~/.claude/skills/bark-notify-hook/hook_permission.py"


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
    """检查 hook 是否已安装"""
    if not settings or 'hooks' not in settings:
        return False, False

    hooks = settings.get('hooks', {})

    # 检查 SessionEnd hook
    session_end_installed = False
    session_end = hooks.get('SessionEnd', [])
    for item in session_end:
        for hook in item.get('hooks', []):
            if hook.get('command') == HOOK_SESSION_END:
                session_end_installed = True
                break

    # 检查 PermissionRequest hook
    permission_installed = False
    permission_request = hooks.get('PermissionRequest', [])
    for item in permission_request:
        for hook in item.get('hooks', []):
            if hook.get('command') == HOOK_PERMISSION:
                permission_installed = True
                break

    return session_end_installed, permission_installed


def install_hook():
    """安装 SessionEnd 和 PermissionRequest hooks"""
    print("📦 正在安装 Bark Notify Hooks...")
    print("")

    # 备份
    backup_settings()

    # 加载配置
    settings = load_settings()
    if settings is None:
        return False

    # 检查是否已安装
    session_end_installed, permission_installed = is_hook_installed(settings)
    if session_end_installed and permission_installed:
        print("⚠️  Hooks 已经安装，无需重复安装")
        return True

    # 添加 hooks
    if 'hooks' not in settings:
        settings['hooks'] = {}

    # 安装 SessionEnd hook
    if not session_end_installed:
        if 'SessionEnd' not in settings['hooks']:
            settings['hooks']['SessionEnd'] = []

        settings['hooks']['SessionEnd'].append({
            "hooks": [
                {
                    "type": "command",
                    "command": HOOK_SESSION_END
                }
            ]
        })
        print("✅ SessionEnd hook 已添加")

    # 安装 PermissionRequest hook
    if not permission_installed:
        if 'PermissionRequest' not in settings['hooks']:
            settings['hooks']['PermissionRequest'] = []

        settings['hooks']['PermissionRequest'].append({
            "hooks": [
                {
                    "type": "command",
                    "command": HOOK_PERMISSION
                }
            ]
        })
        print("✅ PermissionRequest hook 已添加")

    # 保存
    if save_settings(settings):
        print("")
        print("✅ Hooks 安装成功！")
        print("")
        print("功能说明：")
        print("  📱 会话结束时 → 自动发送完成通知")
        print("  ⚠️  权限请求时 → 自动提醒需要确认")
        print("")
        print("下一步：")
        print("  1. 确保已配置 BARK_DEVICE_KEY")
        print("  2. 运行 /bark-notify-hook test 测试推送")
        return True

    return False


def uninstall_hook():
    """卸载 SessionEnd 和 PermissionRequest hooks"""
    print("🗑️  正在卸载 Bark Notify Hooks...")
    print("")

    # 备份
    backup_settings()

    # 加载配置
    settings = load_settings()
    if settings is None:
        return False

    # 检查是否已安装
    session_end_installed, permission_installed = is_hook_installed(settings)
    if not session_end_installed and not permission_installed:
        print("⚠️  Hooks 未安装，无需卸载")
        return True

    # 移除 SessionEnd hook
    if session_end_installed and 'hooks' in settings and 'SessionEnd' in settings['hooks']:
        new_session_end = []
        for item in settings['hooks']['SessionEnd']:
            new_hooks = []
            for hook in item.get('hooks', []):
                if hook.get('command') != HOOK_SESSION_END:
                    new_hooks.append(hook)

            if new_hooks:
                item['hooks'] = new_hooks
                new_session_end.append(item)

        if new_session_end:
            settings['hooks']['SessionEnd'] = new_session_end
        else:
            del settings['hooks']['SessionEnd']
        print("✅ SessionEnd hook 已移除")

    # 移除 PermissionRequest hook
    if permission_installed and 'hooks' in settings and 'PermissionRequest' in settings['hooks']:
        new_permission = []
        for item in settings['hooks']['PermissionRequest']:
            new_hooks = []
            for hook in item.get('hooks', []):
                if hook.get('command') != HOOK_PERMISSION:
                    new_hooks.append(hook)

            if new_hooks:
                item['hooks'] = new_hooks
                new_permission.append(item)

        if new_permission:
            settings['hooks']['PermissionRequest'] = new_permission
        else:
            del settings['hooks']['PermissionRequest']
        print("✅ PermissionRequest hook 已移除")

    # 如果 hooks 为空，删除整个 hooks 字段
    if 'hooks' in settings and not settings['hooks']:
        del settings['hooks']

    # 保存
    if save_settings(settings):
        print("")
        print("✅ Hooks 卸载成功！")
        print("")
        print("对话结束和权限请求时不再自动推送通知")
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

    session_end_installed, permission_installed = is_hook_installed(settings)

    print("Hook 状态:")
    print(f"  SessionEnd (会话结束): {'✅ 已安装' if session_end_installed else '❌ 未安装'}")
    print(f"  PermissionRequest (权限请求): {'✅ 已安装' if permission_installed else '❌ 未安装'}")

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
    print("")

    all_installed = session_end_installed and permission_installed
    if all_installed and device_key:
        print("✅ 一切就绪！")
        print("   📱 会话结束时 → 自动推送")
        print("   ⚠️  权限请求时 → 自动提醒")
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
        print("  /bark-notify-hook install   - 安装 hooks（会话结束 + 权限请求）")
        print("  /bark-notify-hook uninstall - 卸载 hooks")
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
