---
name: bark-notify-hook
description: Automatically send iOS Bark push notifications when Claude completes responses. Auto-installs Stop hook on first use.
---

# Bark Notify Hook - 自动推送通知

## 概述

在 Claude Code 完成回复时**自动**发送 Bark 推送通知到你的 iPhone/iPad，无需手动调用。

## 功能特性

- 🔔 每次 Claude 回复完成时自动推送到 iPhone/iPad
- 🎯 零配置，首次使用自动安装 hook
- 🔧 支持自定义标题、分组、铃声
- 🧹 一键卸载，干净删除所有配置

## 快速开始

### 1. 安装

通过 Claude Code 安装此 skill：

```bash
# 使用 /bark-notify-hook install 首次安装
```

### 2. 配置 Device Key

在 `~/.claude/settings.json` 的 `env` 中添加：

```json
{
  "env": {
    "BARK_DEVICE_KEY": "your_device_key_here"
  }
}
```

获取 device key：
1. 打开 Bark App
2. 复制测试 URL 中的 key
3. 例如：`https://api.day.app/ABC123/test` → key 为 `ABC123`

### 3. 完成

现在每次 Claude 完成回复时，你的 iPhone 会自动收到推送通知！

**重要**：修改配置后需要重启 Claude Code 才能生效。

## 命令

### `/bark-notify-hook install`

安装 Stop hook 到 `~/.claude/settings.json`

**功能：**
- 自动备份现有 settings.json
- 添加 Stop hook 配置
- 验证配置是否成功

**示例：**
```
/bark-notify-hook install
```

### `/bark-notify-hook uninstall`

卸载 Stop hook

**功能：**
- 从 settings.json 中移除 hook 配置
- 保留其他配置不变
- 自动备份

**示例：**
```
/bark-notify-hook uninstall
```

### `/bark-notify-hook test`

测试推送是否正常工作

**功能：**
- 发送测试推送到手机
- 验证 BARK_DEVICE_KEY 是否配置
- 检查网络连接

**示例：**
```
/bark-notify-hook test
```

### `/bark-notify-hook status`

查看当前安装状态

**功能：**
- 检查 hook 是否已安装
- 显示 device key 配置状态
- 显示当前配置信息

**示例：**
```
/bark-notify-hook status
```

## 自定义配置

### 修改推送标题

编辑 `~/.claude/skills/bark-notify-hook/hook.py`：

```python
# 默认标题
title = "Claude 任务完成"

# 修改为自定义标题
title = "AI 助手已完成工作"
```

### 修改分组、铃声和图标

编辑 hook.py 中的 `send_bark` 调用：

```python
result = send_bark(
    device_key, 
    title, 
    body, 
    group="claude",      # 修改分组
    sound="minuet",      # 修改铃声
    icon="图标URL"       # 修改图标
)
```

**常用铃声：**
- `minuet` - 默认，轻柔
- `bell` - 清脆，适合重要通知
- `alarm` - 紧急，适合错误通知
- `chime` - 柔和提醒

**常用分组：**
- `claude` - 默认，AI 对话通知
- `work` - 工作相关
- `personal` - 个人事务

**图标：**
- 默认使用 Claude 官方图标
- 可以替换为任何公开的图片 URL

## 工作原理

1. **安装时**：在 `~/.claude/settings.json` 中添加 `hooks.Stop` 配置
2. **回复完成时**：Claude Code 在主代理完成响应时自动执行 `hook.py` 脚本
3. **推送发送**：脚本调用 Bark API 发送推送到你的设备

## Hook 配置示例

安装后，settings.json 中会添加：

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python ~/.claude/skills/bark-notify-hook/hook.py"
          }
        ]
      }
    ]
  }
}
```

## 故障排查

### 没有收到推送？

1. **检查 device key**
   ```bash
   echo $BARK_DEVICE_KEY
   ```

2. **测试推送**
   ```
   /bark-notify-hook test
   ```

3. **检查 hook 状态**
   ```
   /bark-notify-hook status
   ```

4. **手动测试 hook 脚本**
   ```bash
   python ~/.claude/skills/bark-notify-hook/hook.py "测试消息"
   ```

### Hook 未触发？

- 确认 settings.json 中 hook 配置正确
- 重启 Claude Code
- 检查 hook.py 脚本是否存在且有执行权限

## 与 bark-notify skill 的区别

| 特性 | bark-notify | bark-notify-hook |
|------|-------------|------------------|
| 触发方式 | 手动调用 `/bark-notify` | 自动触发（Stop hook） |
| 使用场景 | 需要明确控制何时推送 | 希望每次回复完成都推送 |
| 配置复杂度 | 无需配置，直接使用 | 需要安装 hook |
| 推送内容 | 自定义标题和内容 | 固定标题，可修改 |

## 相关资源

- Bark 官网: https://bark.day.app/
- GitHub 项目: https://github.com/yz1128/bark-notification-plugin
- 手动版 skill: bark-notify

## License

MIT
