#!/usr/bin/env python3
"""
Simple 2-Way Voice Communication Test
This script tests the TTS functionality directly
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

# Import the TTS function from the main app
import time

def test_voice_locally():
    """Test TTS functionality locally without server"""
    print("🔊 Testing Text-to-Speech locally...")
    
    try:
        import pyttsx3
        import pygame
        from gtts import gTTS
        
        # Test pyttsx3
        print("Testing pyttsx3...")
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        
        # Create test audio file
        test_text = "Hello! This is a test of the 2-way voice communication system. If you can hear this, everything is working!"
        
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
            
        audio_path = f"uploads/test_voice_{int(time.time())}.wav"
        
        print(f"🎵 Generating audio file: {audio_path}")
        engine.save_to_file(test_text, audio_path)
        engine.runAndWait()
        
        if os.path.exists(audio_path):
            print(f"✅ Audio file created successfully: {audio_path}")
            print(f"📁 File size: {os.path.getsize(audio_path)} bytes")
            
            # Try to play with pygame
            print("🔊 Attempting to play audio...")
            pygame.mixer.init()
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
                
            print("✅ Audio playback completed!")
            
        else:
            print("❌ Failed to create audio file")
            
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_gtts():
    """Test Google TTS"""
    print("\n🌐 Testing Google TTS...")
    
    try:
        from gtts import gTTS
        import pygame
        
        test_text = "Hello! This is Google Text to Speech test."
        
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
            
        audio_path = f"uploads/gtts_test_{int(time.time())}.mp3"
        
        print(f"🎵 Generating Google TTS audio: {audio_path}")
        tts = gTTS(text=test_text, lang='en', slow=False)
        tts.save(audio_path)
        
        if os.path.exists(audio_path):
            print(f"✅ Google TTS audio created: {audio_path}")
            print(f"📁 File size: {os.path.getsize(audio_path)} bytes")
            
            # Try to play with pygame
            print("🔊 Playing Google TTS audio...")
            pygame.mixer.init()
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()
            
            # Wait for playback
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
                
            print("✅ Google TTS playback completed!")
            
        else:
            print("❌ Failed to create Google TTS audio")
            
    except Exception as e:
        print(f"❌ Google TTS Error: {e}")

if __name__ == "__main__":
    print("🎤🔊 2-Way Voice Communication Test")
    print("=" * 50)
    
    test_voice_locally()
    test_gtts()
    
    print("\n" + "=" * 50)
    print("✅ Voice system test completed!")
    print("🌐 Server should be running at: http://127.0.0.1:5000")
    print("🎯 To test in browser:")
    print("  1. Open http://127.0.0.1:5000")
    print("  2. Login to your account")
    print("  3. Click the 🔊 volume button")
    print("  4. Send a message and listen for voice response")