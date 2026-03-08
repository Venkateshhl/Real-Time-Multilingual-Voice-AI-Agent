# Voice AI Agent README

## Setup Instructions

1. Install Python 3.8+
2. Install dependencies: `pip install -r requirements.txt`
3. Set OpenAI API key: `export OPENAI_API_KEY=your_key`
4. Run server: `uvicorn backend.main:app --reload`

## Architecture

- **Backend**: FastAPI with WebSocket for real-time audio
- **STT**: OpenAI Whisper
- **Language Detection**: langdetect
- **Agent**: GPT-3.5-turbo with tool orchestration
- **TTS**: OpenAI TTS
- **Memory**: In-memory (session and persistent)
- **Scheduler**: Mock appointment engine

## Latency Measurement

Latency is logged in the console for each request.

Target: <450ms end-to-end.

## Features

- Multilingual support (EN, HI, TA)
- Appointment booking/cancellation/rescheduling
- Contextual memory
- Real-time voice processing

## Known Limitations

- In-memory storage (not persistent)
- Mock appointment data
- No outbound campaigns implemented
- Basic error handling

## Trade-offs

- Used OpenAI services for simplicity over custom models
- In-memory storage for quick setup vs production DB
- Mock scheduler for demo vs real validation