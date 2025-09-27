#!/usr/bin/env python3
"""
Test voice recording workflow to verify AI responses
"""
import requests
import json
import os
import time

def test_voice_to_text_api():
    """Test the voice-to-text API endpoint"""
    print("🧪 Testing Voice-to-Text API Workflow")
    print("=" * 40)
    
    # Check if there are any existing audio files to test with
    audio_files = [f for f in os.listdir('.') if f.endswith(('.wav', '.mp3', '.webm'))]
    
    if not audio_files:
        print("❌ No audio files found for testing")
        print("💡 Try recording a voice message in the web interface first")
        return
    
    # Use the first audio file found
    audio_file = audio_files[0]
    print(f"📁 Using audio file: {audio_file}")
    
    url = "http://127.0.0.1:5000/api/voice-to-text"
    
    try:
        with open(audio_file, 'rb') as f:
            files = {'audio': (audio_file, f, 'audio/wav')}
            
            print(f"📤 Sending audio to: {url}")
            response = requests.post(url, files=files, timeout=30)
            
            print(f"📨 Response Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success'):
                    print("✅ Voice-to-text processing successful!")
                    print(f"📝 Transcribed text: '{data.get('transcribed_text')}'")
                    print(f"📊 ML Analysis: {data.get('ml_analysis', {}).get('risk_level', 'Unknown')}")
                    
                    # Now test if we can send this text to chat API
                    transcribed_text = data.get('transcribed_text')
                    if transcribed_text:
                        print("\n🤖 Testing chat response to transcribed text...")
                        test_chat_with_text(transcribed_text)
                    
                else:
                    print(f"❌ Voice processing failed: {data.get('error')}")
            else:
                print(f"❌ Request failed: {response.text}")
                
    except FileNotFoundError:
        print(f"❌ Audio file not found: {audio_file}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_chat_with_text(message):
    """Test sending text to chat API"""
    url = "http://127.0.0.1:5000/api/chat"
    
    data = {
        "message": message,
        "enable_voice": True
    }
    
    try:
        response = requests.post(url, json=data, timeout=30)
        print(f"📨 Chat API Status: {response.status_code}")
        
        if response.status_code == 200:
            chat_data = response.json()
            if chat_data.get('response'):
                print("✅ Chat response received!")
                print(f"🤖 AI Response: {chat_data['response'][:100]}...")
                
                if chat_data.get('voice_response'):
                    voice_resp = chat_data['voice_response']
                    if voice_resp.get('available'):
                        print(f"🔊 Voice response available: {voice_resp.get('audio_path')}")
                    else:
                        print(f"❌ Voice response failed: {voice_resp.get('error')}")
            else:
                print(f"❌ No response in data: {chat_data}")
        else:
            print(f"❌ Chat failed: {response.text[:200]}...")
            if "login" in response.text.lower():
                print("🔐 Authentication required - please login first")
                
    except Exception as e:
        print(f"❌ Chat API error: {e}")

def check_server_and_auth():
    """Check server status and authentication"""
    try:
        # Check main page
        response = requests.get("http://127.0.0.1:5000", timeout=5)
        print(f"🌐 Server status: {response.status_code}")
        
        # Check if redirected to login
        if "login" in response.url.lower() or "login" in response.text.lower():
            print("🔐 Authentication required")
            print("💡 Please login at: http://127.0.0.1:5000")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Server check failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Checking server status...")
    if check_server_and_auth():
        test_voice_to_text_api()
    else:
        print("\n💡 Please start the server and login first:")
        print("   1. Run: python enhanced_chat_app.py")
        print("   2. Open: http://127.0.0.1:5000")
        print("   3. Login to your account")
        print("   4. Try voice recording in the web interface")