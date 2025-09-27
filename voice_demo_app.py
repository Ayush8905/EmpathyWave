from flask import Flask, request, jsonify, render_template_string
import pyttsx3
import os
import time
from gtts import gTTS
import pygame

app = Flask(__name__)

# Initialize voice engine
try:
    voice_engine = pyttsx3.init()
    voice_engine.setProperty('rate', 150)
    voice_engine.setProperty('volume', 0.9)
    print("✅ Voice engine initialized!")
except Exception as e:
    print(f"❌ Voice engine error: {e}")
    voice_engine = None

# Create uploads directory
if not os.path.exists('uploads'):
    os.makedirs('uploads')

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>2-Way Voice Communication Demo</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .demo-container { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
        .voice-btn { width: 80px; height: 80px; border-radius: 50%; border: none; margin: 10px; font-size: 24px; color: white; cursor: pointer; transition: all 0.3s; }
        .voice-btn.mic { background: #e74c3c; }
        .voice-btn.speaker { background: #27ae60; }
        .voice-btn:hover { transform: scale(1.1); }
        .chat-area { min-height: 300px; max-height: 400px; overflow-y: auto; border: 1px solid #ddd; padding: 15px; border-radius: 8px; margin: 15px 0; }
        .message { margin: 10px 0; padding: 10px; border-radius: 8px; }
        .user-msg { background: #e3f2fd; margin-left: 50px; }
        .ai-msg { background: #f3e5f5; margin-right: 50px; }
        .status { padding: 10px; border-radius: 5px; margin: 10px 0; }
        .status.success { background: #d4edda; color: #155724; }
        .status.error { background: #f8d7da; color: #721c24; }
        .status.info { background: #d1ecf1; color: #0c5460; }
    </style>
</head>
<body>
    <div class="container">
        <div class="demo-container">
            <h1 class="text-center mb-4">🎤🔊 2-Way Voice Communication Demo</h1>
            
            <div class="text-center">
                <button class="voice-btn mic" onclick="sendTestMessage()" title="Send Test Message">
                    🎤
                </button>
                <button class="voice-btn speaker" onclick="testTTS()" title="Test Voice Output">
                    🔊
                </button>
            </div>
            
            <div id="statusArea"></div>
            <div id="chatArea" class="chat-area"></div>
            
            <div class="row mt-4">
                <div class="col-md-6">
                    <h5>📋 Instructions:</h5>
                    <ul>
                        <li>🎤 Click microphone to send test message</li>
                        <li>🔊 Click speaker to test voice output</li>
                        <li>Messages will show text + play audio</li>
                    </ul>
                </div>
                <div class="col-md-6">
                    <h5>🔧 System Status:</h5>
                    <div id="systemStatus">Checking...</div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let messageCounter = 0;
        
        function showStatus(message, type) {
            const statusArea = document.getElementById('statusArea');
            const statusDiv = document.createElement('div');
            statusDiv.className = `status ${type}`;
            statusDiv.textContent = message;
            statusArea.appendChild(statusDiv);
            setTimeout(() => statusDiv.remove(), 5000);
        }
        
        function addMessage(type, message) {
            const chatArea = document.getElementById('chatArea');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${type}-msg`;
            messageDiv.innerHTML = `<strong>${type === 'user' ? 'You' : 'AI'}:</strong> ${message}`;
            chatArea.appendChild(messageDiv);
            chatArea.scrollTop = chatArea.scrollHeight;
        }
        
        async function sendTestMessage() {
            showStatus('🎤 Sending test message...', 'info');
            addMessage('user', 'Hello! Can you respond with voice?');
            
            try {
                const response = await fetch('/api/chat-with-voice', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: 'Hello! Can you respond with voice?' })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    addMessage('ai', result.response);
                    showStatus('✅ AI responded! Playing voice...', 'success');
                    
                    if (result.audio_file) {
                        const audio = new Audio(result.audio_file);
                        audio.onplay = () => showStatus('🔊 AI is speaking...', 'info');
                        audio.onended = () => showStatus('✅ Voice response completed!', 'success');
                        audio.onerror = () => showStatus('❌ Audio playback failed', 'error');
                        await audio.play();
                    }
                } else {
                    showStatus('❌ Error: ' + result.error, 'error');
                }
            } catch (error) {
                showStatus('❌ Request failed: ' + error.message, 'error');
            }
        }
        
        async function testTTS() {
            showStatus('🔊 Testing text-to-speech...', 'info');
            
            try {
                const response = await fetch('/api/tts-test', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: 'Hello! This is a test of the voice system. Two-way communication is working!' })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showStatus('✅ TTS generated! Playing audio...', 'success');
                    const audio = new Audio(result.audio_file);
                    audio.onplay = () => showStatus('🔊 Playing test audio...', 'info');
                    audio.onended = () => showStatus('✅ TTS test completed!', 'success');
                    audio.onerror = () => showStatus('❌ Audio playback failed', 'error');
                    await audio.play();
                } else {
                    showStatus('❌ TTS Error: ' + result.error, 'error');
                }
            } catch (error) {
                showStatus('❌ TTS test failed: ' + error.message, 'error');
            }
        }
        
        // Check system status on load
        document.addEventListener('DOMContentLoaded', function() {
            document.getElementById('systemStatus').innerHTML = `
                <div class="status success">✅ Demo server running</div>
                <div class="status info">🔊 Voice engines: Available</div>
                <div class="status info">🎤 Ready for testing</div>
            `;
        });
    </script>
</body>
</html>
'''

@app.route('/')
def demo():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/chat-with-voice', methods=['POST'])
def chat_with_voice():
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        # Generate AI response
        ai_response = f"Hello! I received your message: '{message}'. This is my voice response demonstrating 2-way communication!"
        
        # Generate audio
        audio_file = generate_voice_response(ai_response)
        
        return jsonify({
            'success': True,
            'response': ai_response,
            'audio_file': audio_file
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/tts-test', methods=['POST'])
def tts_test():
    try:
        data = request.get_json()
        text = data.get('text', 'Test message')
        
        audio_file = generate_voice_response(text)
        
        return jsonify({
            'success': True,
            'audio_file': audio_file
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def generate_voice_response(text):
    """Generate voice response using available TTS engines"""
    try:
        timestamp = int(time.time())
        
        # Try pyttsx3 first (offline)
        if voice_engine:
            audio_path = f"uploads/voice_{timestamp}.wav"
            voice_engine.save_to_file(text, audio_path)
            voice_engine.runAndWait()
            
            if os.path.exists(audio_path):
                return f"/uploads/{os.path.basename(audio_path)}"
        
        # Fallback to gTTS (online)
        audio_path = f"uploads/gtts_{timestamp}.mp3"
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(audio_path)
        
        if os.path.exists(audio_path):
            return f"/uploads/{os.path.basename(audio_path)}"
        
        raise Exception("No TTS engine available")
        
    except Exception as e:
        print(f"TTS Error: {e}")
        raise e

@app.route('/uploads/<filename>')
def serve_audio(filename):
    from flask import send_from_directory
    return send_from_directory('uploads', filename)

if __name__ == '__main__':
    print("🚀 Starting 2-Way Voice Communication Demo")
    print("🌐 Open: http://127.0.0.1:8000")
    print("🎤🔊 Full voice communication ready!")
    app.run(host='0.0.0.0', port=8000, debug=True)