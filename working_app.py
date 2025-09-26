from flask import Flask, request, jsonify, render_template_string
import joblib
import os
import librosa
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

app = Flask(__name__)

# Load text model
text_model_data = None
audio_model_data = None

def load_text_model():
    global text_model_data
    if os.path.exists('data/models/text_model.pkl'):
        text_model_data = joblib.load('data/models/text_model.pkl')
        return True
    return False

def extract_audio_features(audio_data, sr=16000):
    """Extract comprehensive audio features for depression detection"""
    features = []
    
    # MFCC features (13 coefficients)
    mfccs = librosa.feature.mfcc(y=audio_data, sr=sr, n_mfcc=13)
    features.extend(np.mean(mfccs, axis=1))
    features.extend(np.std(mfccs, axis=1))
    
    # Spectral features
    spectral_centroids = librosa.feature.spectral_centroid(y=audio_data, sr=sr)
    features.append(np.mean(spectral_centroids))
    features.append(np.std(spectral_centroids))
    
    spectral_rolloff = librosa.feature.spectral_rolloff(y=audio_data, sr=sr)
    features.append(np.mean(spectral_rolloff))
    features.append(np.std(spectral_rolloff))
    
    # Zero crossing rate
    zcr = librosa.feature.zero_crossing_rate(audio_data)
    features.append(np.mean(zcr))
    features.append(np.std(zcr))
    
    # Chroma features
    chroma = librosa.feature.chroma_stft(y=audio_data, sr=sr)
    features.extend(np.mean(chroma, axis=1))
    features.extend(np.std(chroma, axis=1))
    
    # RMS energy
    rms = librosa.feature.rms(y=audio_data)
    features.append(np.mean(rms))
    features.append(np.std(rms))
    
    # Tempo
    tempo, _ = librosa.beat.beat_track(y=audio_data, sr=sr)
    features.append(tempo)
    
    return np.array(features)

def analyze_audio_features(features):
    """Analyze audio features for depression indicators"""
    # Extract key features
    mfcc_mean = np.mean(features[:13])  # First 13 are MFCC means
    spectral_centroid_mean = features[26]  # Spectral centroid mean
    zcr_mean = features[30]  # Zero crossing rate mean
    rms_mean = features[38]  # RMS energy mean
    tempo = features[40]  # Tempo
    
    # Depression indicators based on research:
    # - Lower pitch (higher MFCC values)
    # - Reduced energy (lower RMS)
    # - Slower speech (lower tempo)
    # - More monotone (lower spectral centroid variation)
    
    depression_score = 0.0
    
    # MFCC analysis (pitch-related)
    if mfcc_mean > -5:
        depression_score += 0.3
    elif mfcc_mean > -3:
        depression_score += 0.2
    
    # Energy analysis
    if rms_mean < 0.01:
        depression_score += 0.3
    elif rms_mean < 0.02:
        depression_score += 0.2
    
    # Tempo analysis (speech rate)
    if tempo < 80:
        depression_score += 0.2
    elif tempo < 100:
        depression_score += 0.1
    
    # Spectral centroid (voice brightness)
    if spectral_centroid_mean < 1000:
        depression_score += 0.2
    
    # Normalize score
    depression_score = min(depression_score, 1.0)
    
    return depression_score

# HTML template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Depression Detection System</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        textarea { width: 100%; height: 120px; padding: 15px; border: 2px solid #ddd; border-radius: 5px; }
        button { background-color: #007bff; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; margin: 10px 5px; }
        .result { margin-top: 20px; padding: 15px; border-radius: 5px; }
        .no-risk { background-color: #d4edda; border: 1px solid #c3e6cb; color: #155724; }
        .at-risk { background-color: #fff3cd; border: 1px solid #ffeaa7; color: #856404; }
        .high-risk { background-color: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Depression Detection System</h1>
        
        <h3>Text Analysis</h3>
        <textarea id="textInput" placeholder="Enter your text here..."></textarea>
        <button onclick="analyzeText()">Analyze Text</button>
        
        <h3>Audio Analysis</h3>
        <input type="file" id="audioInput" accept="audio/*">
        <button onclick="analyzeAudio()">Analyze Audio</button>
        
        <div id="result"></div>
        
        <div style="margin-top: 30px; padding: 20px; background-color: #e9ecef; border-radius: 5px;">
            <h3>Mental Health Resources</h3>
            <p><strong>Important:</strong> This tool is for informational purposes only.</p>
            <ul>
                <li>National Suicide Prevention Lifeline: 988</li>
                <li>Crisis Text Line: Text HOME to 741741</li>
                <li>SAMHSA National Helpline: 1-800-662-4357</li>
            </ul>
        </div>
    </div>

    <script>
        async function analyzeText() {
            const text = document.getElementById('textInput').value.trim();
            if (!text) { alert('Please enter some text'); return; }
            
            document.getElementById('result').innerHTML = 'Analyzing...';
            
            try {
                const response = await fetch('/api/text', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({text: text})
                });
                const data = await response.json();
                displayResult(data, 'Text Analysis');
            } catch (error) {
                document.getElementById('result').innerHTML = 'Error: ' + error.message;
            }
        }
        
        async function analyzeAudio() {
            const fileInput = document.getElementById('audioInput');
            const file = fileInput.files[0];
            if (!file) { alert('Please select an audio file'); return; }
            
            document.getElementById('result').innerHTML = 'Analyzing audio...';
            
            const formData = new FormData();
            formData.append('audio', file);
            
            try {
                const response = await fetch('/api/audio', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                displayResult(data, 'Audio Analysis');
            } catch (error) {
                document.getElementById('result').innerHTML = 'Error: ' + error.message;
            }
        }
        
        function displayResult(data, type) {
            const resultDiv = document.getElementById('result');
            let riskClass = 'no-risk';
            let riskText = 'No Risk';
            
            if (data.risk_level === 'at_risk') {
                riskClass = 'at-risk';
                riskText = 'At Risk';
            } else if (data.risk_level === 'high_risk') {
                riskClass = 'high-risk';
                riskText = 'High Risk';
            }
            
            resultDiv.className = 'result ' + riskClass;
            resultDiv.innerHTML = `
                <h4>${type} Result</h4>
                <p><strong>Risk Level:</strong> ${riskText}</p>
                <p><strong>Confidence:</strong> ${(data.confidence * 100).toFixed(1)}%</p>
                <p><strong>Risk Score:</strong> ${(data.risk_score * 100).toFixed(1)}%</p>
            `;
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/text', methods=['POST'])
def analyze_text():
    try:
        if not text_model_data:
            if not load_text_model():
                return jsonify({'error': 'Text model not found'}), 500
        
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        model = text_model_data['model']
        vectorizer = text_model_data['vectorizer']
        
        text_vec = vectorizer.transform([text])
        prediction = model.predict(text_vec)[0]
        probability = model.predict_proba(text_vec)[0]
        
        risk_score = probability[1] if len(probability) > 1 else prediction
        if risk_score < 0.3:
            risk_level = "no_risk"
        elif risk_score < 0.7:
            risk_level = "at_risk"
        else:
            risk_level = "high_risk"
        
        return jsonify({
            'prediction': int(prediction),
            'risk_score': float(risk_score),
            'risk_level': risk_level,
            'confidence': float(max(probability))
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/audio', methods=['POST'])
def analyze_audio():
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({'error': 'No audio file selected'}), 400
        
        # Load audio file
        audio_data, sr = librosa.load(audio_file, sr=16000)
        
        # Extract comprehensive features
        features = extract_audio_features(audio_data, sr)
        
        # Analyze features for depression indicators
        depression_score = analyze_audio_features(features)
        
        # Determine risk level
        if depression_score < 0.3:
            risk_level = "no_risk"
        elif depression_score < 0.7:
            risk_level = "at_risk"
        else:
            risk_level = "high_risk"
        
        return jsonify({
            'prediction': 1 if depression_score > 0.5 else 0,
            'risk_score': float(depression_score),
            'risk_level': risk_level,
            'confidence': float(depression_score),
            'features_analyzed': {
                'mfcc_mean': float(np.mean(features[:13])),
                'spectral_centroid': float(features[26]),
                'energy': float(features[38]),
                'tempo': float(features[40])
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({
        'text_model': 'loaded' if text_model_data else 'not_loaded',
        'audio_model': 'enabled',
        'audio_features': 'comprehensive',
        'status': 'running',
        'capabilities': {
            'text_analysis': True,
            'audio_analysis': True,
            'feature_extraction': ['MFCC', 'Spectral', 'Chroma', 'Tempo', 'Energy'],
            'risk_levels': ['no_risk', 'at_risk', 'high_risk']
        }
    })

if __name__ == '__main__':
    print("Starting Depression Detection System...")
    print("Loading text model...")
    if load_text_model():
        print("Text model loaded successfully!")
    else:
        print("Warning: Text model not found!")
    
    print("Starting web server...")
    app.run(host='0.0.0.0', port=5000, debug=True)
