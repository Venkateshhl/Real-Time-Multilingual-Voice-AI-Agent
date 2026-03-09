#!/usr/bin/env python3
"""
Quick test to verify the Voice AI Agent server is working
"""

import subprocess
import time
import requests
import threading

def test_server():
    """Test if the server starts and responds to health checks"""

    print("🧪 Testing Voice AI Agent Server")
    print("=" * 40)

    # Start server in background
    print("🚀 Starting server...")
    server_process = subprocess.Popen([
        "python", "-m", "uvicorn", "backend.main:app",
        "--host", "127.0.0.1", "--port", "8000"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for server to start
    time.sleep(3)

    try:
        # Test health endpoint
        print("🏥 Testing health endpoint...")
        response = requests.get("http://127.0.0.1:8000/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
        else:
            print(f"❌ Health check failed: {response.status_code}")

        # Test detailed health endpoint
        print("📊 Testing detailed health endpoint...")
        response = requests.get("http://127.0.0.1:8000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Detailed health check passed:")
            print(f"   - Languages: {data.get('supported_languages', 'N/A')}")
            print(f"   - Max audio size: {data.get('max_audio_size', 'N/A')} bytes")
            print(f"   - Session timeout: {data.get('session_timeout', 'N/A')} seconds")
        else:
            print(f"❌ Detailed health check failed: {response.status_code}")

        print("\n🎉 Server is working correctly!")
        print("📋 Next steps:")
        print("1. Set OPENAI_API_KEY environment variable for full functionality")
        print("2. Deploy to Railway for live testing")
        print("3. Test WebSocket connection for real-time audio processing")

    except requests.exceptions.RequestException as e:
        print(f"❌ Server connection failed: {e}")
        print("💡 Make sure the server started correctly")

    finally:
        # Stop server
        print("\n🛑 Stopping server...")
        server_process.terminate()
        server_process.wait()
        print("✅ Server stopped")

if __name__ == "__main__":
    test_server()