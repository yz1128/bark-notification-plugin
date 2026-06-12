---
name: bark-notify
description: Send iOS push notifications via Bark after completing tasks. Automatically triggers on task completion to notify your iPhone.
---

# Bark Notify - iOS Push Notification

## Overview

在任务完成后自动向你的 iPhone 发送 Bark 推送通知。适用于长时间运行的任务、后台操作或需要及时了解完成状态的场景。

## When to Use

- 长时间运行的任务完成后需要通知（代码生成、测试、部署）
- 后台任务执行完毕时
- 需要在手机上及时查看任务结果摘要

## Setup

1. 在 iPhone 上安装 Bark App：https://bark.day.app/
2. 打开 Bark，复制你的 device key（类似 `eUt43wGYCe6YpDWMiRxPgX`）
3. 设置环境变量：
   ```bash
   # 在 ~/.claude/settings.json 的 env 中添加
   "BARK_DEVICE_KEY": "your_device_key_here"
   ```

## Usage

### 方法 1：手动推送（立即发送）

在任何任务完成后，调用此 skill 发送通知：

```bash
# 发送简单通知
/bark-notify "任务已完成"

# 发送带标题的通知
/bark-notify "代码审查完成" "发现 3 个问题需要修复，详见 PR #123"

# 发送分组通知
/bark-notify "部署成功" "生产环境已更新到 v2.1.0" --group "deploy"
```

### 方法 2：Hook 模式（自动触发）

**注意：此功能需要 Claude Code 支持 session_end hook，当前版本可能不支持。**

如果你的 Claude Code 版本支持 Python 插件 hook，可以启用自动通知：

```bash
# 检查是否支持 hook
ls ~/.claude/plugins/bark-notify/__init__.py

# 如果文件存在，说明 hook 已安装
# 每次会话结束时会自动发送通知
```

## Command Reference

### bark_send

发送 Bark 推送通知

**参数：**
- `title` (必需): 通知标题
- `body` (可选): 通知内容，默认为 "✅ 任务已完成"
- `--group` (可选): 分组名称，默认为 "claude"
- `--sound` (可选): 铃声名称，默认为 "minuet"
- `--url` (可选): 点击通知后打开的 URL

**示例：**

```bash
# 基本使用
bark_send "编译完成"

# 完整参数
bark_send "测试通过" "所有 127 个测试用例已通过" --group "ci" --sound "bell"

# 带跳转链接
bark_send "PR 已创建" "请查看 PR #456" --url "https://github.com/user/repo/pull/456"
```

### bark_notify_task

在任务完成后发送通知（包装命令）

**用法：**
```bash
bark_notify_task <command>
```

**示例：**
```bash
# 在测试完成后通知
bark_notify_task "npm test"

# 在构建完成后通知
bark_notify_task "make build"

# 在部署完成后通知
bark_notify_task "kubectl apply -f deploy.yaml"
```

## Implementation

当被调用时，执行以下操作：

1. 读取 `BARK_DEVICE_KEY` 环境变量
2. 提取任务摘要（最后一条 AI 响应的前 200 字符）
3. 通过 Bark API 发送 POST 请求：
   ```
   POST https://api.day.app/{device_key}
   Content-Type: application/json
   
   {
     "title": "Hermes",
     "body": "任务摘要...",
     "group": "claude",
     "sound": "minuet",
     "isArchive": 1
   }
   ```

## Error Handling

- 如果 `BARK_DEVICE_KEY` 未设置，输出警告但不中断任务
- 网络错误会记录但不影响主任务执行
- 推送在后台线程执行，不阻塞响应

## Bark API Reference

参考文档：`~/.claude/plugins/bark-notify/barkApi.md`

支持的参数：
- `title`: 推送标题
- `body`: 推送内容
- `group`: 消息分组
- `sound`: 铃声（minuet, bell, chime 等）
- `icon`: 自定义图标 URL
- `url`: 点击跳转 URL
- `isArchive`: 是否归档（1=是）
- `badge`: 角标数字

## Tips

1. **分组管理**：为不同类型的任务设置不同的 group
   - `ci`: CI/CD 通知
   - `deploy`: 部署通知
   - `review`: 代码审查通知
   - `claude`: 默认 Claude 任务

2. **铃声选择**：
   - `minuet`: 默认，轻柔
   - `bell`: 清脆，适合重要通知
   - `chime`: 柔和，适合提醒类
   - `alarm`: 紧急，适合错误通知

3. **内容优化**：通知内容会自动截断到 200 字符，确保关键信息在前面

## Troubleshooting

### 收不到推送？

1. 检查 device key 是否正确：
   ```bash
   echo $BARK_DEVICE_KEY
   ```

2. 测试 Bark API：
   ```bash
   curl "https://api.day.app/${BARK_DEVICE_KEY}/测试/测试推送"
   ```

3. 检查手机 Bark App 是否在线

4. 查看 Claude 日志：
   ```bash
   # 查找 bark 相关日志
   grep -i bark ~/.claude/*.log
   ```

### SSL 连接错误？

如果遇到 SSL 错误，可能是系统证书问题。Python 脚本会使用 `ssl.create_default_context()` 处理。

## Examples

### Example 1: 代码生成完成通知
```
用户: "帮我重构这个 auth 模块"
AI: [执行重构...]
AI: "重构完成，已更新 5 个文件，所有测试通过。"
→ 推送: "Hermes" / "重构完成，已更新 5 个文件，所有测试通过。"
```

### Example 2: 测试结果通知
```bash
bark_notify_task "npm test"
→ 推送: "测试完成" / "127 passed, 0 failed"
```

### Example 3: 部署通知
```bash
bark_send "部署成功" "v2.1.0 已上线到生产环境" --group "deploy" --url "https://dashboard.example.com"
→ 推送标题: "部署成功"
→ 推送内容: "v2.1.0 已上线到生产环境"
→ 分组: deploy
→ 点击跳转: https://dashboard.example.com
```
