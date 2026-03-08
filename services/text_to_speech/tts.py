import openai

def text_to_speech(text, language):
    # Map language to voice
    voice_map = {
        'en': 'alloy',
        'hi': 'alloy',  # OpenAI supports some Indian languages
        'ta': 'alloy'
    }
    voice = voice_map.get(language, 'alloy')
    response = openai.Audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text
    )
    return response.content