@echo off
REM Bark Notify Skill 安装脚本 (Windows)

echo.
echo 🔧 Bark Notify Skill 安装脚本
echo ================================
echo.

REM 检查 Claude skills 目录
set CLAUDE_SKILLS_DIR=%USERPROFILE%\.claude\skills
if not exist "%CLAUDE_SKILLS_DIR%" (
    echo ❌ 错误: Claude skills 目录不存在: %CLAUDE_SKILLS_DIR%
    echo    请确保已安装 Claude Code
    pause
    exit /b 1
)

echo ✅ 找到 Claude skills 目录: %CLAUDE_SKILLS_DIR%
echo.

REM 获取脚本目录
set SCRIPT_DIR=%~dp0
set SKILL_SRC=%SCRIPT_DIR%skill-hook
set SKILL_DEST=%CLAUDE_SKILLS_DIR%\bark-notify-hook

REM 检查 skill 源目录
if not exist "%SKILL_SRC%" (
    echo ❌ 错误: skill-hook 目录不存在: %SKILL_SRC%
    pause
    exit /b 1
)

echo 📦 源目录: %SKILL_SRC%
echo 📍 目标目录: %SKILL_DEST%
echo.

REM 询问安装方式
echo 请选择安装方式:
echo   1) 复制文件（独立安装，不会随 git pull 更新）
echo   2) 创建符号链接（推荐，会随 git pull 自动更新，需要管理员权限）
echo.
set /p INSTALL_METHOD="请输入选项 [1/2]: "

if "%INSTALL_METHOD%"=="1" (
    echo.
    echo 📋 复制文件到 %SKILL_DEST% ...
    xcopy /E /I /Y "%SKILL_SRC%" "%SKILL_DEST%" > nul
    echo ✅ 文件复制完成
) else if "%INSTALL_METHOD%"=="2" (
    echo.
    echo 🔗 创建符号链接 ^(需要管理员权限^)...
    mklink /D "%SKILL_DEST%" "%SKILL_SRC%" > nul 2>&1
    if errorlevel 1 (
        echo ❌ 创建符号链接失败，可能需要管理员权限
        echo    请以管理员身份运行此脚本，或选择方式 1
        pause
        exit /b 1
    )
    echo ✅ 符号链接创建完成
) else (
    echo ❌ 无效选项
    pause
    exit /b 1
)

echo.
echo ✅ Bark Notify Hook 安装成功！
echo.

REM 检查环境变量
set SETTINGS_FILE=%USERPROFILE%\.claude\settings.json
if exist "%SETTINGS_FILE%" (
    findstr /C:"BARK_DEVICE_KEY" "%SETTINGS_FILE%" > nul 2>&1
    if not errorlevel 1 (
        echo ✅ 检测到 BARK_DEVICE_KEY 已配置
        echo.
        echo 🎉 安装完成！现在可以使用：
        echo    /bark-notify-hook install
        echo    /bark-notify-hook test
    ) else (
        echo ⚠️  未检测到 BARK_DEVICE_KEY 配置
        echo.
        echo 请在 %SETTINGS_FILE% 的 env 中添加：
        echo.
        echo   "BARK_DEVICE_KEY": "your_device_key_here"
        echo.
        echo 获取 device key：
        echo   1. 打开 Bark App
        echo   2. 复制测试 URL 中的 key
        echo   3. 例如: https://api.day.app/ABC123/test
        echo      则 device key 为: ABC123
    )
) else (
    echo ⚠️  未找到 Claude settings 文件: %SETTINGS_FILE%
    echo.
    echo 请手动创建并配置 BARK_DEVICE_KEY
)

echo.
echo 📚 更多使用说明：
echo    type %SKILL_DEST%\README.md
echo.
pause
