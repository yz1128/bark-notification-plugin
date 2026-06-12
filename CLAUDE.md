# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

Bark Notify - 通过 iOS Bark 应用在 AI Agent 任务完成时发送推送通知。

**双模式架构**：
- **Skill 模式**（推荐）：Claude Code skill，手动调用 `/bark-notify` 发送推送
- **Plugin Hook 模式**：Python hook 插件，LLM 响应后自动推送（需框架支持）

## 快速开始

### 作为 Claude Code Skill 使用（推荐）

```bash
# 1. 安装
ln -s ~/bark-notification-plugin/skill ~/.claude/skills/bark-notify

# 2. 配置 device key 在 ~/.claude/settings.json
"BARK_DEVICE_KEY": "your_key_here"

# 3. 使用
/bark-notify "任务完成"
/bark-notify "测试通过" "所有用例已通过" --group ci
```

### 作为 Plugin Hook 使用

**注意：Claude Code 目前不支持 Python plugin hooks。**

其他框架可以将 `__init__.py` 和 `plugin.yaml` 复制到插件目录。

## 架构说明

### Skill 模式架构（skill/ 目录）

```
用户调用 /bark-notify
    ↓
run.py (Skill 入口)
    ↓
bark_send.send_bark()
    ↓
HTTP POST → https://api.day.app/{device_key}
    ↓
iPhone 收到推送
```

**核心文件**：
- `skill/run.py` - Claude Code skill 入口，解析参数并调用发送函数
- `skill/bark_send.py` - 推送核心实现，可独立使用
- `skill/bark_notify_task.py` - 命令包装器，任务完成后自动推送

### Plugin Hook 模式架构（根目录）

```
post_llm_call → _store_response() → OrderedDict (限制 50 条)
                                         ↓
立即发送 → _send_bark() → Threading (daemon)
```

**核心文件**：
- `__init__.py` - Hook 注册和实现
- `plugin.yaml` - Plugin 元数据

## 修改指南

### Skill 模式：调整推送参数

编辑 `skill/bark_send.py` 的 `send_bark()` 函数：

```python
payload = {
    "title": title,
    "body": body or "✅ 任务已完成",
    "group": "claude",        # 修改默认分组
    "sound": "minuet",        # 修改默认铃声
    "isArchive": 1,           # 是否归档
}

# 可选参数
if "level" in kwargs:         # critical/active/timeSensitive/passive
    payload["level"] = kwargs["level"]
if "badge" in kwargs:         # 角标数字
    payload["badge"] = kwargs["badge"]
```

### Plugin Hook 模式：调整触发条件

编辑 `__init__.py` 的 `_on_post_llm_call()` 函数：

```python
# 当前：每次 LLM 响应后立即发送
def _on_post_llm_call(...):
    # 立即发送通知
    thread = threading.Thread(target=_send_bark, ...)
    thread.start()

# 修改为：仅在特定条件下发送
def _on_post_llm_call(...):
    # 示例：仅在响应超过 100 字时发送
    if len(assistant_response) > 100:
        thread = threading.Thread(target=_send_bark, ...)
        thread.start()
```

## 故障排查

| 症状 | 可能原因 | 解决方法 |
|------|---------|---------|
| Skill 调用无响应 | BARK_DEVICE_KEY 未设置 | 检查 ~/.claude/settings.json 的 env 配置 |
| 推送未收到 | 网络问题或 device key 错误 | 运行 `python skill/bark_send.py "测试" "测试"` |
| 命令行乱码 | Windows 编码问题 | bark_send.py 已处理 UTF-8 编码 |
| Plugin hook 不触发 | 框架不支持 Python hooks | 使用 Skill 模式代替 |

## 测试

### 测试 Skill 模式
```bash
cd ~/bark-notification-plugin/skill
python bark_send.py "测试推送" "这是测试消息"
```

### 测试 Plugin Hook 模式
```bash
cd ~/bark-notification-plugin
python -c "
import os
os.environ['BARK_DEVICE_KEY'] = 'your_key'
from __init__ import _send_bark
_send_bark('your_key', 'Hook 测试', 'Plugin hook 工作正常')
"
```

## 代码结构

### Skill 模式（skill/ 目录）
```
skill/
├── run.py                    # Skill 入口
├── bark_send.py             # 核心：send_bark() 函数
├── bark_notify_task.py      # 包装器：执行命令后推送
├── SKILL.md                 # 完整文档
└── README.md                # 快速开始
```

### Plugin Hook 模式（根目录）
```
__init__.py                   # Hook 实现
├── register()               # 框架调用的注册入口
├── _on_post_llm_call()      # Hook: 每次响应后发送
├── _send_bark()             # 核心: HTTP POST 到 Bark API
├── _store_response()        # 缓存管理: 存储
└── _pop_response()          # 缓存管理: 取出删除

plugin.yaml                   # 插件元数据
barkApi.md                    # Bark API 完整文档
```

## 相关资源
- Bark 官网: https://bark.day.app/
- Bark API 文档: `barkApi.md`
- MCP 集成: 见 `barkApi.md` 的 MCP 章节
