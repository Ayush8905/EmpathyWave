from flask import Blueprint, request, jsonify
import requests
import os
from config import Config

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    """Handle chatbot conversation"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # For now, return a simple response
        # In the future, this will integrate with Google Gemini API
        response = {
            'message': message,
            'response': 'I understand you\'re reaching out. How can I help you today?',
            'timestamp': '2024-01-01T00:00:00Z'
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chatbot_bp.route('/status', methods=['GET'])
def chatbot_status():
    """Check chatbot status"""
    return jsonify({
        'status': 'ready',
        'api_key_configured': bool(Config.GEMINI_API_KEY)
    })
