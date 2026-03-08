import json
import os
from typing import Any, Dict

import redis


def _redis_client() -> redis.Redis:
    url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    return redis.from_url(url)


def get_patient_key(patient_id: str) -> str:
    return f"patient:{patient_id}:profile"


def get_patient_profile(patient_id: str) -> Dict[str, Any]:
    client = _redis_client()
    raw = client.get(get_patient_key(patient_id))
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except Exception:
        return {}


def update_patient_profile(patient_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    client = _redis_client()
    key = get_patient_key(patient_id)
    current = get_patient_profile(patient_id)
    current.update(updates)
    client.set(key, json.dumps(current))
    return current

