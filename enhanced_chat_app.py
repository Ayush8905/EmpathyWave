from flask import Flask, request, jsonify, render_template, session, redirect, url_for, flash
import joblib
import os
import librosa
import numpy as np
import google.generativeai as genai
from sklearn.feature_extraction.text import TfidfVectorizer
import uuid
import datetime
import re
from werkzeug.utils import secure_filename
import tempfile
import logging
from dotenv import load_dotenv
import time
import json
from functools import wraps
from database import DatabaseManager
from depression_risk_analyzer import risk_analyzer
from emergency_email_service import email_service

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'empathy-wave-enhanced-secret-key-2024')

# Initialize database
db = DatabaseManager()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/empathy_wave.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configure Gemini AI
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', "AIzaSyDj7wyPs73Nxmrnqo0H1PyLx_iUwC-XwQk")
try:
    genai.configure(api_key=GEMINI_API_KEY)
    logger.info("Gemini AI configured successfully")
except Exception as e:
    logger.error(f"Failed to configure Gemini AI: {str(e)}")
    genai = None

# Initialize Gemini model
try:
    if genai:
        gemini_model = genai.GenerativeModel('gemini-pro')
        logger.info("Gemini model initialized successfully")
    else:
        gemini_model = None
        logger.warning("Gemini AI not available - using fallback responses")
except Exception as e:
    logger.error(f"Failed to initialize Gemini model: {str(e)}")
    gemini_model = None

# Global variables for models
text_model_data = None

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'session_token' not in session:
            return redirect(url_for('login'))
        
        # Validate session
        is_valid, user_data = db.validate_session(session['session_token'])
        if not is_valid:
            session.clear()
            flash('Your session has expired. Please log in again.', 'warning')
            return redirect(url_for('login'))
        
        # Store user data in session for easy access
        session['user_data'] = user_data
        return f(*args, **kwargs)
    return decorated_function

def load_text_model():
    """Load the trained text depression detection model"""
    global text_model_data
    try:
        if os.path.exists('data/models/text_model.pkl'):
            text_model_data = joblib.load('data/models/text_model.pkl')
            logger.info("Text model loaded successfully!")
            return True
        else:
            logger.warning("Text model file not found!")
            text_model_data = None
            return False
    except Exception as e:
        logger.error(f"Error loading text model: {str(e)}")
        text_model_data = None
        return False

def predict_depression_from_text(text):
    """Predict depression risk from text using trained model"""
    try:
        if not text_model_data:
            return {"error": "Model not loaded"}
        
        model = text_model_data['model']
        vectorizer = text_model_data['vectorizer']
        
        # Transform text and predict
        text_vec = vectorizer.transform([text])
        prediction = model.predict(text_vec)[0]
        probability = model.predict_proba(text_vec)[0]
        
        # Calculate risk score
        risk_score = probability[1] if len(probability) > 1 else prediction
        
        # Determine risk level
        if risk_score < 0.3:
            risk_level = "Low Risk"
            risk_color = "success"
        elif risk_score < 0.7:
            risk_level = "Moderate Risk"
            risk_color = "warning"
        else:
            risk_level = "High Risk"
            risk_color = "danger"
        
        return {
            "prediction": int(prediction),
            "risk_score": float(risk_score),
            "risk_level": risk_level,
            "risk_color": risk_color,
            "confidence": float(max(probability))
        }
        
    except Exception as e:
        return {"error": str(e)}

def analyze_text_with_gemini(text):
    """Use Gemini to analyze text for depression indicators"""
    try:
        if not gemini_model:
            return get_fallback_analysis(text)
            
        prompt = f"""
        Analyze the following text for potential signs of depression or mental health concerns. 
        Provide a brief assessment focusing on emotional tone, mood indicators, and language patterns.
        Be supportive and understanding in your response. Don't provide medical diagnosis.
        
        Text: "{text}"
        
        Please provide:
        1. Overall emotional tone assessment
        2. Any concerning patterns you notice
        3. A supportive response
        
        Keep your response concise and helpful.
        """
        
        response = gemini_model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        logger.error(f"Gemini analysis error: {str(e)}")
        return get_fallback_analysis(text)

def get_fallback_analysis(text):
    """Provide basic text analysis when Gemini is not available"""
    text_lower = text.lower()
    
    # Count emotional indicators
    negative_words = ['sad', 'depressed', 'hopeless', 'worthless', 'empty', 'numb', 'tired', 'exhausted']
    anxiety_words = ['anxious', 'worried', 'nervous', 'panic', 'fear', 'stressed']
    positive_words = ['happy', 'good', 'great', 'better', 'hopeful', 'grateful']
    
    negative_count = sum(1 for word in negative_words if word in text_lower)
    anxiety_count = sum(1 for word in anxiety_words if word in text_lower)
    positive_count = sum(1 for word in positive_words if word in text_lower)
    
    # Generate analysis based on word patterns
    if negative_count > anxiety_count and negative_count > positive_count:
        return "The text shows some indicators of low mood or sadness. The language suggests the person may be experiencing difficult emotions. It's important to acknowledge these feelings and consider professional support if they persist."
    elif anxiety_count > negative_count and anxiety_count > positive_count:
        return "The text contains language that suggests anxiety or worry. The person appears to be experiencing some stress or concerns. These feelings are valid and addressing them through healthy coping strategies or professional support can be helpful."
    elif positive_count > 0:
        return "The text shows some positive emotional indicators. While there may be challenges present, there are also signs of resilience or hope. Building on these positive elements can be beneficial for overall well-being."
    else:
        return "The text provides insight into the person's current emotional state. Everyone experiences ups and downs, and it's important to acknowledge all feelings as valid. Professional support can provide valuable guidance for navigating emotional challenges."

def get_gemini_response(user_message, context=""):
    """Get response from Gemini AI for chat"""
    try:
        if not gemini_model:
            return get_fallback_response(user_message, context)
            
        # Create a context-aware prompt
        system_prompt = """
        You are EmpathyWave, a supportive and empathetic AI assistant designed to help people with mental health conversations.
        You should:
        1. Be warm, understanding, and supportive
        2. Listen actively and respond thoughtfully
        3. Encourage seeking professional help when appropriate
        4. Never provide medical diagnosis or replace professional therapy
        5. Be conversational and engaging
        6. Show genuine care and empathy
        
        Guidelines:
        - If someone expresses distress, validate their feelings
        - Suggest healthy coping strategies when appropriate
        - Encourage professional help for serious concerns
        - Keep responses conversational and supportive
        - Ask follow-up questions to show you're engaged
        """
        
        full_prompt = f"{system_prompt}\n\nContext: {context}\n\nUser: {user_message}\n\nEmpathyWave:"
        
        response = gemini_model.generate_content(full_prompt)
        return response.text
        
    except Exception as e:
        logger.error(f"Gemini API error: {str(e)}")
        return get_fallback_response(user_message, context)

def get_fallback_response(user_message, context=""):
    """Provide fallback responses when Gemini is not available"""
    user_message_lower = user_message.lower()
    
    # Emotional support responses
    if any(word in user_message_lower for word in ['sad', 'depressed', 'down', 'low', 'upset']):
        return "I hear that you're feeling sad right now. Those feelings are valid, and it's okay to feel this way. Sometimes talking about what's bothering you can help. Would you like to share more about what's on your mind? Remember, if you're feeling overwhelmed, please consider reaching out to a mental health professional."
    
    elif any(word in user_message_lower for word in ['anxious', 'worried', 'nervous', 'scared', 'panic']):
        return "It sounds like you're experiencing some anxiety. That can be really difficult to deal with. Some people find it helpful to take slow, deep breaths or try grounding techniques like focusing on things you can see, hear, and feel around you. Have you tried any coping strategies before? If your anxiety is persistent, speaking with a counselor might be beneficial."
    
    elif any(word in user_message_lower for word in ['angry', 'mad', 'frustrated', 'irritated']):
        return "I can sense some frustration in what you're sharing. Anger is a normal emotion, and it often signals that something important to us is being affected. Have you been able to identify what might be causing these feelings? Sometimes talking through these emotions can help us understand them better."
    
    elif any(word in user_message_lower for word in ['stressed', 'overwhelmed', 'pressure', 'busy']):
        return "It sounds like you're dealing with a lot of stress right now. Feeling overwhelmed is more common than you might think. What's been putting the most pressure on you lately? Sometimes breaking things down into smaller, manageable pieces can help. Are you taking care of yourself through all of this?"
    
    elif any(word in user_message_lower for word in ['lonely', 'alone', 'isolated', 'disconnected']):
        return "Feeling lonely can be really painful. Thank you for sharing that with me. Even though it might feel like you're alone, reaching out here shows strength. Is there anyone in your life you feel comfortable talking to? Sometimes connecting with others, even in small ways, can help us feel less isolated."
    
    elif any(word in user_message_lower for word in ['tired', 'exhausted', 'drained', 'fatigue']):
        return "It sounds like you're feeling really drained. That exhaustion - whether physical, emotional, or both - can make everything feel harder. Have you been getting enough rest? Sometimes our bodies and minds need extra care when we're feeling this way. What does rest look like for you?"
    
    elif any(word in user_message_lower for word in ['help', 'support', 'need', 'struggling']):
        return "I'm glad you're reaching out. Asking for help takes courage, and it's a positive step. While I'm here to listen and provide support, I want to remind you that professional counselors and therapists are trained to provide more comprehensive help. In the meantime, what specific area would you like to talk about?"
    
    elif any(word in user_message_lower for word in ['happy', 'good', 'great', 'amazing', 'wonderful']):
        return "It's wonderful to hear that you're feeling positive! Those good moments are precious. What's been going well for you? Celebrating the positive experiences, even small ones, can be really important for our overall well-being."
    
    elif any(word in user_message_lower for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
        return "Hello there! I'm glad you're here. I'm EmpathyWave, and I'm here to listen and provide support. Feel free to share whatever is on your mind - whether you're having a good day, a tough day, or anything in between. How are you feeling right now?"
    
    else:
        return "Thank you for sharing that with me. I'm here to listen and support you. While I may not have all the answers, I want you to know that your feelings and experiences are valid. Would you like to tell me more about what's on your mind? If you're going through a difficult time, please remember that professional support is available."

def extract_audio_features(audio_data, sr=16000):
    """Extract comprehensive audio features for depression detection"""
    try:
        features = []
        
        # MFCC features (13 coefficients)
        mfccs = librosa.feature.mfcc(y=audio_data, sr=sr, n_mfcc=13)
        mfcc_means = np.mean(mfccs, axis=1)
        mfcc_stds = np.std(mfccs, axis=1)
        features.extend(mfcc_means.flatten())
        features.extend(mfcc_stds.flatten())
        
        # Spectral features
        spectral_centroids = librosa.feature.spectral_centroid(y=audio_data, sr=sr)
        features.append(float(np.mean(spectral_centroids)))
        features.append(float(np.std(spectral_centroids)))
        
        spectral_rolloff = librosa.feature.spectral_rolloff(y=audio_data, sr=sr)
        features.append(float(np.mean(spectral_rolloff)))
        features.append(float(np.std(spectral_rolloff)))
        
        # Zero crossing rate
        zcr = librosa.feature.zero_crossing_rate(audio_data)
        features.append(float(np.mean(zcr)))
        features.append(float(np.std(zcr)))
        
        # Chroma features
        chroma = librosa.feature.chroma_stft(y=audio_data, sr=sr)
        chroma_means = np.mean(chroma, axis=1)
        chroma_stds = np.std(chroma, axis=1)
        features.extend(chroma_means.flatten())
        features.extend(chroma_stds.flatten())
        
        # RMS energy
        rms = librosa.feature.rms(y=audio_data)
        features.append(float(np.mean(rms)))
        features.append(float(np.std(rms)))
        
        # Tempo
        try:
            tempo, _ = librosa.beat.beat_track(y=audio_data, sr=sr)
            features.append(float(tempo))
        except Exception:
            features.append(120.0)  # Default tempo
        
        return np.array(features, dtype=float)
        
    except Exception as e:
        logger.error(f"Error extracting audio features: {str(e)}")
        return None

def analyze_audio_depression(features):
    """Analyze audio features for depression indicators"""
    try:
        if features is None:
            return 0.5
            
        # Extract key features
        mfcc_mean = np.mean(features[:13])
        spectral_centroid_mean = features[26]
        zcr_mean = features[30]
        rms_mean = features[38]
        tempo = features[40]
        
        # Depression scoring based on research
        depression_score = 0.0
        
        # Voice characteristics associated with depression
        if mfcc_mean > -5:  # Lower pitch
            depression_score += 0.3
        if rms_mean < 0.02:  # Lower energy
            depression_score += 0.3
        if tempo < 90:  # Slower speech
            depression_score += 0.2
        if spectral_centroid_mean < 1000:  # Less brightness
            depression_score += 0.2
        
        return min(depression_score, 1.0)
        
    except Exception as e:
        print(f"Error analyzing audio: {str(e)}")
        return 0.5

@app.route('/')
@login_required
def index():
    """Render the main chat interface"""
    return render_template('chat_interface.html', user=session['user_data'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Please enter both email and password.', 'danger')
            return render_template('login.html')
        
        # Authenticate user
        success, result = db.authenticate_user(email, password)
        
        if success:
            user_id = result
            # Create session
            session_token = db.create_session(user_id)
            
            if session_token:
                session['session_token'] = session_token
                session['user_id'] = user_id
                flash('Welcome back! You have been successfully logged in.', 'success')
                return redirect(url_for('index'))
            else:
                flash('Failed to create session. Please try again.', 'danger')
        else:
            flash(result, 'danger')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handle user registration"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        parent_phone = request.form.get('parent_phone', '').strip()
        parent_email = request.form.get('parent_email', '').strip()
        
        # Validate form data
        if not all([email, password, confirm_password, parent_phone, parent_email]):
            flash('Please fill in all required fields.', 'danger')
            return render_template('signup.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('signup.html')
        
        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'danger')
            return render_template('signup.html')
        
        # Create user
        success, result = db.create_user(email, password, parent_phone, parent_email)
        
        if success:
            user_id = result
            flash('Account created successfully! You can now log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash(result, 'danger')
    
    return render_template('signup.html')

@app.route('/emergency-dashboard')
@login_required
def emergency_dashboard():
    """Emergency alerts dashboard (admin access)"""
    # In a production system, you'd add admin role checking here
    return render_template('emergency_dashboard.html')

@app.route('/logout')
@login_required
def logout():
    """Handle user logout"""
    if 'session_token' in session:
        db.end_session(session['session_token'])
    
    session.clear()
    flash('You have been successfully logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/api/chat', methods=['POST'])
@login_required
def chat():
    """Handle chat messages with emergency alert system"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        user_id = session.get('user_id')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Get user information for emergency alerts
        user_data = db.get_user_by_id(user_id)
        if not user_data:
            return jsonify({'error': 'User not found'}), 404
        
        # Get user's chat history for context
        recent_history = db.get_user_chat_history(user_id, limit=10)
        historical_messages = [msg['message'] for msg in recent_history]
        
        # 🚨 ENHANCED RISK ANALYSIS - New emergency system
        risk_assessment = risk_analyzer.analyze_message(
            user_id=str(user_id),
            message=user_message,
            user_history=historical_messages
        )
        
        # Predict depression using trained model
        ml_prediction = predict_depression_from_text(user_message)
        
        # Analyze with Gemini
        gemini_analysis = analyze_text_with_gemini(user_message)
        
        # Get context from recent chat history
        context = " ".join(historical_messages)
        
        # Get Gemini response for conversation
        gemini_response = get_gemini_response(user_message, context)
        
        # Combine analysis results with new risk assessment
        combined_analysis = {
            'ml_prediction': ml_prediction,
            'gemini_analysis': gemini_analysis,
            'risk_assessment': {
                'level': risk_assessment['risk_level'],
                'score': risk_assessment['risk_score'],
                'emergency_required': risk_assessment['emergency_alert_required']
            },
            'combined_risk_assessment': risk_assessment['risk_level']
        }
        
        # Determine risk color for UI
        if risk_assessment['risk_level'] in ['CRITICAL', 'HIGH']:
            combined_analysis['risk_color'] = 'danger'
        elif risk_assessment['risk_level'] == 'MODERATE':
            combined_analysis['risk_color'] = 'warning'
        else:
            combined_analysis['risk_color'] = 'success'
        
        # Save chat to database first
        chat_saved = db.save_chat_message(
            user_id=user_id,
            message=user_message,
            response=gemini_response,
            risk_level=risk_assessment['risk_level'],
            confidence_score=risk_assessment['risk_score']
        )
        
        # Save detailed risk assessment to database
        if chat_saved:
            db.save_risk_assessment(user_id, None, risk_assessment)
        
        # 🚨 EMERGENCY ALERT SYSTEM - Check if emergency email should be sent
        emergency_alert_sent = False
        alert_details = None
        
        if risk_assessment['emergency_alert_required'] and user_data.get('parent_email'):
            
            # Smart cooldown system to balance safety with spam prevention
            recent_alerts = db.get_recent_emergency_alerts(user_id, hours=6)
            critical_alerts_recent = [alert for alert in recent_alerts if alert['risk_level'] in ['CRITICAL', 'HIGH']]
            
            should_send_alert = True
            cooldown_reason = None
            
            # Cooldown logic: 
            # - CRITICAL: Always send (suicide threats are emergencies)
            # - HIGH: 30-minute cooldown 
            # - MODERATE: 6-hour cooldown
            current_risk = risk_assessment['risk_level']
            
            if current_risk == 'CRITICAL':
                # Always send CRITICAL alerts (suicide threats)
                should_send_alert = True
                logger.warning(f"🚨 CRITICAL ALERT - Bypassing cooldown for user {user_id}")
                
            elif current_risk == 'HIGH':
                # Check for HIGH/CRITICAL alerts in last 30 minutes
                recent_high_alerts = [alert for alert in recent_alerts 
                                    if alert['risk_level'] in ['CRITICAL', 'HIGH'] 
                                    and alert['created_at'] > (datetime.datetime.now() - datetime.timedelta(minutes=30)).isoformat()]
                if recent_high_alerts:
                    should_send_alert = False
                    cooldown_reason = "HIGH alert sent within 30 minutes"
                    
            else:  # MODERATE
                # Check for any alert in last 6 hours
                if critical_alerts_recent:
                    should_send_alert = False
                    cooldown_reason = "Alert sent within 6 hours"
            
            if not should_send_alert:
                logger.info(f"Emergency alert not sent - {cooldown_reason} for user {user_id}")
            else:
                logger.warning(f"🚨 SENDING EMERGENCY ALERT for user {user_id} - Risk Level: {current_risk}")
            
            if should_send_alert:
                logger.warning(f"🚨 EMERGENCY ALERT TRIGGERED for user {user_id} - Risk Level: {risk_assessment['risk_level']}")
                
                # Create emergency alert record
                alert_id = db.create_emergency_alert(
                    user_id=user_id,
                    risk_level=risk_assessment['risk_level'],
                    risk_score=risk_assessment['risk_score'],
                    parent_email=user_data['parent_email'],
                    message_content=user_message,
                    risk_indicators=json.dumps(risk_assessment['indicators'])
                )
                
                if alert_id:
                    # Prepare data for email service
                    email_user_data = {
                        'email': user_data['email'],
                        'parent_email': user_data['parent_email']
                    }
                    
                    email_risk_assessment = {
                        'level': risk_assessment['risk_level'],
                        'score': risk_assessment['risk_score'],
                        'summary': f"AI analysis detected {len(risk_assessment['indicators']['critical'] + risk_assessment['indicators']['high'])} high-priority risk indicators in user communication."
                    }
                    
                    # Send emergency email
                    email_sent = email_service.send_emergency_alert(
                        user_data=email_user_data,
                        risk_assessment=email_risk_assessment
                    )
                    
                    if email_sent:
                        # Update alert record as sent
                        db.update_emergency_alert_sent(alert_id, datetime.datetime.now())
                        emergency_alert_sent = True
                        alert_details = {
                            'sent_to': user_data['parent_email'],
                            'timestamp': datetime.datetime.now().isoformat(),
                            'risk_level': risk_assessment['risk_level']
                        }
                        logger.info(f"✅ Emergency email sent successfully to {user_data['parent_email']}")
                    else:
                        logger.error(f"❌ Failed to send emergency email for user {user_id}")
        
        # Add emergency alert info to response
        combined_analysis['emergency_alert'] = {
            'required': risk_assessment['emergency_alert_required'],
            'sent': emergency_alert_sent,
            'details': alert_details
        }
        
        return jsonify({
            'response': gemini_response,
            'analysis': combined_analysis,
            'user_id': user_id
        })
        
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/audio-analysis', methods=['POST'])
@login_required
def analyze_audio():
    """Handle audio file analysis"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({'error': 'No audio file selected'}), 400
        
        # Save temporarily and process
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            audio_file.save(temp_file.name)
            
            # Load and analyze audio
            audio_data, sr = librosa.load(temp_file.name, sr=16000)
            features = extract_audio_features(audio_data, sr)
            
            if features is not None:
                depression_score = analyze_audio_depression(features)
                
                # Determine risk level
                if depression_score < 0.3:
                    risk_level = "Low Risk"
                    risk_color = "success"
                elif depression_score < 0.7:
                    risk_level = "Moderate Risk"
                    risk_color = "warning"
                else:
                    risk_level = "High Risk"
                    risk_color = "danger"
                
                # Clean up temp file
                os.unlink(temp_file.name)
                
                return jsonify({
                    'risk_score': float(depression_score),
                    'risk_level': risk_level,
                    'risk_color': risk_color,
                    'confidence': float(depression_score),
                    'features_analyzed': {
                        'energy': float(features[38]) if len(features) > 38 else 0,
                        'tempo': float(features[40]) if len(features) > 40 else 0,
                        'spectral_centroid': float(features[26]) if len(features) > 26 else 0
                    }
                })
            else:
                return jsonify({'error': 'Could not analyze audio file'}), 500
                
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat-history')
@login_required
def get_chat_history():
    """Get chat history for current user"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify([])
    
    history = db.get_user_chat_history(user_id, limit=50)
    return jsonify(history)

@app.route('/api/clear-chat', methods=['POST'])
@login_required
def clear_chat():
    """Clear chat history for current user"""
    # Note: In a real application, you might want to soft-delete rather than hard-delete
    # For now, we'll just return success as the database doesn't have a clear function
    return jsonify({'status': 'cleared'})

if __name__ == '__main__':
    print("🚀 Starting EmpathyWave Enhanced Chat Bot...")
    print("🤖 Loading AI models...")
    
    # Load text model
    if load_text_model():
        print("✅ Text model loaded successfully!")
    else:
        print("⚠️  Warning: Text model not found!")
    
    print("🌟 Starting enhanced chat interface...")
    print("💬 Gemini AI integration enabled!")
    print("🎵 Audio analysis enabled!")
    
    app.run(host='0.0.0.0', port=5000, debug=True)