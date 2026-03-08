import time
from typing import Tuple


class SpeechToTextResult(Tuple[str, float]):
    """
    (text, latency_ms)
    """


def transcribe_audio(audio_bytes: bytes, language_hint: str | None = None) -> tuple[str, float]:
    """
    Stub for STT engine.
    In a real implementation this would call Whisper or a cloud STT API.
    Returns (text, latency_ms).
    """
    start = time.perf_counter()
    # TODO: Replace with actual STT call.
    # For now we just pretend the audio is already text for demo.
    text = audio_bytes.decode("utf-8", errors="ignore")
    elapsed_ms = (time.perf_counter() - start) * 1000
    return text, elapsed_ms

