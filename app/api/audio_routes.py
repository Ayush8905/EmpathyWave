from flask import Blueprint, request, jsonify
import os
from config import Config

audio_bp = Blueprint('audio', __name__)

@audio_bp.route('/upload', methods=['POST'])
def upload_audio():
    """Handle audio file upload for depression analysis"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        
        if audio_file.filename == '':
            return jsonify({'error': 'No audio file selected'}), 400
        
        # For now, return a placeholder response
        # In the future, this will process the audio file
        response = {
            'filename': audio_file.filename,
            'status': 'uploaded',
            'message': 'Audio file received. Processing will be implemented soon.'
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@audio_bp.route('/status', methods=['GET'])
def audio_status():
    """Check audio processing status"""
    return jsonify({
        'status': 'ready',
        'supported_formats': ['wav', 'mp3', 'm4a'],
        'max_duration': Config.AUDIO_DURATION
    })
