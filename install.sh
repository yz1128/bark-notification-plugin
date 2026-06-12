#!/bin/bash
# Bark Notify Skill 安装脚本

set -e

echo "🔧 Bark Notify Skill 安装脚本"
echo "================================"
echo ""

# 检查 Claude skills 目录
CLAUDE_SKILLS_DIR="$HOME/.claude/skills"
if [ ! -d "$CLAUDE_SKILLS_DIR" ]; then
    echo "❌ 错误: Claude skills 目录不存在: $CLAUDE_SKILLS_DIR"
    echo "   请确保已安装 Claude Code"
    exit 1
fi

echo "✅ 找到 Claude skills 目录: $CLAUDE_SKILLS_DIR"
echo ""

# 获取项目目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_SRC="$SCRIPT_DIR/skill"
SKILL_DEST="$CLAUDE_SKILLS_DIR/bark-notify"

# 检查 skill 源目录
if [ ! -d "$SKILL_SRC" ]; then
    echo "❌ 错误: skill 目录不存在: $SKILL_SRC"
    exit 1
fi

echo "📦 源目录: $SKILL_SRC"
echo "📍 目标目录: $SKILL_DEST"
echo ""

# 询问安装方式
echo "请选择安装方式:"
echo "  1) 复制文件（独立安装，不会随 git pull 更新）"
echo "  2) 创建符号链接（推荐，会随 git pull 自动更新）"
echo ""
read -p "请输入选项 [1/2]: " INSTALL_METHOD

case "$INSTALL_METHOD" in
    1)
        echo ""
        echo "📋 复制文件到 $SKILL_DEST ..."
        cp -r "$SKILL_SRC" "$SKILL_DEST"
        echo "✅ 文件复制完成"
        ;;
    2)
        echo ""
        echo "🔗 创建符号链接..."
        ln -sf "$SKILL_SRC" "$SKILL_DEST"
        echo "✅ 符号链接创建完成"
        ;;
    *)
        echo "❌ 无效选项"
        exit 1
        ;;
esac

echo ""
echo "✅ Bark Notify Skill 安装成功！"
echo ""

# 检查环境变量
SETTINGS_FILE="$HOME/.claude/settings.json"
if [ -f "$SETTINGS_FILE" ]; then
    if grep -q "BARK_DEVICE_KEY" "$SETTINGS_FILE"; then
        echo "✅ 检测到 BARK_DEVICE_KEY 已配置"
        echo ""
        echo "🎉 安装完成！现在可以使用："
        echo "   /bark-notify \"测试推送\""
    else
        echo "⚠️  未检测到 BARK_DEVICE_KEY 配置"
        echo ""
        echo "请在 $SETTINGS_FILE 的 env 中添加："
        echo ""
        echo "  \"BARK_DEVICE_KEY\": \"your_device_key_here\""
        echo ""
        echo "获取 device key："
        echo "  1. 打开 Bark App"
        echo "  2. 复制测试 URL 中的 key"
        echo "  3. 例如: https://api.day.app/ABC123/test"
        echo "     则 device key 为: ABC123"
    fi
else
    echo "⚠️  未找到 Claude settings 文件: $SETTINGS_FILE"
    echo ""
    echo "请手动创建并配置 BARK_DEVICE_KEY"
fi

echo ""
echo "📚 更多使用说明："
echo "   cat $SKILL_DEST/README.md"
echo ""
