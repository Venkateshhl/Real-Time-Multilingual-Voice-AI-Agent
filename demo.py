#!/usr/bin/env python3
"""
Demo script to show how the Voice AI Agent works
This simulates the entire pipeline without requiring audio input
"""

import time
import json
from scheduler.appointment_engine.engine import check_availability, book_appointment, cancel_appointment
from services.language_detection.lang_detect import detect_language
from agent.reasoning.agent import process_request
from memory.session_memory.session import get_session, set_session

def simulate_conversation():
    """Simulate a complete conversation flow"""

    print("🎯 Voice AI Agent Demo")
    print("=" * 50)

    # Simulate session
    session_id = "demo_session_123"

    # Test cases with mock AI responses
    test_cases = [
        {
            "user_input": "Book appointment with cardiologist tomorrow",
            "expected_lang": "en",
            "mock_ai_response": "Appointment booked for cardiologist tomorrow at 10 AM",
            "description": "Booking request in English"
        },
        {
            "user_input": "मुझे कल डॉक्टर से मिलना है",
            "expected_lang": "hi",
            "mock_ai_response": "आपका कल कार्डियोलॉजिस्ट के साथ अपॉइंटमेंट 10 बजे बुक हो गया है",
            "description": "Booking request in Hindi"
        },
        {
            "user_input": "நாளை மருத்துவரை பார்க்க வேண்டும்",
            "expected_lang": "ta",
            "mock_ai_response": "உங்கள் நாளை இதயநல நிபுணருடன் 10 மணி நேர நியமனம் பதிவு செய்யப்பட்டது",
            "description": "Booking request in Tamil"
        }
    ]

    for i, test in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: {test['description']}")
        print("-" * 40)

        user_input = test["user_input"]
        print(f"👤 User: {user_input}")

        # Step 1: Language Detection
        start_time = time.time()
        detected_lang = detect_language(user_input)
        lang_time = time.time() - start_time
        print(f"🌍 Language Detected: {detected_lang} ({lang_time:.3f}s)")

        # Step 2: Get Session Context
        context = get_session(session_id)
        print(f"💭 Session Context: {context}")

        # Step 3: AI Agent Processing (Mocked for demo)
        agent_start = time.time()
        try:
            response = process_request(user_input, detected_lang, context)
        except Exception as e:
            print(f"⚠️  AI processing failed (API key needed): {str(e)}")
            response = test["mock_ai_response"]  # Use mock response
        agent_time = time.time() - agent_start
        print(f"🤖 AI Response: {response} ({agent_time:.3f}s)")

        # Step 4: Update Session Memory
        context['last_interaction'] = user_input
        context['last_response'] = response
        context['language'] = detected_lang
        set_session(session_id, context)

        # Step 5: Simulate TTS (just show text)
        tts_time = 0.1  # Mock TTS time
        print(f"🔊 TTS Generated: [Audio bytes would be sent] ({tts_time:.3f}s)")

        # Total latency
        total_time = lang_time + agent_time + tts_time
        print(f"⚡ Total Latency: {total_time:.3f}s (Target: <0.45s)")

        print()

def demonstrate_appointment_engine():
    """Show how the appointment scheduling works"""

    print("🏥 Appointment Engine Demo")
    print("=" * 50)

    # Test availability check
    print("📅 Checking availability for cardiologist tomorrow:")
    slots = check_availability("cardiologist", "tomorrow")
    print(f"Available slots: {slots}")

    # Test booking
    print("\n📝 Booking appointment:")
    result = book_appointment("patient_123", "cardiologist", "tomorrow", "10:00 AM")
    print(f"Result: {result}")

    # Check availability again
    print("\n📅 Checking availability after booking:")
    slots = check_availability("cardiologist", "tomorrow")
    print(f"Available slots: {slots}")

    # Test double booking
    print("\n🚫 Attempting double booking:")
    result = book_appointment("patient_456", "cardiologist", "tomorrow", "10:00 AM")
    print(f"Result: {result}")

    # Test cancellation
    print("\n❌ Cancelling appointment:")
    result = cancel_appointment("patient_123", "cardiologist", "tomorrow", "10:00 AM")
    print(f"Result: {result}")

    # Check availability after cancellation
    print("\n📅 Checking availability after cancellation:")
    slots = check_availability("cardiologist", "tomorrow")
    print(f"Available slots: {slots}")

def show_memory_system():
    """Demonstrate the memory system"""

    print("🧠 Memory System Demo")
    print("=" * 50)

    session_id = "demo_memory_session"

    # Show empty session
    print("📭 Initial session memory:")
    context = get_session(session_id)
    print(f"Context: {context}")

    # Add some context
    context = {
        "intent": "booking",
        "doctor": "dermatologist",
        "preferred_language": "hi"
    }
    set_session(session_id, context)

    print("\n💾 After setting context:")
    updated_context = get_session(session_id)
    print(f"Context: {updated_context}")

if __name__ == "__main__":
    print("🚀 Starting Voice AI Agent Demonstration")
    print("Note: This demo uses mock data and simulated AI responses")
    print("For full functionality, set OPENAI_API_KEY environment variable")
    print()

    # Run demonstrations
    demonstrate_appointment_engine()
    print("\n" + "="*50 + "\n")

    show_memory_system()
    print("\n" + "="*50 + "\n")

    simulate_conversation()

    print("\n🎉 Demo Complete!")
    print("To run the full voice system:")
    print("1. Set OPENAI_API_KEY=your_key")
    print("2. Run: uvicorn backend.main:app --reload")
    print("3. Connect WebSocket client to ws://localhost:8000/ws")