#!/usr/bin/env python3
"""
Simple Flask app for depression detection
"""

from flask import Flask, render_template, request, jsonify
import joblib
import os

app = Flask(__name__, template_folder='app/templates')

# Load the trained model
model_data = None

def load_model():
    """Load the trained model"""
    global model_data
    model_path = 'data/models/text_model.pkl'
    if os.path.exists(model_path):
        model_data = joblib.load(model_path)
        return True
    return False

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/prediction/text', methods=['POST'])
def predict_text():
    """Predict depression risk from text"""
    try:
        if model_data is None:
            if not load_model():
                return jsonify({'error': 'Model not found'}), 500
        
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Get model components
        model = model_data['model']
        vectorizer = model_data['vectorizer']
        
        # Make prediction
        text_vec = vectorizer.transform([text])
        prediction = model.predict(text_vec)[0]
        probability = model.predict_proba(text_vec)[0]
        
        # Determine risk level
        risk_score = probability[1] if len(probability) > 1 else prediction
        if risk_score < 0.3:
            risk_level = "no_risk"
        elif risk_score < 0.7:
            risk_level = "at_risk"
        else:
            risk_level = "high_risk"
        
        return jsonify({
            'text': text,
            'prediction': int(prediction),
            'risk_score': float(risk_score),
            'risk_level': risk_level,
            'confidence': float(max(probability))
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/prediction/status', methods=['GET'])
def model_status():
    """Check model status"""
    if model_data is None:
        if not load_model():
            return jsonify({'status': 'not_loaded', 'error': 'Model not found'})
    
    return jsonify({
        'status': 'loaded',
        'accuracy': model_data.get('accuracy', 'N/A')
    })

@app.route('/api/test', methods=['GET'])
def test_api():
    """Test API endpoint"""
    return jsonify({
        'status': 'working',
        'message': 'Depression Detection API is running!'
    })

if __name__ == '__main__':
    print("Starting Depression Detection Flask App...")
    print("Loading model...")
    if load_model():
        print("Model loaded successfully!")
    else:
        print("Warning: Model not found!")
    
    print("Starting web server...")
    app.run(host='0.0.0.0', port=5000, debug=True)
