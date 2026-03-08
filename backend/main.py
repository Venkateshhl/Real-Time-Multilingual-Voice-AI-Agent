from fastapi import FastAPI, WebSocket
import time
import os
from services.speech_to_text.stt import transcribe
from services.language_detection.lang_detect import detect_language
from agent.reasoning.agent import process_request
from services.text_to_speech.tts import text_to_speech
from memory.session_memory.session import get_session, set_session

# Set API key - in production, use environment
# os.environ['OPENAI_API_KEY'] = 'your_openai_api_key'

app = FastAPI()

@app.get("/")
def health():
    return {"status": "running"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    session_id = f"session_{id(websocket)}"
    context = get_session(session_id)
    try:
        while True:
            start_time = time.time()
            audio_data = await websocket.receive_bytes()
            
            # Speech-to-Text
            text = transcribe(audio_data)
            
            # Language Detection
            lang = detect_language(text)
            
            # AI Agent Processing
            response_text = process_request(text, lang, context)
            
            # Update Session Memory
            context['last_interaction'] = text
            context['last_response'] = response_text
            set_session(session_id, context)
            
            # Text-to-Speech
            audio_response = text_to_speech(response_text, lang)
            
            end_time = time.time()
            latency = end_time - start_time
            print(f"Total latency: {latency:.2f} seconds")
            
            await websocket.send_bytes(audio_response)
    except Exception as e:
        print(f"Error: {e}")
        await websocket.close()