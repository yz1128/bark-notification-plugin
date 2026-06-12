"""Bark Notify Plugin — Send iOS push notifications when tasks complete."""

import logging
import os
import threading
import urllib.request
import urllib.parse
import json
from collections import OrderedDict

logger = logging.getLogger(__name__)

# Store last response per session (bounded to prevent leaks)
_responses: OrderedDict[str, dict] = OrderedDict()
_MAX_STORED = 50


def _store_response(session_id: str, data: dict):
    """Store response data, evicting oldest if over limit."""
    _responses[session_id] = data
    _responses.move_to_end(session_id)
    while len(_responses) > _MAX_STORED:
        _responses.popitem(last=False)


def _pop_response(session_id: str) -> dict | None:
    """Retrieve and remove stored response for a session."""
    return _responses.pop(session_id, None)


def _on_post_llm_call(
    session_id: str,
    user_message: str,
    assistant_response: str,
    conversation_history: list,
    model: str,
    platform: str,
    **kwargs,
):
    """Capture the final response for notification body."""
    _store_response(session_id, {
        "response": assistant_response or "",
        "model": model,
        "platform": platform,
        "user_message": user_message or "",
    })


def _send_bark(device_key: str, title: str, body: str, group: str = "hermes"):
    """Send a Bark notification (non-blocking, fire-and-forget)."""
    url = f"https://api.day.app/{device_key}"
    payload = json.dumps({
        "title": title,
        "body": body,
        "group": group,
        "sound": "minuet",
        "isArchive": 1,
    }).encode("utf-8")

    try:
        req = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode())
            if result.get("code") == 200:
                logger.info("Bark notification sent: %s", title)
            else:
                logger.warning("Bark API returned: %s", result)
    except Exception as e:
        logger.error("Bark notification failed: %s", e)


def _on_session_end(
    session_id: str,
    completed: bool,
    interrupted: bool,
    model: str,
    platform: str,
    **kwargs,
):
    """Send Bark notification when session ends."""
    device_key = os.environ.get("BARK_DEVICE_KEY")
    if not device_key:
        return

    # Only notify on successful completion
    if not completed or interrupted:
        _responses.pop(session_id, None)
        return

    stored = _pop_response(session_id)

    # Build title: "Hermes" for CLI, "Hermes (telegram)" for gateway
    if platform and platform != "cli":
        title = f"Hermes ({platform})"
    else:
        title = "Hermes"

    # Build body from stored response
    if stored and stored.get("response"):
        body = stored["response"].strip()
        # Truncate for notification preview
        if len(body) > 200:
            body = body[:197] + "..."
    else:
        body = "✅ 任务已完成"

    # Send in background thread to not block session teardown
    thread = threading.Thread(
        target=_send_bark,
        args=(device_key, title, body),
        daemon=True,
    )
    thread.start()


def register(ctx):
    """Register hooks for Bark notifications."""
    ctx.register_hook("post_llm_call", _on_post_llm_call)
    ctx.register_hook("on_session_end", _on_session_end)
    logger.info("bark-notify: registered (device_key %s)",
                "set" if os.environ.get("BARK_DEVICE_KEY") else "NOT SET")
