@echo off
echo ===============================================
echo    🚀 EmpathyWave Enhanced Chat Bot Setup    
echo ===============================================
echo.

echo 📦 Installing required dependencies...
pip install -r requirements.txt

echo.
echo 🔧 Setting up environment...
if not exist "data\models" (
    mkdir "data\models"
    echo Created models directory
)

if not exist "logs" (
    mkdir "logs"
    echo Created logs directory
)

echo.
echo 🤖 Starting EmpathyWave Enhanced Chat Bot...
echo.
echo Features enabled:
echo ✅ Gemini AI Integration
echo ✅ Real-time Depression Analysis
echo ✅ Audio Processing
echo ✅ Animated UI
echo ✅ Responsive Design
echo.
echo 🌐 Access the app at: http://localhost:5000
echo.

python enhanced_chat_app.py

pause