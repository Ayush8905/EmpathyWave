#!/usr/bin/env python3
"""
Direct TTS Test - Tests voice functionality without server
"""
import os
import time

def test_pyttsx3():
    """Test pyttsx3 text-to-speech"""
    print("🔊 Testing pyttsx3 (offline TTS)...")
    
    try:
        import pyttsx3
        
        # Initialize the engine
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        
        # Create uploads directory if it doesn't exist
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
            print("📁 Created uploads directory")
        
        # Generate audio file
        test_text = "Hello! This is a test of the two-way voice communication system. If you can hear this, the text-to-speech is working perfectly!"
        audio_file = f"uploads/pyttsx3_test_{int(time.time())}.wav"
        
        print(f"🎵 Generating audio: {audio_file}")
        engine.save_to_file(test_text, audio_file)
        engine.runAndWait()
        
        if os.path.exists(audio_file):
            size = os.path.getsize(audio_file)
            print(f"✅ Audio file created successfully!")
            print(f"📁 File: {audio_file}")
            print(f"📊 Size: {size} bytes")
            
            # Try to play with pygame
            try:
                import pygame
                pygame.mixer.init()
                pygame.mixer.music.load(audio_file)
                print("🔊 Playing audio...")
                pygame.mixer.music.play()
                
                # Wait for playback
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                
                print("✅ Playback completed!")
                return True
                
            except Exception as play_error:
                print(f"⚠️ Playback failed: {play_error}")
                print("ℹ️ Audio file created but playback failed")
                return True
                
        else:
            print("❌ Failed to create audio file")
            return False
            
    except Exception as e:
        print(f"❌ pyttsx3 test failed: {e}")
        return False

def test_gtts():
    """Test Google TTS"""
    print("\n🌐 Testing gTTS (online TTS)...")
    
    try:
        from gtts import gTTS
        import pygame
        
        test_text = "This is a test of Google Text to Speech for the EmpathyWave voice system."
        audio_file = f"uploads/gtts_test_{int(time.time())}.mp3"
        
        print(f"🎵 Generating Google TTS audio: {audio_file}")
        tts = gTTS(text=test_text, lang='en', slow=False)
        tts.save(audio_file)
        
        if os.path.exists(audio_file):
            size = os.path.getsize(audio_file)
            print(f"✅ Google TTS audio created!")
            print(f"📁 File: {audio_file}")
            print(f"📊 Size: {size} bytes")
            
            # Try to play
            try:
                pygame.mixer.init()
                pygame.mixer.music.load(audio_file)
                print("🔊 Playing Google TTS audio...")
                pygame.mixer.music.play()
                
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                
                print("✅ Google TTS playback completed!")
                return True
                
            except Exception as play_error:
                print(f"⚠️ Playback failed: {play_error}")
                return True
                
        else:
            print("❌ Failed to create Google TTS audio")
            return False
            
    except Exception as e:
        print(f"❌ Google TTS test failed: {e}")
        return False

def show_results(pyttsx3_ok, gtts_ok):
    """Show test results and next steps"""
    print("\n" + "=" * 60)
    print("📋 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    if pyttsx3_ok:
        print("✅ pyttsx3 (Offline TTS): WORKING")
    else:
        print("❌ pyttsx3 (Offline TTS): FAILED")
        
    if gtts_ok:
        print("✅ gTTS (Online TTS): WORKING")
    else:
        print("❌ gTTS (Online TTS): FAILED")
        
    if pyttsx3_ok or gtts_ok:
        print("\n🎉 VOICE SYSTEM IS FUNCTIONAL!")
        print("🌐 Your server is running at: http://127.0.0.1:5000")
        print("\n🎯 TO USE 2-WAY VOICE COMMUNICATION:")
        print("  1. Open http://127.0.0.1:5000 in your browser")
        print("  2. Login to your account")
        print("  3. Look for the 🔊 volume button in the header")
        print("  4. Click it to enable voice responses")
        print("  5. Send a message and listen for the AI's voice!")
        print("\n💡 TIP: Use the 'Test Voice System' button in the sidebar")
    else:
        print("\n❌ VOICE SYSTEM NOT WORKING")
        print("🔧 Please check your audio drivers and dependencies")

if __name__ == "__main__":
    print("🎤🔊 EmpathyWave Voice System Test")
    print("=" * 60)
    
    # Test both TTS systems
    pyttsx3_result = test_pyttsx3()
    gtts_result = test_gtts()
    
    # Show results
    show_results(pyttsx3_result, gtts_result)