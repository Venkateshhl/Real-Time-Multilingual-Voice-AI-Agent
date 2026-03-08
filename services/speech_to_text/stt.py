import openai
from io import BytesIO

def transcribe(audio_bytes, language=None):
    audio_file = BytesIO(audio_bytes)
    audio_file.name = "audio.wav"  # Assume WAV format
    response = openai.Audio.transcribe(
        model="whisper-1",
        file=audio_file,
        language=language
    )
    return response['text']