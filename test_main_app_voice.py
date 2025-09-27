#!/usr/bin/env python3
"""
Test script to verify voice integration in main EmpathyWave app
"""
import requests
import json
import time

def test_voice_chat():
    """Test voice-enabled chat with the main app"""
    print("🧪 Testing Voice Integration in Main EmpathyWave App")
    print("=" * 50)
    
    # Test chat endpoint with voice enabled
    url = "http://127.0.0.1:5000/api/chat"
    
    test_data = {
        "message": "Hello, can you tell me about your voice features?",
        "enable_voice": True
    }
    
    print(f"📤 Sending request to: {url}")
    print(f"📝 Message: {test_data['message']}")
    print(f"🔊 Voice enabled: {test_data['enable_voice']}")
    print()
    
    try:
        response = requests.post(url, json=test_data, timeout=30)
        
        print(f"📨 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            print("✅ Response received successfully!")
            print(f"🤖 Bot response: {data.get('response', 'No response')[:100]}...")
            print()
            
            # Check voice response
            voice_response = data.get('voice_response')
            if voice_response:
                print("🔊 Voice Response Details:")
                print(f"  Available: {voice_response.get('available')}")
                if voice_response.get('available'):
                    audio_path = voice_response.get('audio_path')
                    print(f"  Audio Path: {audio_path}")
                    
                    # Test if audio file can be accessed
                    if audio_path:
                        audio_url = f"http://127.0.0.1:5000{audio_path}"
                        print(f"  Testing audio URL: {audio_url}")
                        
                        try:
                            audio_response = requests.get(audio_url, timeout=10)
                            if audio_response.status_code == 200:
                                print(f"  ✅ Audio file accessible ({len(audio_response.content)} bytes)")
                                print(f"  🎵 Content-Type: {audio_response.headers.get('Content-Type', 'Unknown')}")
                            else:
                                print(f"  ❌ Audio file not accessible (Status: {audio_response.status_code})")
                        except Exception as e:
                            print(f"  ❌ Error accessing audio file: {e}")
                else:
                    error = voice_response.get('error', 'Unknown error')
                    print(f"  ❌ Error: {error}")
            else:
                print("❌ No voice response in data")
                
        else:
            print(f"❌ Request failed with status {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - Is the main app running on port 5000?")
        print("💡 Start it with: python enhanced_chat_app.py")
    except Exception as e:
        print(f"❌ Error: {e}")

def check_server_status():
    """Check if the main app server is running"""
    try:
        response = requests.get("http://127.0.0.1:5000", timeout=5)
        if response.status_code == 200 or response.status_code == 404:
            print("✅ Main app server is running on port 5000")
            return True
        else:
            print(f"⚠️  Server responded with status {response.status_code}")
            return False
    except:
        print("❌ Main app server is not running on port 5000")
        return False

if __name__ == "__main__":
    print("🔍 Checking main app server status...")
    if check_server_status():
        print()
        test_voice_chat()
    else:
        print("\n💡 Please start the main app first:")
        print("   python enhanced_chat_app.py")