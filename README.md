# Bark Notify Skill

通过 iOS [Bark](https://bark.day.app/) 应用在 AI Agent 任务完成时发送推送通知。

**三种使用模式**：
1. **Skill 模式**（推荐）：Claude Code skill，手动调用 `/bark-notify` 发送推送
2. **Skill Hook 模式**（自动）：一键安装 SessionEnd hook，会话结束自动推送
3. **Plugin Hook 模式**：Python hook 插件，LLM 响应后自动推送（需框架支持）

## 功能特性

- 🔔 任务完成推送到 iPhone/iPad
- 🎯 捕获 LLM 响应作为通知内容
- 🧵 异步发送，不阻塞会话关闭
- 💾 自动管理会话缓存（防止内存泄漏）
- 🎨 支持自定义提示音、分组、归档等参数
- 📱 命令行独立使用，灵活调用
- ⚡ 一键安装/卸载自动推送 hook

## 快速开始

### 方式一：Claude Code Skill（推荐 - 手动推送）

**1. 安装 Skill**

**自动安装（推荐）：**

```bash
# Linux/macOS
git clone https://github.com/yz1128/bark-notification-plugin.git
cd bark-notification-plugin
./install.sh

# Windows（PowerShell 或 CMD）
git clone https://github.com/yz1128/bark-notification-plugin.git
cd bark-notification-plugin
install.bat
```

**手动安装：**

```bash
# 克隆到 Claude skills 目录
git clone https://github.com/yz1128/bark-notification-plugin.git ~/.claude/skills/bark-notify

# 或者创建符号链接（推荐，会随 git pull 自动更新）
git clone https://github.com/yz1128/bark-notification-plugin.git ~/bark-notification-plugin
ln -s ~/bark-notification-plugin/skill ~/.claude/skills/bark-notify
```

**2. 配置 Device Key**

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

**3. 使用 Skill**

在 Claude Code 对话中：

```bash
# 发送简单通知
/bark-notify "任务完成"

# 发送带内容的通知
/bark-notify "测试通过" "所有 127 个测试用例已通过"

# 自定义分组和铃声
/bark-notify "部署成功" "v2.1.0 已上线" --group deploy --sound bell

# 带跳转链接
/bark-notify "PR 已创建" "请查看 #456" --url "https://github.com/user/repo/pull/456"
```

### 方式二：Skill Hook 模式（推荐 - 自动推送）⭐

**一键安装，会话结束自动推送！**

**1. 安装 Skill**

```bash
# 创建符号链接
ln -s ~/bark-notification-plugin/skill-hook ~/.claude/skills/bark-notify-hook
```

**2. 配置 Device Key**（同上）

**3. 安装 Hook**

在 Claude Code 中运行：

```
/bark-notify-hook install
```

**4. 完成！**

现在每次对话结束时，会自动发送推送到你的 iPhone！

**其他命令：**
- `/bark-notify-hook uninstall` - 卸载自动推送
- `/bark-notify-hook test` - 测试推送
- `/bark-notify-hook status` - 查看状态

**手动配置 Hook（可选）：**

如果你想手动配置，在 `~/.claude/settings.json` 中添加：

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
    ]
  }
}
```

### 方式三：Python Plugin Hook（高级）

**注意：此方式需要你的 Agent 框架支持 Python plugin hooks。Claude Code 目前不支持。**

**1. 安装插件**

**1. 安装插件**

将 `__init__.py` 和 `plugin.yaml` 复制到你的框架插件目录。

**2. 配置环境变量**

```bash
export BARK_DEVICE_KEY="your_device_key"
```

**3. Hook 说明**

插件会自动注册以下 hooks：
- `post_llm_call` - 每次 LLM 响应后立即发送通知
- `on_session_end` - （备用）会话结束时发送通知

### 方式三：命令行直接使用

```bash
# 基本推送
python skill/bark_send.py "标题" "内容"

# 带参数
python skill/bark_send.py "部署成功" "v2.1.0 已上线" --group deploy --sound bell

# 包装命令（任务完成后自动推送）
python skill/bark_notify_task.py npm test
```

## 使用示例

### Skill 模式示例

### Skill 模式示例

```
用户: "帮我重构这个 auth 模块"
AI: [执行重构...]
AI: "重构完成，已更新 5 个文件，所有测试通过。"
用户: "/bark-notify '重构完成' '已更新 5 个文件，所有测试通过'"
→ 推送: "重构完成" / "已更新 5 个文件，所有测试通过"
```

### Plugin Hook 模式示例

插件会在以下情况自动发送通知：
- ✅ 每次 LLM 响应后立即推送
- ✅ 已设置 `BARK_DEVICE_KEY`

通知内容包括：
- **标题**: "Hermes" 或 "Hermes (platform)"
- **正文**: LLM 响应（前 200 字符）

### 命令行模式示例

```bash
# 包装测试命令
python skill/bark_notify_task.py npm test
→ 推送: "✅ 任务成功" / "npm test\n用时: 12秒"

# 直接发送
python skill/bark_send.py "编译完成" "Build successful"
→ 推送: "编译完成" / "Build successful"
```

### 环境要求

- Python 3.7+
- 无第三方依赖（仅使用标准库）

### 自定义通知参数

编辑 `__init__.py` 中的 `_send_bark()` 函数：

```python
payload = json.dumps({
    "title": title,
    "body": body,
    "group": "hermes",      # 修改分组名
    "sound": "minuet",      # 更换提示音
    "level": "active",      # critical/timeSensitive/passive
    "badge": 1,             # 角标数字
    "isArchive": 1,         # 是否归档
})
```

完整参数说明见 [barkApi.md](barkApi.md)。

## 文件说明

```
bark-notification-plugin/
├── skill/                      # Claude Code Skill（手动推送）
│   ├── SKILL.md               # Skill 完整文档
│   ├── README.md              # Skill 快速开始
│   ├── bark_send.py           # 核心推送工具（可独立使用）
│   ├── bark_notify_task.py    # 命令包装器
│   ├── run.py                 # Skill 入口点
│   └── hook.py                # SessionEnd hook 脚本（手动配置用）
├── skill-hook/                 # ⭐ Skill Hook 模式（自动推送）
│   ├── SKILL.md               # 完整文档
│   ├── README.md              # 快速开始
│   ├── run.py                 # 安装/卸载/测试工具
│   ├── hook.py                # SessionEnd hook 脚本
│   └── bark_send.py           # 核心推送实现
├── install.sh                  # Linux/macOS 安装脚本
├── install.bat                 # Windows 安装脚本
├── __init__.py                 # Python Plugin Hook 实现
├── plugin.yaml                 # Plugin 元数据
├── barkApi.md                 # Bark API 完整文档
├── CLAUDE.md                  # 代码库文档（供 Claude Code 使用）
└── README.md                  # 本文件
```

## 故障排查

| 症状 | 解决方法 |
|------|---------|
| 没有收到通知 | 检查 `BARK_DEVICE_KEY` 是否设置，查看启动日志 |
| 通知内容为空 | 确认 `post_llm_call` hook 正常触发 |
| 网络错误 | 确认 `api.day.app` 可访问 |

## 架构设计

```
post_llm_call → _store_response() → OrderedDict (限制 50 条)
                                         ↓
on_session_end → _pop_response() → _send_bark() → Threading (daemon)
```

关键设计：
- **会话隔离**: 用 `session_id` 关联响应和通知
- **内存安全**: LRU 驱逐策略，最多缓存 50 条
- **非阻塞**: daemon 线程异步发送（10s 超时）

## 相关资源

- [Bark 官方文档](https://bark.day.app/)
- [Bark GitHub](https://github.com/Finb/Bark)
- [MCP 集成指南](barkApi.md#mcp)

## License

MIT
