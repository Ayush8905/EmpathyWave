#!/bin/bash

echo "==============================================="
echo "    🚀 EmpathyWave Enhanced Chat Bot Setup    "
echo "==============================================="
echo

echo "📦 Installing required dependencies..."
pip install -r requirements.txt

echo
echo "🔧 Setting up environment..."
mkdir -p data/models
mkdir -p logs
echo "Created necessary directories"

echo
echo "🤖 Starting EmpathyWave Enhanced Chat Bot..."
echo
echo "Features enabled:"
echo "✅ Gemini AI Integration"
echo "✅ Real-time Depression Analysis"
echo "✅ Audio Processing"
echo "✅ Animated UI"
echo "✅ Responsive Design"
echo
echo "🌐 Access the app at: http://localhost:5000"
echo

python enhanced_chat_app.py