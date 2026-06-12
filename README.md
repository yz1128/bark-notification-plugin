# Bark Notify Hook

通过 iOS [Bark](https://bark.day.app/) 应用在 Claude Code 会话结束或需要用户输入时自动发送推送通知。

**一键安装，自动推送！**

## 功能特性

- 🔔 会话结束时自动推送到 iPhone/iPad
- ⚠️ 权限请求时自动提醒（需要你的确认时）
- ⚡ 一键安装/卸载 hooks
- 🎯 智能状态检测
- 🎨 支持自定义提示音、分组、归档
- 🧹 完全卸载，不留残留

## 快速开始

### 1. 安装 Skill

```bash
# Linux/macOS
git clone https://github.com/yz1128/bark-notify-skill.git
ln -s ~/bark-notify-skill/skill-hook ~/.claude/skills/bark-notify-hook

# Windows (PowerShell 管理员权限)
git clone https://github.com/yz1128/bark-notify-skill.git
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\skills\bark-notify-hook" -Target "$env:USERPROFILE\bark-notify-skill\skill-hook"
```

### 2. 配置 Device Key

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

### 3. 安装 Hooks

在 Claude Code 中运行：

```
/bark-notify-hook install
```

### 4. 完成！

现在会自动推送：
- 📱 **会话结束时** → "Claude 任务完成"
- ⚠️ **权限请求时** → "需要你的确认" (紧急提醒)

## 命令

- `/bark-notify-hook install` - 安装 hooks（会话结束 + 权限请求）
- `/bark-notify-hook uninstall` - 卸载 hooks
- `/bark-notify-hook test` - 测试推送
- `/bark-notify-hook status` - 查看状态

## 工作原理

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

## 自定义配置

### 修改推送标题

编辑 `~/.claude/skills/bark-notify-hook/hook.py`：

```python
# 默认标题
title = "Claude 任务完成"

# 修改为自定义标题
title = "AI 助手已完成工作"
```

### 修改分组和铃声

编辑 hook.py 中的 `send_bark` 调用：

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
- `claude-permission` - 权限请求通知（默认）
- `work` - 工作相关
- `personal` - 个人事务

## 文件说明

```
bark-notify-skill/
├── skill-hook/                 # ⭐ Skill Hook 模式（推荐使用）
│   ├── SKILL.md               # 完整文档
│   ├── README.md              # 快速开始
│   ├── run.py                 # 安装/卸载/测试工具
│   ├── hook.py                # SessionEnd hook 脚本
│   ├── hook_permission.py     # PermissionRequest hook 脚本
│   └── bark_send.py           # 核心推送实现
├── skill/                      # 手动推送模式（已废弃）
├── __init__.py                 # Python Plugin Hook（已废弃）
├── barkApi.md                  # Bark API 完整文档
└── README.md                   # 本文件
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
   ```

### Hooks 未触发？

- 确认 settings.json 中 hooks 配置正确
- 重启 Claude Code
- 检查 hook 脚本是否存在且有执行权限

### 权限请求推送过于频繁？

编辑 `hook_permission.py`，可以添加条件过滤：

```python
# 只在特定工具时推送
if tool_name not in ["Edit", "Write", "Bash"]:
    sys.exit(0)
```

## 安装的 Hook 配置

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
    ]
  }
}
```

## 相关资源

- Bark 官网: https://bark.day.app/
- Bark GitHub: https://github.com/Finb/Bark
- Claude Code 文档: https://claude.ai/code

## License

MIT
