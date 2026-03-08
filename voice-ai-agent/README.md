# 2Care.ai Real-Time Multilingual Voice AI Agent

This repository implements a reference **real-time voice AI agent** for clinical appointment booking, rescheduling, cancellation, and outbound reminders, with **English, Hindi, and Tamil** support.

The backend is written in **Python (FastAPI)** and demonstrates:

- Real-time audio handling over **WebSockets**
- Multilingual STT → language detection → LLM reasoning → TTS pipeline
- **Redis**-backed session and persistent memory
- Appointment scheduling with conflict detection using **SQLAlchemy**
- Outbound reminder campaign scheduling (stubbed)
- Latency measurement and logging for STT, agent reasoning, and TTS

---

## Setup

### 1. Prerequisites

- Python 3.10+
- Redis instance (e.g. `redis://localhost:6379/0`)
- (Optional) PostgreSQL; the sample uses SQLite by default but schemas are Postgres-ready.
- OpenAI API key (for intent understanding) in `OPENAI_API_KEY`.

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the backend

```bash
cd backend
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Health check:

- `GET http://localhost:8000/health`

WebSocket endpoint:

- `ws://localhost:8000/ws/voice` – accepts binary audio frames and returns synthesized audio frames.

REST APIs:

- `GET /appointments/availability/{doctor_id}/{date}`
- `POST /appointments/book`
- `POST /appointments/{appointment_id}/cancel`
- `POST /appointments/{appointment_id}/reschedule`
- `POST /campaigns/reminder`

---

## Architecture Overview

High-level pipeline:

```text
User Speech
  → WebSocket (/ws/voice)
  → Speech-to-Text (services.speech_to_text)
  → Language Detection (services.language_detection)
  → LLM Agent (agent.reasoning with OpenAI)
  → Tool Orchestration (scheduler.appointment_engine via REST tools)
  → Text Response
  → Text-to-Speech (services.text_to_speech)
  → WebSocket Audio Response
```

**Memory design:**

- `memory.session_memory`: per-session Redis key storing current conversation state (intent, pending fields, last agent payload).
- `memory.persistent_memory`: per-patient Redis key storing long-term profile (preferred language, past appointment metadata, etc.).

**Scheduling logic:**

- `scheduler.appointment_engine`:
  - SQLAlchemy models: `Appointment`, `DoctorSchedule`.
  - Validates that:
    - Slots are in the doctor's configured schedule.
    - Slots are not already booked (`status="booked"`).
    - Appointments are not in the past.
  - Provides `book_appointment`, `cancel_appointment`, `reschedule_appointment`, `get_available_slots`.

**Outbound campaigns:**

- `scheduler.campaigns`:
  - In-memory queue of `OutboundCall` objects.
  - `backend/api/campaigns.py` exposes `POST /campaigns/reminder` to schedule reminder calls (telephony integration would be added here).

---

## Latency Measurement

Latency is measured in `backend/main.py` inside the WebSocket handler:

- `stt_ms`: time spent in `transcribe_audio`.
- `agent_result.latency_ms`: time spent in `call_agent` (LLM reasoning).
- `tts_ms`: time spent in `synthesize_speech`.
- `total_ms`: overall time from audio receipt to synthesized audio bytes.

All values are logged in a single structured log line:

```text
latency_ms session_id=<id> stt=<ms> agent=<ms> tts=<ms> total=<ms>
```

The system is designed to target **< 450 ms** total latency with a production-grade STT/TTS stack and optimized model choice (e.g., small LLM for intent extraction).

---

## Project Layout

```text
voice-ai-agent
├── backend
│   ├── main.py                 # FastAPI app + WebSocket
│   └── api
│       ├── appointments.py     # Appointment lifecycle APIs
│       └── campaigns.py        # Outbound reminder scheduling APIs
├── agent
│   ├── prompt.py               # System prompt and schema
│   └── reasoning.py            # LLM call for intent extraction
├── services
│   ├── speech_to_text.py       # STT abstraction (stub)
│   ├── text_to_speech.py       # TTS abstraction (stub)
│   └── language_detection.py   # Language detection
├── memory
│   ├── session_memory.py       # Per-session Redis state
│   └── persistent_memory.py    # Long-term patient profile
├── scheduler
│   ├── appointment_engine.py   # DB models + booking/reschedule/cancel
│   └── campaigns.py            # Outbound campaign scheduler (in-memory)
└── docs
    └── architecture.md         # Detailed architecture notes
```

---

## Docs and Diagram

- See `docs/architecture.md` for a written architecture diagram and component responsibilities.
- For submission, you can convert that into a PNG/PDF diagram using any diagramming tool (e.g., draw.io, Excalidraw, Lucidchart).

---

## Known Limitations & Next Steps

- STT/TTS are stub implementations; plug in Whisper / a low-latency TTS engine.
- Outbound calls are kept in-memory for simplicity; use a durable queue and telephony provider for production.
- SQLite is used for convenience; swap `DATABASE_URL` in `scheduler/appointment_engine.py` for PostgreSQL.
- The NLG layer for Hindi/Tamil responses is minimal; add proper multilingual templates and prompts for production quality.

