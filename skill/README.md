# Bark Notify Skill - 快速开始

## 安装完成 ✅

Bark notify skill 已成功创建在 `~/.claude/skills/bark-notify/`

## 使用方法

### 1. 基本推送

在任何对话中，直接使用：

```
/bark-notify "任务完成"
```

### 2. 自动推送（SessionEnd Hook）⭐ 推荐

在 `~/.claude/settings.json` 中配置 hook，实现会话结束时自动推送：

```json
{
  "hooks": {
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python ~/.claude/skills/bark-notify/hook.py"
          }
        ]
      }
    ]
  }
}
```

配置后，每次对话结束时会自动发送 "Claude 任务完成" 推送到你的手机，无需手动调用。

### 3. 带内容的推送

```
/bark-notify "测试通过" "所有 127 个测试用例已通过"
```

### 4. 自定义分组和铃声

```
/bark-notify "部署成功" "v2.1.0 已上线到生产环境" --group deploy --sound bell
```

### 5. 带跳转链接

```
/bark-notify "PR 已创建" "请查看 #456" --url "https://github.com/user/repo/pull/456"
```

## 命令行直接使用

也可以在命令行直接调用：

```bash
# 基本使用
python ~/.claude/skills/bark-notify/bark_send.py "标题" "内容"

# 带参数
python ~/.claude/skills/bark-notify/bark_send.py "标题" "内容" --group test --sound alarm

# 包装其他命令
python ~/.claude/skills/bark-notify/bark_notify_task.py npm test
```

## 测试

发送一条测试推送：

```bash
cd ~/.claude/skills/bark-notify
python bark_send.py "测试推送" "Bark notify skill 已就绪"
```

你应该在几秒内收到 iPhone 通知！

## 配置

设备密钥已配置在 `~/.claude/settings.json`:
```json
{
  "env": {
    "BARK_DEVICE_KEY": "eUt43wGYCe6YpDWMiRxPgX"
  }
}
```

## 文件说明

- `SKILL.md` - Skill 文档和使用说明
- `bark_send.py` - 核心推送功能（可独立使用）
- `bark_notify_task.py` - 命令包装器，执行完命令后自动推送
- `run.py` - Skill 入口点，供 Claude Code 调用
- `hook.py` - SessionEnd hook 脚本，用于自动推送
- `README.md` - 本文件

## 下一步

现在你可以：

1. 在对话中测试：`/bark-notify "Hello from Claude"`
2. 查看完整文档：`cat ~/.claude/skills/bark-notify/SKILL.md`
3. 自定义铃声和分组满足不同场景

## 常用铃声

- `minuet` - 默认，轻柔
- `bell` - 清脆，适合重要通知
- `alarm` - 紧急，适合错误通知
- `chime` - 柔和提醒

## 常用分组

- `claude` - 默认，AI 对话通知
- `task` - 任务执行通知
- `deploy` - 部署相关
- `ci` - CI/CD 通知
- `test` - 测试结果

祝使用愉快！📱
