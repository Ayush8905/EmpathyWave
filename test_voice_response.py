#!/usr/bin/env python3
"""
Quick test to verify 2-way voice communication functionality
"""

import requests
import json
import time

def test_voice_response():
    """Test the voice response functionality"""
    base_url = "http://127.0.0.1:5000"
    
    # Test 1: Check if TTS endpoint exists
    print("🔊 Testing Text-to-Speech API...")
    tts_data = {
        "text": "Hello, this is a test of the voice response system.",
        "use_online": False
    }
    
    try:
        # First, let's try the TTS API directly
        tts_response = requests.post(f"{base_url}/api/text-to-speech", json=tts_data)
        print(f"TTS API Status: {tts_response.status_code}")
        
        if tts_response.status_code == 200:
            tts_result = tts_response.json()
            print(f"✅ TTS Success: {tts_result}")
        else:
            print(f"❌ TTS Failed: {tts_response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Server not running or connection failed")
        return False
    except Exception as e:
        print(f"❌ TTS Test Error: {e}")
        return False
    
    # Test 2: Check if chat with voice enabled works
    print("\n💬 Testing Chat with Voice Response...")
    chat_data = {
        "message": "Hello, how are you?",
        "enable_voice": True
    }
    
    try:
        # Note: This would require authentication in real scenario
        chat_response = requests.post(f"{base_url}/api/chat", json=chat_data)
        print(f"Chat API Status: {chat_response.status_code}")
        
        if chat_response.status_code == 200:
            chat_result = chat_response.json()
            print(f"✅ Chat Success: Response received")
            if 'voice_response' in chat_result:
                print(f"🔊 Voice Response Available: {chat_result['voice_response']}")
            else:
                print("❌ No voice response in chat result")
        else:
            print(f"❌ Chat Failed: {chat_response.text}")
            
    except Exception as e:
        print(f"❌ Chat Test Error: {e}")
        return False
    
    return True

def check_server_status():
    """Check if server is running"""
    try:
        response = requests.get("http://127.0.0.1:5000")
        return response.status_code in [200, 302]  # 302 for redirects
    except:
        return False

if __name__ == "__main__":
    print("🚀 Testing 2-Way Voice Communication System")
    print("=" * 50)
    
    if not check_server_status():
        print("❌ Server is not running! Please start enhanced_chat_app.py first")
        exit(1)
    
    print("✅ Server is running")
    test_voice_response()
    
    print("\n" + "=" * 50)
    print("Test completed. Check the results above.")