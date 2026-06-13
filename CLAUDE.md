# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

Bark Notify - 通过 iOS Bark 应用在 AI Agent 会话结束或需要用户输入时自动发送推送通知。

**支持两个 AI Agent**：
- **Claude Code**：通过 Skill Hook 实现
- **Hermes Agent**：通过 Plugin Hook 实现

## 快速开始

### Claude Code（推荐）

```bash
# 1. 安装
ln -s ~/bark-notify-skill/skill-hook ~/.claude/skills/bark-notify-hook

# 2. 配置 device key 在 ~/.claude/settings.json
"BARK_DEVICE_KEY": "your_key_here"

# 3. 安装 hooks
/bark-notify-hook install

# 4. 完成！现在会自动推送：
#    - 会话结束时
#    - 权限请求时
#    - 需要输入时
```

### Hermes Agent

```bash
# 1. 安装
cp -r bark-notify-skill/hermes-plugin ~/.hermes/plugins/bark-notify

# 2. 配置 device key 在 ~/.hermes/.env
BARK_DEVICE_KEY=your_key_here

# 3. 启用插件
hermes plugins enable bark-notify
```

## 架构说明

### Claude Code Skill Hook（skill-hook/ 目录）

```
用户运行 /bark-notify-hook install
    ↓
添加 hooks 到 ~/.claude/settings.json
    ↓
会话结束 → hook.py → send_bark() → HTTP POST
权限请求 → hook_permission.py → send_bark() → HTTP POST
需要输入 → hook_user_input.py → send_bark() → HTTP POST
    ↓
iPhone 收到推送
```

**核心文件**：
- `skill-hook/run.py` - 安装/卸载/测试工具
- `skill-hook/hook.py` - SessionEnd hook 脚本
- `skill-hook/hook_permission.py` - PermissionRequest hook 脚本
- `skill-hook/hook_user_input.py` - Elicitation hook 脚本
- `skill-hook/bark_send.py` - 核心推送实现

### Hermes Agent Plugin Hook（hermes-plugin/ 目录）

```
post_llm_call → _store_response() → OrderedDict (限制 50 条)
                                         ↓
on_session_end → _send_bark() → Threading (daemon)
    ↓
iPhone 收到推送（带 Hermes 图标）
```

**核心文件**：
- `hermes-plugin/__init__.py` - Hook 注册和实现（带 Hermes 图标）
- `hermes-plugin/plugin.yaml` - Plugin 元数据

## 修改指南

### Claude Code：修改推送参数

编辑 `skill-hook/bark_send.py` 的 `send_bark()` 函数：

```python
payload = {
    "title": title,
    "body": body or "✅ 任务已完成",
    "group": "claude",        # 修改默认分组
    "sound": "minuet",        # 修改默认铃声
    "isArchive": 1,           # 是否归档
}
```

### Hermes Agent：修改触发条件

编辑 `hermes-plugin/__init__.py` 的 `_on_session_end()` 函数：

```python
# 修改铃声
def _on_session_end(...):
    if completed and not interrupted:
        sound = "minuet"      # 正常完成
    elif interrupted:
        sound = "alarm"       # 中断
    else:
        sound = "chime"       # 其他
```

## 故障排查

| 症状 | 可能原因 | 解决方法 |
|------|---------|---------|
| 没有收到推送 | BARK_DEVICE_KEY 未设置 | 检查配置文件中的 env 配置 |
| Claude Code hooks 不触发 | hooks 未安装 | 运行 `/bark-notify-hook install` |
| Hermes 插件不工作 | 插件未启用 | 运行 `hermes plugins enable bark-notify` |
| 推送内容为空 | 会话异常结束 | 检查网络连接和 Bark App 状态 |

## 测试

### Claude Code

```bash
# 测试推送
/bark-notify-hook test

# 查看状态
/bark-notify-hook status

# 手动测试 hook 脚本
python ~/.claude/skills/bark-notify-hook/hook.py "测试消息"
```

### Hermes Agent

```bash
# 测试推送
python3 ~/.hermes/plugins/bark-notify/__init__.py

# 查看插件状态
hermes plugins list | grep bark-notify
```

## 代码结构

### Claude Code Skill Hook（skill-hook/）
```
skill-hook/
├── run.py                 # 安装/卸载/测试工具
├── hook.py                # SessionEnd hook 脚本
├── hook_permission.py     # PermissionRequest hook 脚本
├── hook_user_input.py     # Elicitation hook 脚本
├── bark_send.py           # 核心推送实现
├── SKILL.md               # 完整文档
└── README.md              # 快速开始
```

### Hermes Agent Plugin Hook（hermes-plugin/）
```
hermes-plugin/
├── __init__.py            # 主代码（带 Hermes 图标）
├── plugin.yaml            # 插件配置
└── README.md              # 使用说明
```

## 相关资源
- Bark 官网: https://bark.day.app/
- Bark API 文档: `barkApi.md`
- Claude Code 文档: https://claude.ai/code
- Hermes Agent 文档: https://hermes-agent.nousresearch.com/docs/
