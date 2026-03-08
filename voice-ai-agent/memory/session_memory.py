import json
import os
from typing import Any, Dict, Optional

import redis


def _redis_client() -> redis.Redis:
    url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    return redis.from_url(url)


def get_session_key(session_id: str) -> str:
    return f"session:{session_id}:state"


def get_session_state(session_id: str) -> Dict[str, Any]:
    client = _redis_client()
    raw = client.get(get_session_key(session_id))
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except Exception:
        return {}


def set_session_state(session_id: str, state: Dict[str, Any], ttl_seconds: Optional[int] = 3600) -> None:
    client = _redis_client()
    key = get_session_key(session_id)
    client.set(key, json.dumps(state), ex=ttl_seconds)

