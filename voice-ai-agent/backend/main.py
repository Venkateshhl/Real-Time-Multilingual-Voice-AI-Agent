from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
import time
import uuid

from agent.reasoning import call_agent
from memory.session_memory import get_session_state, set_session_state
from memory.persistent_memory import update_patient_profile
from services.language_detection import detect_language
from services.speech_to_text import transcribe_audio
from services.text_to_speech import synthesize_speech
from backend.api.appointments import router as appointments_router
from backend.api.campaigns import router as campaigns_router


logger = logging.getLogger("voice-ai-backend")
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="2Care.ai Voice AI Agent", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "running"}


app.include_router(appointments_router)
app.include_router(campaigns_router)


@app.websocket("/ws/voice")
async def voice_ws(websocket: WebSocket):
    """
    WebSocket endpoint for real-time audio streaming.
    The client should send small audio chunks (e.g. 100–300ms) as binary frames.
    The server returns synthesized audio frames as binary.
    Latency for STT, agent reasoning, and TTS is measured per turn and logged.
    """
    await websocket.accept()
    session_id = str(uuid.uuid4())
    logger.info("Voice WebSocket connection accepted session_id=%s", session_id)
    try:
        while True:
            message = await websocket.receive_bytes()

            t_stt_start = time.perf_counter()
            text, stt_ms = transcribe_audio(message)
            t_stt_end = time.perf_counter()

            lang = detect_language(text)

            state = get_session_state(session_id)
            state["last_user_utterance"] = text
            state["language"] = lang

            agent_result = call_agent(text, lang)
            state["last_agent_payload"] = agent_result.payload

            # Simple example of persistent memory update: track preferred language.
            patient_id = state.get("patient_id", "anonymous")
            update_patient_profile(patient_id, {"preferred_language": lang})

            set_session_state(session_id, state)

            t_tts_start = time.perf_counter()
            reply_text = _render_reply(agent_result.payload, lang)
            audio_bytes, tts_ms = synthesize_speech(reply_text, language=lang)
            t_tts_end = time.perf_counter()

            total_ms = (t_tts_end - t_stt_start) * 1000

            logger.info(
                "latency_ms session_id=%s stt=%.1f agent=%.1f tts=%.1f total=%.1f",
                session_id,
                stt_ms,
                agent_result.latency_ms,
                tts_ms,
                total_ms,
            )

            await websocket.send_bytes(audio_bytes)
    except WebSocketDisconnect:
        logger.info("Voice WebSocket disconnected session_id=%s", session_id)


def _render_reply(agent_payload: dict, language: str) -> str:
    """
    Very small NLG layer that converts the agent's structured payload
    into a user-facing sentence. For the assignment we keep this simple
    and primarily in English, but this is where multilingual templates
    would live.
    """
    intent = agent_payload.get("intent", "unknown")

    if intent == "book":
        specialty = agent_payload.get("doctor_specialty", "doctor")
        date = agent_payload.get("date", "the requested date")
        time_ = agent_payload.get("time", "a suitable time")
        return f"I will book an appointment with a {specialty} on {date} at {time_}."

    if intent == "reschedule":
        date = agent_payload.get("date", "the new date")
        time_ = agent_payload.get("time", "the new time")
        return f"I will reschedule your appointment to {date} at {time_}."

    if intent == "cancel":
        return "I will cancel your appointment."

    if intent == "availability":
        return "I will check the doctor's availability and suggest open slots."

    return "I'm having trouble processing that request. Could you repeat?"


if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)

