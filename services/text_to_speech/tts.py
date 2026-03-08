import openai

def text_to_speech(text, language):
    # Map language to voice
    voice_map = {
        'en': 'alloy',
        'hi': 'alloy',  # OpenAI supports some Indian languages
        'ta': 'alloy'
    }
    voice = voice_map.get(language, 'alloy')
    client = openai.OpenAI()  # Updated for openai>=1.0.0
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text
    )
    return response.content