# Bark Notify Hook - 自动推送通知

Claude 完成回复时**自动**发送 Bark 推送到你的 iPhone/iPad。

## 快速开始

### 1. 安装 Skill

```bash
# 克隆到 Claude skills 目录
cd ~/.claude/skills
git clone https://github.com/yz1128/bark-notification-plugin.git
ln -s bark-notification-plugin/skill-hook bark-notify-hook
```

### 2. 配置 Device Key

在 `~/.claude/settings.json` 中添加：

```json
{
  "env": {
    "BARK_DEVICE_KEY": "your_device_key_here"
  }
}
```

获取 device key：打开 Bark App → 复制测试 URL 中的 key

### 3. 安装 Hook

在 Claude Code 中运行：

```
/bark-notify-hook install
```

### 4. 完成！

现在每次 Claude 完成回复时，你的 iPhone 会自动收到推送！

**注意**：需要重启 Claude Code 才能让 hook 配置生效。

## 命令

- `/bark-notify-hook install` - 安装 Stop hook
- `/bark-notify-hook uninstall` - 卸载 hook
- `/bark-notify-hook test` - 测试推送
- `/bark-notify-hook status` - 查看状态

## 工作原理

1. **安装时**：在 `~/.claude/settings.json` 中添加 `hooks.Stop` 配置
2. **回复完成时**：Claude Code 在主代理完成响应时自动执行 `hook.py` 脚本
3. **推送发送**：脚本调用 Bark API 发送推送到你的设备

## 文件说明

- `SKILL.md` - 完整文档
- `run.py` - Skill 入口（安装/卸载/测试）
- `hook.py` - Stop hook 脚本（每次 Claude 回复完成时触发）
- `bark_send.py` - Bark API 核心实现

## 自定义

编辑 `hook.py` 修改推送标题、分组或铃声：

```python
title = "自定义标题"  # 修改标题

result = send_bark(
    device_key, 
    title, 
    body, 
    group="custom",      # 修改分组
    sound="bell"         # 修改铃声
)
```

## 与 bark-notify 的区别

| 特性 | bark-notify | bark-notify-hook |
|------|-------------|------------------|
| 触发方式 | 手动 `/bark-notify` | 自动（Stop hook） |
| 触发时机 | 用户手动调用时 | 每次 Claude 回复完成时 |
| 使用场景 | 需要控制何时推送 | 希望实时获知 Claude 回复 |
| 配置 | 无需配置 | 需要安装 hook |

## License

MIT
