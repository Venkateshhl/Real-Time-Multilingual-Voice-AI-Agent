# Architecture – 2Care.ai Real-Time Multilingual Voice AI Agent

## 1. High-Level Flow

```text
User Speech
  ↓
WebSocket (/ws/voice)
  ↓
Speech-to-Text (STT)
  ↓
Language Detection
  ↓
LLM Agent (intent extraction)
  ↓
Tool Orchestration (appointment APIs)
  ↓
Text Response
  ↓
Text-to-Speech (TTS)
  ↓
WebSocket Audio Response
```

The entire loop is optimized for low latency by:

- Keeping a single persistent WebSocket connection.
- Using lightweight JSON payloads for intent and scheduling tools.
- Measuring and logging latency for STT, LLM, and TTS separately.

## 2. Components

- `backend/main.py`
  - FastAPI application.
  - `/health` endpoint for liveness checks.
  - `/ws/voice` WebSocket for streaming audio in and audio out.
  - Includes routers from `backend/api/appointments.py` and `backend/api/campaigns.py`.

- `services/speech_to_text.py`
  - Abstracts STT implementation (`transcribe_audio`).
  - Returns transcribed text and per-stage latency.
  - Can be wired to Whisper/OpenAI/other STT.

- `services/language_detection.py`
  - Wraps `langdetect` to infer language codes (`en`, `hi`, `ta`).
  - Used to:
    - Adapt prompts for the LLM.
    - Persist user language preferences.

- `agent/prompt.py`
  - Defines the system prompt and JSON schema for intents:
    - `intent` – book, reschedule, cancel, availability, etc.
    - `doctor_specialty`, `doctor_id`, `date`, `time`, `language`.

- `agent/reasoning.py`
  - `call_agent` sends a compact conversation (system + user) to the LLM.
  - Expects a JSON-only response and parses it into `AgentResult`.
  - Measures and returns agent latency.

- `memory/session_memory.py`
  - Session-scoped state using Redis:
    - Last user utterance.
    - Last agent payload.
    - Language, inferred `patient_id`, and pending intent details.

- `memory/persistent_memory.py`
  - Long-lived patient profile, also in Redis:
    - `preferred_language`.
    - Room for `past_appointments`, `preferred_doctor`, etc.

- `scheduler/appointment_engine.py`
  - SQLAlchemy models:
    - `Appointment(id, patient_id, doctor_id, specialty, date, time, status)`.
    - `DoctorSchedule(id, doctor_id, date, slot)`.
  - Core functions:
    - `get_available_slots(doctor_id, date)`
    - `book_appointment(patient_id, doctor_id, specialty, date, time_)`
    - `cancel_appointment(appointment_id)`
    - `reschedule_appointment(appointment_id, new_date, new_time)`
  - Validation:
    - No past-time bookings.
    - Slot must exist in `DoctorSchedule`.
    - Slot must not already be booked (`status="booked"`).

- `scheduler/campaigns.py`
  - Simple outbound campaign scheduler:
    - `schedule_reminder(patient_id, phone_number, scheduled_at, message)`.
    - Stores `OutboundCall` objects in memory for demo purposes.

- `backend/api/appointments.py`
  - HTTP APIs that act as tools for the LLM:
    - `GET /appointments/availability/{doctor_id}/{date}`
    - `POST /appointments/book`
    - `POST /appointments/{id}/cancel`
    - `POST /appointments/{id}/reschedule`

- `backend/api/campaigns.py`
  - HTTP API for outbound reminder scheduling:
    - `POST /campaigns/reminder`
  - Designed to integrate with a background worker and telephony provider.

## 3. Memory Flows

### Session Memory

Key structure:

```json
{
  "intent": "book",
  "doctor_specialty": "cardiologist",
  "date": "tomorrow",
  "language": "hi",
  "last_user_utterance": "मुझे कल डॉक्टर से मिलना है",
  "last_agent_payload": { "...": "..." }
}
```

- Stored under `session:{session_id}:state` in Redis.
- Updated on each user turn in `backend/main.py`.
- Enables multi-turn clarification:
  - E.g., "Book appointment" → "Which doctor?" → "Cardiologist".

### Persistent Memory

Key structure:

```json
{
  "preferred_language": "hi",
  "preferred_hospital": "Apollo",
  "last_doctor": "Dr Sharma"
}
```

- Stored under `patient:{patient_id}:profile`.
- Used to:
  - Default language for speech output.
  - Prefer past doctor / hospital automatically.

## 4. Latency Design

In the WebSocket handler:

- Measure:
  - `stt_ms` – STT call (audio → text).
  - `agent_ms` – LLM call (text → JSON intent).
  - `tts_ms` – TTS call (text → audio).
  - `total_ms` – full round-trip.
- Log in a single line for easy aggregation.

To achieve **< 450 ms** in production:

- Use streaming STT and TTS with partial responses.
- Use a small, fast LLM for intent extraction.
- Run components close to each other (same region / VPC).

## 5. Outbound Campaign Mode

- Reminders are created via `POST /campaigns/reminder`.
- Each reminder is represented as an `OutboundCall`.
- A background scheduler (cron / worker) would:
  - Poll `list_scheduled_calls`.
  - Initiate a real phone call via telephony APIs.
  - Connect the audio stream to the same `/ws/voice` pipeline for live interaction.

## 6. Trade-offs & Extensions

- **STT/TTS** are stubbed for simplicity; replace with production engines for real latency and quality.
- **SQLite** was chosen for low-friction setup; switching to PostgreSQL only requires changing `DATABASE_URL`.
- Outbound campaigns are in-memory; production systems should use a message broker (e.g. Redis streams, Kafka, SQS).
- Multilingual generation currently uses simple English templates; Hindi/Tamil output can be improved via:
  - Language-specific prompts.
  - Template libraries or NLG components.

