---
name: bark-notify-hook
description: |
  通过 iOS Bark 应用在 Claude Code / Hermes Agent 完成回复、请求权限或等待输入时自动发送推送通知到 iPhone/iPad。支持三种触发场景：Stop hook（任务完成）、PermissionRequest hook（权限请求）、Elicitation hook（用户输入）。安装后无需手动调用，每次会话结束时自动推送。
  
  触发词：bark推送、bark通知、自动推送、会话结束通知、bark-notify-hook、iOS推送、手机提醒
  
  何时使用：希望在 Claude 完成任务后收到手机提醒时；不想盯着终端等待长时间任务完成时；需要及时响应权限请求时。
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

### Step 1: 获取 Bark Device Key

**输入：** 你的 iPhone/iPad 上已安装 Bark App

**操作：**
1. 打开 Bark App
2. 查看顶部测试 URL，格式为：`https://api.day.app/ABC123/test`
3. 复制其中的 key 部分（`ABC123`）

**输出：** 一串唯一的 device key（如 `eUt43wGYCe6YpDWMiRxPgX`）

---

### Step 2: 配置 Device Key

**输入：** 上一步获取的 device key

**操作：**
编辑 `~/.claude/settings.json`，在 `env` 中添加：

```json
{
  "env": {
    "BARK_DEVICE_KEY": "你的_device_key"
  }
}
```

**输出：** settings.json 文件已保存，包含 BARK_DEVICE_KEY 配置

---

### Step 3: 安装 Hook

**输入：** 在 Claude Code 对话中输入

**操作：**
```
/bark-notify-hook install
```

**输出：** 
```
✅ Hook 安装成功
📄 配置文件: /Users/你/.claude/settings.json
🪝 已添加 3 个 hooks: Stop, PermissionRequest, Elicitation
```

---

### Step 4: 重启生效

**操作：** 完全退出 Claude Code，再重新启动

**输出：** 现在每次 Claude 完成回复时，你的 iPhone 会自动收到推送通知！

## 命令

### `/bark-notify-hook install`

安装 Stop hook 到 `~/.claude/settings.json`

**功能：**
- 自动备份现有 settings.json
- 添加 Stop hook 配置
- 验证配置是否成功

🔴 **CHECKPOINT：安装前请确认**
- 已获取有效的 BARK_DEVICE_KEY
- 已在 settings.json 的 env 中配置 BARK_DEVICE_KEY
- Python 3.7+ 可用（运行 `python --version` 检查）

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

🔴 **CHECKPOINT：卸载前请确认**
- 确认不再需要自动推送通知
- 理解卸载后需要手动调用才能推送
- 如需临时禁用，可以注释 settings.json 中的 hook 配置而非完全卸载

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

🔴 **CHECKPOINT：修改前必读**
- 修改任何 hook 脚本后必须重启 Claude Code 才能生效
- 建议先备份原始脚本：`cp hook_stop.py hook_stop.py.bak`
- 语法错误会导致 hook 静默失败，修改后务必测试

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
- `minuet` - 默认（任务完成时使用）
- `bell` - 清脆（等待输入时使用）
- `alarm` - 紧急（权限请求时使用）
- `chime` - 柔和（一般提醒）

**分组说明：**
- `claude` - 任务完成通知（默认）
- `claude-permission` - 权限请求（hook_permission.py 使用）
- `claude-input` - 用户输入请求（hook_user_input.py 使用）
- `work` - 工作相关自定义分组
- `personal` - 个人事务自定义分组

**图标设置：**
- 默认图标：`https://cdn.jsdelivr.net/gh/yz1128/MyImageRepository@main/image/20260613092240368.png`
- 替换方法：修改 `send_bark()` 调用中的 `icon` 参数为任何公开图片 URL
- 图片格式：支持 PNG、JPG、WebP（推荐 PNG）
- 图片大小：建议 512x512 或 1024x1024

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

### 问题诊断流程

按以下三段式处理故障：**触发条件 → 一线修复 → 仍失败兜底**

| 症状 | 一线修复 | 仍失败则 |
|------|----------|----------|
| **没有收到推送** | 1. 检查 BARK_DEVICE_KEY 是否配置：`echo $BARK_DEVICE_KEY`<br>2. 运行测试命令：`/bark-notify-hook test` | 1. 检查手机网络连接<br>2. 访问 https://api.day.app 确认 Bark 服务正常<br>3. 尝试在 Bark App 中手动发送测试 |
| **Hook 未触发** | 1. 运行 `/bark-notify-hook status` 检查安装状态<br>2. 确认 settings.json 中 hook 配置存在<br>3. 完全退出并重启 Claude Code | 1. 手动运行 hook 脚本测试：<br>`echo '{"session_id":"test"}' \| python ~/.claude/skills/bark-notify-hook/hook_stop.py`<br>2. 检查脚本是否有执行权限<br>3. 查看 Python 版本是否 ≥ 3.7 |
| **推送内容错误** | 1. 检查是否修改过 hook 脚本<br>2. 对比 GitHub 仓库的原始版本<br>3. 重启 Claude Code | 1. 删除并重新安装 skill<br>2. 清空 settings.json 中的 hook 配置重新安装 |
| **收到重复推送** | 1. 运行 `/bark-notify-hook status` 查看是否重复安装<br>2. 检查 settings.json 中 hook 配置是否有重复条目 | 1. 运行 `/bark-notify-hook uninstall`<br>2. 手动编辑 settings.json 删除重复的 hook 配置<br>3. 重新运行 `/bark-notify-hook install` |
| **Python 导入错误** | 1. 确认 Python 3.7+ 已安装<br>2. 检查 bark_send.py 是否存在于 skill 目录 | 1. 完整重新 clone skill 仓库<br>2. 确认没有破坏 skill 目录结构<br>3. 尝试手动运行：`python -c "from bark_send import send_bark"` |

### 快速诊断命令

```bash
# 检查环境
echo $BARK_DEVICE_KEY
python --version

# 检查文件
ls -la ~/.claude/skills/bark-notify-hook/

# 手动测试脚本
echo '{"session_id":"test-123"}' | python ~/.claude/skills/bark-notify-hook/hook_stop.py

# 查看配置
cat ~/.claude/settings.json | grep -A 20 '"hooks"'
```

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
