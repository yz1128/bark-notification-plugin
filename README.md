# Bark Notify Hook

通过 iOS [Bark](https://bark.day.app/) 应用在 AI Agent 会话结束或需要用户输入时自动发送推送通知。

**支持 Claude Code 和 Hermes Agent！**

## 功能特性

- 🔔 会话结束时自动推送到 iPhone/iPad
- ⚠️ 权限请求时紧急提醒（需要你确认时）
- 💬 需要输入时提醒返回（Agent 等待你回答时）
- ⚡ 一键安装/卸载所有 hooks
- 🎯 智能状态检测
- 🎨 支持自定义提示音、分组、归档
- 🧹 完全卸载，不留残留
- 🖼️ 支持自定义图标（Hermes Agent 使用官方 logo）

## 支持的 AI Agent

| Agent | 配置目录 | 安装方式 |
|-------|----------|----------|
| **Claude Code** | `~/.claude/` | Skill Hook |
| **Hermes Agent** | `~/.hermes/` | Plugin Hook |

---

## Claude Code 配置

### 快速开始

#### 1. 安装 Skill

```bash
# Linux/macOS
git clone https://github.com/yz1128/bark-notify-skill.git
ln -s ~/bark-notify-skill/skill-hook ~/.claude/skills/bark-notify-hook

# Windows (PowerShell 管理员权限)
git clone https://github.com/yz1128/bark-notify-skill.git
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\skills\bark-notify-hook" -Target "$env:USERPROFILE\bark-notify-skill\skill-hook"
```

#### 2. 配置 Device Key

打开 Bark 应用，复制测试 URL 中的 key：

```
https://api.day.app/your_device_key/test
                    ^^^^^^^^^^^^^^^^
                    这就是你的 device key
```

在 `~/.claude/settings.json` 的 `env` 中添加：

```json
{
  "env": {
    "BARK_DEVICE_KEY": "your_device_key_here"
  }
}
```

#### 3. 安装 Hooks

在 Claude Code 中运行：

```
/bark-notify-hook install
```

#### 4. 完成！

现在会自动推送：
- 📱 **会话结束时** → "Claude 任务完成"
- ⚠️ **权限请求时** → "需要你的确认" (紧急提醒)
- 💬 **需要输入时** → "需要回答" (提醒返回终端)

### Claude Code 命令

- `/bark-notify-hook install` - 安装所有 hooks（会话结束 + 权限请求 + 用户输入）
- `/bark-notify-hook uninstall` - 卸载所有 hooks
- `/bark-notify-hook test` - 测试推送
- `/bark-notify-hook status` - 查看状态

### Claude Code 工作原理

**会话结束推送（SessionEnd Hook）：**
- 每次对话结束时自动触发
- 发送标题："Claude 任务完成"
- 铃声：轻柔的 minuet
- 分组：claude

**权限请求推送（PermissionRequest Hook）：**
- Claude 需要权限确认时自动触发
- 发送标题："⚠️ [项目名] 需要确认"
- 铃声：紧急的 alarm
- 优先级：时效性通知
- 不归档（需要立即处理）

**用户输入推送（Elicitation Hook）：**
- Claude 等待你回答问题时自动触发
- 发送标题："💬 [项目名] 需要回答"
- 铃声：清脆的 bell
- 优先级：时效性通知
- 不归档（需要立即处理）

---

## Hermes Agent 配置

### 快速开始

#### 1. 安装 Plugin

```bash
# 克隆仓库
git clone https://github.com/yz1128/bark-notify-skill.git

# 复制插件到 Hermes 插件目录
cp -r bark-notify-skill/hermes-plugin ~/.hermes/plugins/bark-notify
```

#### 2. 配置 Device Key

在 `~/.hermes/.env` 文件中添加：

```bash
BARK_DEVICE_KEY=your_device_key_here
```

#### 3. 启用插件

```bash
hermes plugins enable bark-notify
```

#### 4. 完成！

现在每次会话结束时，你的 iPhone 会收到带有 Hermes logo 的推送通知。

### Hermes Agent 命令

```bash
# 查看插件状态
hermes plugins list

# 禁用插件
hermes plugins disable bark-notify

# 启用插件
hermes plugins enable bark-notify

# 测试推送
python3 ~/.hermes/plugins/bark-notify/__init__.py
```

### Hermes Agent 工作原理

**会话结束推送（on_session_end Hook）：**
- 每次对话结束时自动触发
- 支持正常完成、中断、超时等状态
- 自定义 Hermes 官方 logo 图标
- 不同状态使用不同铃声：
  - ✅ 正常完成 - minuet（轻柔）
  - ⚠️ 中断 - alarm（紧急）
  - ℹ️ 结束 - chime（柔和）

### Hermes Agent 自定义配置

#### 修改图标

编辑 `~/.hermes/plugins/bark-notify/__init__.py`：

```python
# 修改为你喜欢的图标 URL
HERMES_ICON_URL = "https://your-custom-icon-url.com/icon.png"
```

#### 修改铃声

编辑 `_on_session_end` 函数中的 `sound` 参数：

```python
# 可用铃声：
# minuet - 默认，轻柔
# bell - 清脆
# alarm - 紧急
# chime - 柔和提醒
```

---

## 自定义配置（通用）

### 修改推送标题

**Claude Code：** 编辑 `~/.claude/skills/bark-notify-hook/hook.py`

**Hermes Agent：** 编辑 `~/.hermes/plugins/bark-notify/__init__.py`

```python
# 默认标题
title = "任务完成"

# 修改为自定义标题
title = "AI 助手已完成工作"
```

### 修改分组和铃声

编辑 `send_bark` 调用：

```python
result = send_bark(
    device_key, 
    title, 
    body, 
    group="my-group",    # 修改分组
    sound="bell"         # 修改铃声
)
```

**常用铃声：**
- `minuet` - 默认，轻柔
- `bell` - 清脆，适合重要通知
- `alarm` - 紧急，适合错误通知（权限请求默认使用）
- `chime` - 柔和提醒

**常用分组：**
- `claude` - 默认，AI 对话通知
- `hermes` - Hermes Agent 通知
- `work` - 工作相关
- `personal` - 个人事务

---

## 文件说明

```
bark-notify-skill/
├── skill-hook/                 # ⭐ Claude Code Skill Hook（推荐使用）
│   ├── SKILL.md               # 完整文档
│   ├── README.md              # 快速开始
│   ├── run.py                 # 安装/卸载/测试工具
│   ├── hook.py                # SessionEnd hook 脚本
│   ├── hook_permission.py     # PermissionRequest hook 脚本
│   ├── hook_user_input.py     # Elicitation hook 脚本
│   └── bark_send.py           # 核心推送实现
├── hermes-plugin/              # ⭐ Hermes Agent Plugin Hook
│   ├── plugin.yaml            # 插件配置
│   └── __init__.py            # 主代码（带 Hermes 图标）
├── barkApi.md                  # Bark API 完整文档
└── README.md                   # 本文件
```

---

## 故障排查

### 没有收到推送？

#### Claude Code

1. **检查 device key**
   ```bash
   echo $BARK_DEVICE_KEY
   ```

2. **测试推送**
   ```
   /bark-notify-hook test
   ```

3. **检查 hooks 状态**
   ```
   /bark-notify-hook status
   ```

4. **手动测试 hook 脚本**
   ```bash
   # 测试会话结束 hook
   python ~/.claude/skills/bark-notify-hook/hook.py "测试消息"
   
   # 测试权限请求 hook
   echo '{"tool_name":"Edit","cwd":"/home/user/project"}' | python ~/.claude/skills/bark-notify-hook/hook_permission.py
   
   # 测试用户输入 hook
   echo '{"question":"你想继续吗？","cwd":"/home/user/project"}' | python ~/.claude/skills/bark-notify-hook/hook_user_input.py
   ```

#### Hermes Agent

1. **检查 Device Key**
   ```bash
   grep BARK_DEVICE_KEY ~/.hermes/.env
   ```

2. **测试推送**
   ```bash
   python3 ~/.hermes/plugins/bark-notify/__init__.py
   ```

3. **检查插件状态**
   ```bash
   hermes plugins list | grep bark-notify
   ```

4. **查看日志**
   ```bash
   hermes logs | grep -i bark
   ```

### Hooks 未触发？

**Claude Code：**
- 确认 settings.json 中 hooks 配置正确
- 重启 Claude Code
- 检查 hook 脚本是否存在且有执行权限

**Hermes Agent：**
- 确认插件已启用：`hermes plugins enable bark-notify`
- 重启 Hermes 会话
- 检查 `~/.hermes/.env` 中的 Device Key

### 权限请求推送过于频繁？

编辑 `hook_permission.py`（Claude Code）或 `__init__.py`（Hermes Agent），可以添加条件过滤：

```python
# 只在特定工具时推送
if tool_name not in ["Edit", "Write", "Bash"]:
    sys.exit(0)
```

---

## 安装的 Hook 配置

### Claude Code

安装后，`~/.claude/settings.json` 中会添加：

```json
{
  "hooks": {
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python ~/.claude/skills/bark-notify-hook/hook.py"
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

### Hermes Agent

安装后，`~/.hermes/plugins/bark-notify/` 目录结构：

```
~/.hermes/plugins/bark-notify/
├── plugin.yaml      # 插件配置
├── __init__.py      # 主代码（带 Hermes 图标）
└── README.md        # 使用说明
```

---

## 相关资源

- Bark 官网: https://bark.day.app/
- Bark GitHub: https://github.com/Finb/Bark
- Claude Code 文档: https://claude.ai/code
- Hermes Agent 文档: https://hermes-agent.nousresearch.com/docs/

## License

MIT
