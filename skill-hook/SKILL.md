---
name: bark-notify-hook
description: Automatically send iOS Bark push notifications when Claude completes responses. Auto-installs Stop hook on first use.
---

# Bark Notify Hook - 自动推送通知

## 概述

在 Claude Code 完成回复时**自动**发送 Bark 推送通知到你的 iPhone/iPad，无需手动调用。

## 推送格式

所有推送使用统一格式，便于识别：

**标题**：`Claude Code`

**内容**：
- 🆔 Session ID
- 状态标识（任务完成/权限请求/等待输入）
- 附加信息（如工具名称、问题内容等）

**示例 - 任务完成**：
```
标题: Claude Code

内容:
🆔 c4a38421-8dee-422c-b849-9b0de4544e08
✅ 任务完成
```

**示例 - 权限请求**：
```
标题: Claude Code

内容:
🆔 c4a38421-8dee-422c-b849-9b0de4544e08
⚠️ 权限请求

操作: PowerShell
```

**示例 - 等待输入**：
```
标题: Claude Code

内容:
🆔 c4a38421-8dee-422c-b849-9b0de4544e08
💬 等待输入

Which option do you prefer?
```

## 功能特性

- 🔔 每次 Claude 回复完成时自动推送到 iPhone/iPad
- 📱 三种场景智能推送：任务完成、权限请求、等待输入
- 🎯 统一格式，包含 Session ID 便于追踪
- 🖼️ 自带 Claude 图标，识别度高
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

### 修改推送格式

编辑对应的 hook 脚本来修改推送格式：

**hook_stop.py（任务完成）**：
```python
# 标题（默认：Claude Code）
title = "Claude Code"

# 内容格式
body = f"🆔 {session_id}\n✅ 任务完成"
```

**hook_permission.py（权限请求）**：
```python
# 标题
title = "Claude Code"

# 内容格式
body = f"🆔 {session_id}\n⚠️ 权限请求\n\n操作: {tool_name}"
```

**hook_user_input.py（等待输入）**：
```python
# 标题
title = "Claude Code"

# 内容格式
body = f"🆔 {session_id}\n💬 等待输入\n\n{question[:100]}"
```

### 修改分组、铃声和图标

编辑任意 hook 脚本中的 `send_bark` 调用：

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
- `minuet` - 默认，轻柔（用于任务完成）
- `bell` - 清脆，适合提醒（用于等待输入）
- `alarm` - 紧急，适合警告（用于权限请求）
- `chime` - 柔和提醒

**常用分组：**
- `claude` - 默认，AI 对话通知
- `claude-permission` - 权限请求
- `claude-input` - 用户输入请求
- `work` - 工作相关
- `personal` - 个人事务

**图标：**
- 默认使用 Claude 官方图标（jsdelivr CDN）
- 可以替换为任何公开的图片 URL

## 工作原理

1. **安装时**：在 `~/.claude/settings.json` 中添加三个 hook 配置
   - `hooks.Stop` - 任务完成时触发
   - `hooks.PermissionRequest` - 权限请求时触发
   - `hooks.Elicitation` - 等待用户输入时触发

2. **触发时机**：
   - **Stop** - Claude 主代理完成响应时
   - **PermissionRequest** - 需要用户确认权限时
   - **Elicitation** - 需要用户回答问题时

3. **推送发送**：对应的 hook 脚本调用 Bark API 发送推送

**推送特性**：
- **任务完成** - 轻柔铃声（`minuet`），自动归档
- **权限请求** - 紧急铃声（`alarm`），时效性通知，不归档
- **等待输入** - 清脆铃声（`bell`），时效性通知，不归档

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
            "command": "python ~/.claude/skills/bark-notify-hook/hook_stop.py"
          }
        ]
      }
    ],
    "PermissionRequest": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python ~/.claude/skills/bark-notify-hook/hook_permission.py"
          }
        ]
      }
    ],
    "Elicitation": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python ~/.claude/skills/bark-notify-hook/hook_user_input.py"
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
- 检查 hook_stop.py 脚本是否存在且有执行权限

## 常见错误与避免方法

### ❌ 不要：重复执行 install 命令

**为什么：** 会在 settings.json 中创建重复的 hook 配置，导致每次推送多条通知

**正确做法：** 先运行 `/bark-notify-hook status` 检查是否已安装，如已安装则无需重复

---

### ❌ 不要：直接复制粘贴示例中的 BARK_DEVICE_KEY

**为什么：** `your_device_key_here` 不是真实的 key，会导致推送失败

**正确做法：** 从 Bark App 获取你自己的 device key（打开 App → 复制 URL 中的唯一标识）

---

### ❌ 不要：修改 hook 脚本后不重启

**为什么：** Claude Code 在启动时读取 settings.json，运行时不会重新加载

**正确做法：** 修改任何配置或脚本后，必须完全退出并重启 Claude Code

---

### ❌ 不要：删除 skill 目录但不卸载 hook

**为什么：** settings.json 中仍然引用已删除的脚本路径，每次触发会报错

**正确做法：** 先运行 `/bark-notify-hook uninstall` 清理配置，再删除目录

---

### ❌ 不要：在 BARK_DEVICE_KEY 中包含完整 URL

**为什么：** 只需要 key 部分，不需要 `https://api.day.app/` 前缀

**正确做法：**
```json
// ❌ 错误
"BARK_DEVICE_KEY": "https://api.day.app/ABC123/test"

// ✅ 正确
"BARK_DEVICE_KEY": "ABC123"
```

---

### ❌ 不要：在没有 Python 3 环境时安装

**为什么：** hook 脚本依赖 Python 3，没有 Python 会静默失败

**正确做法：** 先确认 `python --version` 或 `python3 --version` 可用且版本 ≥ 3.7

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
