# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

Bark 通知插件 - 通过 iOS Bark 应用在 AI Agent 任务完成时发送推送通知。

**核心功能**: 捕获 LLM 响应内容，在会话成功结束时异步推送到用户的 iPhone/iPad。

## 快速开始

### 环境要求
- Python 3.7+（使用 `OrderedDict`、类型注解）
- 无第三方依赖（仅标准库）

### 配置
```bash
# 必需：设置 Bark device key（从 Bark 应用中复制）
export BARK_DEVICE_KEY="your_key_here"

# 验证插件加载
# 启动时日志会显示: "bark-notify: registered (device_key set)"
```

### 测试
```bash
# 手动测试通知发送
python -c "
from __init__ import _send_bark
_send_bark('your_key', 'Test', 'Hello from Bark!')
"

# 检查日志输出
# 成功: "Bark notification sent: Test"
# 失败: "Bark notification failed: <error>"
```

## 架构说明

### Hook 集成点
插件注册两个 hook 到宿主 Agent 框架：

- **`post_llm_call`** → 每次 LLM 响应后触发，存储响应文本
- **`on_session_end`** → 会话结束时触发，根据状态决定是否发送

### 关键设计决策

| 问题 | 解决方案 | 位置 |
|------|---------|------|
| 并发会话的响应如何关联？ | 用 `session_id` 作 key 存储到 `OrderedDict` | `_store_response()` |
| 如何防止内存泄漏？ | 限制缓存 50 条，超限驱逐最旧 | `_MAX_STORED = 50` |
| 通知发送失败会阻塞会话吗？ | 不会，用 daemon 线程异步发送 | `threading.Thread(daemon=True)` |
| 为什么截断 200 字符？ | iOS 通知预览限制 | `_on_session_end()` |

### 发送条件
仅在以下情况发送通知：
1. `completed=True`（任务完成）
2. `interrupted=False`（未被中断）
3. `BARK_DEVICE_KEY` 已设置

失败或中断的会话会清理缓存但不发送。

## 修改指南

### 调整通知参数
编辑 `_send_bark()` 的 payload：
```python
payload = json.dumps({
    "title": title,
    "body": body,
    "group": "hermes",      # 修改分组名
    "sound": "minuet",      # 更换提示音（参考 barkApi.md）
    "isArchive": 1,         # 是否归档
    "level": "active",      # 可选: critical/timeSensitive/passive
    "badge": 1,             # 可选: 角标数字
})
```

完整参数列表见 `barkApi.md` 的 "Request Parameters" 章节。

### 修改发送条件
编辑 `_on_session_end()` 的判断逻辑：
```python
# 示例：即使中断也发送（通知失败）
if not completed:
    _send_bark(device_key, f"{title} [Failed]", "任务未完成")
    return
```

### 调整截断长度
修改 `_on_session_end()` 中的截断逻辑：
```python
if len(body) > 200:  # 改为其他值
    body = body[:197] + "..."
```

## 故障排查

| 症状 | 可能原因 | 解决方法 |
|------|---------|---------|
| 没有收到通知 | `BARK_DEVICE_KEY` 未设置 | 检查启动日志是否显示 "NOT SET" |
| 通知内容为空 | `post_llm_call` 未触发 | 检查宿主框架的 hook 注册是否成功 |
| 网络错误日志 | Bark API 不可达 | 检查网络连接，确认 `api.day.app` 可访问 |
| 通知延迟 | 线程调度延迟 | 正常现象（daemon 线程 + 10s 超时） |

## 代码结构

```
__init__.py          # 插件主文件
├── register()       # 框架调用的注册入口
├── _on_post_llm_call()   # Hook: 捕获响应
├── _on_session_end()     # Hook: 发送通知
├── _send_bark()          # 核心: HTTP POST 到 Bark API
├── _store_response()     # 缓存管理: 存储
└── _pop_response()       # 缓存管理: 取出删除

plugin.yaml          # 插件元数据（名称、版本、环境变量）
barkApi.md           # Bark API 完整文档（参数、示例、MCP 配置）
```

## 相关资源
- Bark 官网: https://bark.day.app/
- Bark API 文档: `barkApi.md`
- MCP 集成: 见 `barkApi.md` 的 MCP 章节
