import time


def synthesize_speech(text: str, language: str = "en") -> tuple[bytes, float]:
    """
    Stub for TTS engine.
    In a real implementation this would call a low-latency TTS API.
    Returns (audio_bytes, latency_ms).
    """
    start = time.perf_counter()
    # TODO: Replace with actual TTS call.
    # For now we just return the input text as bytes.
    audio = text.encode("utf-8")
    elapsed_ms = (time.perf_counter() - start) * 1000
    return audio, elapsed_ms

