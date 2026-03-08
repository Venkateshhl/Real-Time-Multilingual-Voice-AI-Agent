import os
import time
from dataclasses import dataclass
from typing import Any, Dict

from openai import OpenAI

from agent.prompt import BASE_SYSTEM_PROMPT


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@dataclass
class AgentResult:
    payload: Dict[str, Any]
    latency_ms: float


def call_agent(user_text: str, language: str) -> AgentResult:
    """
    Call the LLM to interpret user intent and extract structured fields.
    """
    start = time.perf_counter()

    messages = [
        {"role": "system", "content": BASE_SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"Language: {language}\nUser request: {user_text}\nReturn JSON only.",
        },
    ]

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=messages,
            temperature=0.2,
        )
        # Simple extraction: we expect the model to return JSON as the first output text.
        content = response.output[0].content[0].text
    except Exception:
        content = '{"intent": "unknown"}'

    latency_ms = (time.perf_counter() - start) * 1000

    # Best-effort JSON parsing.
    import json

    try:
        payload = json.loads(content)
    except Exception:
        payload = {"intent": "unknown", "raw": content}

    return AgentResult(payload=payload, latency_ms=latency_ms)

