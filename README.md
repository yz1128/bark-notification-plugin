# Bark Notification Plugin

通过 iOS [Bark](https://bark.day.app/) 应用在 AI Agent 任务完成时发送推送通知。

## 功能特性

- 🔔 任务完成自动推送到 iPhone/iPad
- 🎯 捕获 LLM 最终响应作为通知内容
- 🧵 异步发送，不阻塞会话关闭
- 💾 自动管理会话缓存（防止内存泄漏）
- 🎨 支持自定义提示音、分组、归档等参数

## 快速开始

### 1. 获取 Bark Device Key

打开 Bark 应用，复制测试 URL 中的 key：

```
https://api.day.app/your_device_key/test
                    ^^^^^^^^^^^^^^^^
                    这就是你的 device key
```

### 2. 配置环境变量

```bash
export BARK_DEVICE_KEY="your_device_key"
```

### 3. 安装插件

将插件文件复制到你的 Agent 框架的插件目录，插件会自动注册以下 hooks：
- `post_llm_call` - 捕获响应
- `on_session_end` - 发送通知

## 使用示例

插件会在以下情况自动发送通知：
- ✅ 任务成功完成（`completed=True`）
- ✅ 未被中断（`interrupted=False`）
- ✅ 已设置 `BARK_DEVICE_KEY`

通知内容包括：
- **标题**: 框架名称（如 "Hermes" 或 "Hermes (telegram)"）
- **正文**: LLM 最终响应（前 200 字符）

## 配置

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

| 文件 | 说明 |
|------|------|
| `__init__.py` | 插件主文件（hook 注册、通知发送） |
| `plugin.yaml` | 插件元数据（名称、版本、环境变量） |
| `barkApi.md` | Bark API 完整文档 |
| `CLAUDE.md` | 代码库文档（供 Claude Code 使用） |

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
