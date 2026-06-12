# Bark Notify Plugin for Hermes Agent

Hermes 会话结束时自动发送 iOS Bark 推送通知，带有自定义 Hermes 图标。

## 功能特性

- ✅ 会话结束时自动推送通知
- ✅ 支持正常完成、中断、超时等状态
- ✅ 自定义 Hermes 图标
- ✅ 不同状态使用不同铃声
- ✅ 包含模型、平台、会话 ID 信息

## 安装

```bash
# 克隆仓库
git clone https://github.com/yz1128/bark-notify-skill.git

# 复制插件到 Hermes 插件目录
cp -r bark-notify-skill/hermes-plugin ~/.hermes/plugins/bark-notify
```

## 配置

### 1. 设置 Bark Device Key

在 `~/.hermes/.env` 文件中添加：

```bash
BARK_DEVICE_KEY=your_device_key_here
```

获取 Device Key：
1. 打开 Bark App
2. 复制测试 URL 中的 key
3. 例如：`https://api.day.app/ABC123/test` → key 为 `ABC123`

### 2. 启用插件

```bash
hermes plugins enable bark-notify
```

## 使用方法

插件会在以下情况自动触发：

- ✅ **正常完成** - 任务成功完成
- ⚠️ **中断** - 用户中断会话
- ℹ️ **结束** - 会话超时或其他原因结束

## 通知示例

**正常完成：**
```
✅ 已完成
模型: mimo-v2.5-pro
平台: cli
ID: 20260612_22...
```

**中断：**
```
⚠️ 已中断
模型: mimo-v2.5-pro
```

## 自定义配置

### 修改图标

编辑 `~/.hermes/plugins/bark-notify/__init__.py`，修改 `HERMES_ICON_URL` 变量：

```python
HERMES_ICON_URL = "https://your-icon-url.com/icon.png"
```

### 修改铃声

编辑 `_on_session_end` 函数中的 `sound` 参数：

```python
# 可用铃声：
# minuet - 默认，轻柔
# bell - 清脆
# alarm - 紧急
# chime - 柔和提醒
```

### 修改分组

编辑 `send_bark` 调用中的 `group` 参数：

```python
# 可用分组：
# hermes - 默认
# work - 工作相关
# personal - 个人事务
```

## 测试

```bash
python3 ~/.hermes/plugins/bark-notify/__init__.py
```

## 管理命令

```bash
# 查看插件状态
hermes plugins list

# 禁用插件
hermes plugins disable bark-notify

# 启用插件
hermes plugins enable bark-notify
```

## 故障排查

### 没有收到通知？

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

## 图标说明

插件使用 Hermes Agent 官方 logo 作为通知图标：
- URL: `https://raw.githubusercontent.com/NousResearch/hermes-agent/main/website/static/img/logo.png`
- 图标会在设备上自动缓存

## License

MIT
