#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 hook 脚本
"""
import json
import subprocess
import sys

# 模拟 Stop hook 的 JSON 输入
test_data = {
    "hook_event_name": "Stop",
    "session_id": "test-session",
    "cwd": "C:/Users/Yanz",
    "last_assistant_message": "你好！我是 claude-opus-4-8，很高兴见到你。\n\n有什么我可以帮你的吗？"
}

# 将 JSON 数据传给 hook.py
process = subprocess.Popen(
    [sys.executable, "hook.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

stdout, stderr = process.communicate(input=json.dumps(test_data))

print(f"Exit code: {process.returncode}")
print(f"Stdout: {stdout}")
print(f"Stderr: {stderr}")
