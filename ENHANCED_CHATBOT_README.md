# 🚀 EmpathyWave Enhanced Chat Bot

## Overview
EmpathyWave is an advanced AI-powered mental health chat bot that combines Google Gemini AI with trained machine learning models to provide personalized mental health support and depression risk assessment.

## ✨ Key Features

### 🤖 AI-Powered Conversations
- **Gemini AI Integration**: Natural, empathetic conversations using Google's Gemini Pro model
- **Context-Aware Responses**: Maintains conversation context for more meaningful interactions
- **Supportive Communication**: Trained to provide mental health support without medical diagnosis

### 🧠 Real-Time Mental Health Analysis
- **ML Model Integration**: Uses your trained depression detection model for risk assessment
- **Combined Analysis**: Merges Gemini AI insights with ML model predictions
- **Risk Level Assessment**: Categorizes users into Low, Moderate, or High risk levels
- **Confidence Scoring**: Provides confidence levels for all predictions

### 🎵 Audio Analysis Capabilities
- **Voice Recording**: Real-time audio recording through the browser
- **Audio File Upload**: Support for various audio formats
- **Acoustic Feature Analysis**: Extracts MFCC, spectral, and temporal features
- **Voice Pattern Detection**: Identifies depression indicators in speech patterns

### 🎨 Enhanced User Interface
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Smooth Animations**: Engaging transitions and effects throughout the interface
- **Real-Time Analysis Panel**: Live updates showing risk assessments and insights
- **Quick Actions**: Pre-defined messages for easy interaction
- **Professional Theme**: Modern gradient design with intuitive controls

## 🔧 Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Microphone access (for audio features)
- Internet connection (for Gemini AI)

### Installation

#### Windows
1. Run the setup script:
   ```cmd
   start_enhanced_chat.bat
   ```

#### Linux/Mac
1. Make the script executable:
   ```bash
   chmod +x start_enhanced_chat.sh
   ```
2. Run the setup script:
   ```bash
   ./start_enhanced_chat.sh
   ```

#### Manual Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python enhanced_chat_app.py
   ```

### Configuration
The application uses the following configuration:
- **Gemini API Key**: `AIzaSyDj7wyPs73Nxmrnqo0H1PyLx_iUwC-XwQk` (embedded in code)
- **Port**: 5000 (default)
- **Host**: 0.0.0.0 (accessible from all network interfaces)

## 🎯 How to Use

### Starting a Conversation
1. Open your browser to `http://localhost:5000`
2. Type your message in the input field
3. Click the send button or press Enter
4. View real-time analysis in the sidebar

### Quick Actions
Use the pre-defined quick action buttons for common interactions:
- "How are you?"
- "I feel stressed"
- "Need to talk"
- "Feeling anxious"

### Audio Features
1. **Voice Recording**:
   - Click the microphone button in the header or input area
   - Allow microphone access when prompted
   - Speak naturally for 5-30 seconds
   - Click "Stop Recording" when finished

2. **Audio File Upload**:
   - Click the upload button in the input area
   - Select an audio file (WAV, MP3, etc.)
   - Wait for analysis results

### Analysis Panel
The right sidebar shows:
- **Real-time Risk Assessment**: Updated after each message
- **Risk Score Progress Bars**: Visual representation of risk levels
- **AI Analysis**: Gemini's psychological insights
- **Audio Analysis**: Voice pattern analysis results

## 🔍 Technical Details

### Architecture
- **Backend**: Flask web framework
- **AI Integration**: Google Gemini Pro API
- **ML Models**: Scikit-learn for depression detection
- **Audio Processing**: Librosa for feature extraction
- **Frontend**: Bootstrap 5 with custom CSS animations

### Machine Learning Pipeline
1. **Text Analysis**:
   - TF-IDF vectorization of user messages
   - Trained classification model predicts depression risk
   - Probability scores converted to risk levels

2. **Audio Analysis**:
   - Extracts 40+ acoustic features (MFCC, spectral, temporal)
   - Analyzes voice patterns associated with depression
   - Combines multiple indicators for risk assessment

3. **Combined Analysis**:
   - Merges ML model predictions with Gemini insights
   - Provides comprehensive risk assessment
   - Maintains conversation context for better accuracy

### API Endpoints
- `GET /`: Main chat interface
- `POST /api/chat`: Send message and get AI response
- `POST /api/audio-analysis`: Analyze audio files
- `GET /api/chat-history`: Retrieve conversation history
- `POST /api/clear-chat`: Clear conversation history

## 🛡️ Privacy & Safety

### Data Handling
- **Session-Based**: Chat history stored temporarily in memory
- **No Permanent Storage**: Messages not saved to disk
- **Privacy Focused**: Audio files processed and deleted immediately

### Safety Features
- **Crisis Resources**: Always visible support hotlines
- **Professional Disclaimer**: Clear indication this is not medical diagnosis
- **Supportive Responses**: Encourages seeking professional help when needed

### Support Resources
- **National Suicide Prevention**: 988
- **Crisis Text Line**: Text HOME to 741741
- **SAMHSA Helpline**: 1-800-662-4357

## 🚨 Important Disclaimers

⚠️ **This application is for informational and supportive purposes only**
- Not a substitute for professional medical advice
- Does not provide medical diagnosis or treatment
- Users experiencing crisis should contact emergency services
- Encourages seeking help from qualified mental health professionals

## 🛠️ Customization

### Modifying the UI
- Edit `templates/chat_interface.html` for layout changes
- Modify CSS variables in the `<style>` section for theme customization
- Add new animations by extending the CSS keyframes

### Updating AI Behavior
- Modify prompts in `enhanced_chat_app.py` functions:
  - `analyze_text_with_gemini()`: Analysis prompts
  - `get_gemini_response()`: Conversation prompts

### Model Integration
- Replace `data/models/text_model.pkl` with your trained model
- Ensure the model has the same interface (predict, predict_proba methods)
- Update feature extraction if using different text processing

## 🔧 Troubleshooting

### Common Issues
1. **Gemini API Errors**: Check internet connection and API key validity
2. **Audio Not Working**: Ensure microphone permissions are granted
3. **Model Loading Errors**: Verify `text_model.pkl` exists in `data/models/`
4. **Port Already in Use**: Change port in `enhanced_chat_app.py` (line with `app.run()`)

### Performance Optimization
- For production: Use WSGI server like Gunicorn
- For better security: Use environment variables for API keys
- For scaling: Implement database storage for persistent sessions

## 📝 License & Credits

This enhanced chat bot builds upon your existing depression detection system and integrates:
- Google Gemini AI for natural language processing
- Advanced UI/UX design principles
- Comprehensive audio analysis capabilities
- Real-time mental health assessment features

---

**🌟 Start supporting mental health with AI-powered empathy today!**