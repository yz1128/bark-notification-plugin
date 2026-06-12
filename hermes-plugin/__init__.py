"""
Bark Notify Plugin for Hermes Agent
Sends iOS push notifications via Bark when sessions end.
"""

import os
import json
import urllib.request
import urllib.parse
import logging

logger = logging.getLogger(__name__)

BARK_API_URL = "https://api.day.app"
HERMES_ICON_URL = "https://raw.githubusercontent.com/NousResearch/hermes-agent/main/website/static/img/logo.png"


def _get_device_key():
    """Get Bark device key from environment or config."""
    # Check environment variable first
    key = os.environ.get("BARK_DEVICE_KEY")
    if key:
        return key

    # Try loading from .env file
    env_file = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("BARK_DEVICE_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")

    return None


def send_bark(device_key, title, body, group="hermes", sound="minuet", icon=None):
    """Send a notification via Bark API."""
    url = f"{BARK_API_URL}/{device_key}"
    data = {
        "title": title,
        "body": body,
        "group": group,
        "sound": sound,
        "icon": icon or HERMES_ICON_URL,
    }

    encoded_data = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=encoded_data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result
    except Exception as e:
        logger.error(f"Failed to send Bark notification: {e}")
        return {"code": -1, "message": str(e)}


def _on_session_end(session_id, completed, interrupted, model, platform, **kwargs):
    """Hook called when a session ends."""
    device_key = _get_device_key()
    if not device_key:
        logger.warning("BARK_DEVICE_KEY not configured, skipping notification")
        return

    # Determine status
    if interrupted:
        status = "⚠️ 已中断"
        title = "Hermes 会话中断"
        sound = "alarm"
    elif completed:
        status = "✅ 已完成"
        title = "Hermes 任务完成"
        sound = "minuet"
    else:
        status = "ℹ️ 已结束"
        title = "Hermes 会话结束"
        sound = "chime"

    # Build body
    body_parts = [status]
    if model:
        body_parts.append(f"模型: {model}")
    if platform and platform != "cli":
        body_parts.append(f"平台: {platform}")
    if session_id:
        body_parts.append(f"ID: {session_id[:8]}...")

    body = "\n".join(body_parts)

    # Send notification with Hermes icon
    result = send_bark(device_key, title, body, sound=sound)
    if result.get("code") == 200:
        logger.info(f"Bark notification sent for session {session_id}")
    else:
        logger.warning(f"Bark notification failed: {result}")


def register(ctx):
    """Register the plugin hook."""
    ctx.register_hook("on_session_end", _on_session_end)
    logger.info("Bark notify plugin registered")
