# EmpathyWave - Depression Detection System

A comprehensive AI-powered depression detection system that analyzes both text and voice patterns to assess mental health risk levels.

## 🌟 Features

### 📝 Text Analysis
- **Trained ML Model**: Random Forest classifier trained on 75,000 samples
- **Real-time Analysis**: Instant depression risk assessment from text input
- **High Accuracy**: Well-balanced dataset with proven performance
- **Risk Classification**: Three-tier system (No Risk, At Risk, High Risk)

### 🎵 Voice Analysis
- **Comprehensive Audio Features**: MFCC, Spectral, Chroma, Tempo, Energy analysis
- **Depression Indicators**: Analyzes pitch, energy, speech rate, and voice brightness
- **Multi-format Support**: WAV, MP3, M4A audio files
- **Research-based**: Uses established audio biomarkers for depression detection

### 🌐 Web Interface
- **User-friendly Design**: Clean, professional interface
- **Dual Input Methods**: Both text and audio analysis options
- **Real-time Results**: Instant feedback with confidence scores
- **Mental Health Resources**: Integrated support links and helplines

## 🚀 Quick Start

### Prerequisites
```bash
pip install -r requirements.txt
```

### Running the Application
```bash
python working_app.py
```

Visit `http://localhost:5000` to access the web interface.

## 📊 System Architecture

### Text Model
- **Algorithm**: Random Forest with TF-IDF vectorization
- **Features**: 1000 text features with n-grams
- **Dataset**: 75,000 samples (38,027 non-depression, 36,973 depression)
- **Performance**: High accuracy on depression detection

### Audio Model
- **Feature Extraction**: 41 comprehensive audio features
- **Analysis Method**: Research-based depression indicators
- **Supported Formats**: WAV, MP3, M4A
- **Processing**: Real-time audio analysis

## 🔧 API Endpoints

### Text Analysis
```bash
POST /api/text
Content-Type: application/json
{
  "text": "I feel really sad and hopeless today"
}
```

### Audio Analysis
```bash
POST /api/audio
Content-Type: multipart/form-data
audio: [audio file]
```

### System Status
```bash
GET /api/status
```

## 📁 Project Structure

```
EmpathyWave/
├── app/                          # Main application modules
│   ├── models/                   # ML model implementations
│   │   ├── text_model.py        # Text-based depression detection
│   │   └── audio_model.py       # Audio-based depression detection
│   ├── preprocessing/            # Data preprocessing pipelines
│   │   └── data_loader.py       # Dataset loading and preparation
│   ├── api/                     # Flask API routes
│   │   ├── prediction_routes.py # Prediction endpoints
│   │   ├── chatbot_routes.py    # Chatbot integration
│   │   └── audio_routes.py      # Audio processing endpoints
│   └── templates/               # Web interface templates
│       └── index.html           # Main web interface
├── data/                        # Data and model storage
│   ├── models/                  # Trained model files
│   │   ├── text_model.pkl      # Text model
│   │   └── audio_model.pkl     # Audio model
│   ├── raw/                     # Raw dataset files
│   └── processed/              # Processed data files
├── notebooks/                   # Jupyter notebooks
│   └── data_exploration.ipynb  # Dataset analysis
├── working_app.py              # Main Flask application
├── train_models.py             # Model training script
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🧠 Technical Details

### Text Analysis Features
- **TF-IDF Vectorization**: Term frequency-inverse document frequency
- **N-gram Analysis**: Unigrams and bigrams for context
- **Stop Word Removal**: English stop words filtered
- **Feature Selection**: Top 1000 most informative features

### Audio Analysis Features
- **MFCC Coefficients**: 13 Mel-frequency cepstral coefficients
- **Spectral Features**: Centroid, rolloff, bandwidth
- **Chroma Features**: 12 pitch class profiles
- **Rhythm Features**: Tempo and beat tracking
- **Energy Features**: RMS energy analysis

### Depression Indicators
- **Lower Pitch**: Higher MFCC values indicate depressed speech
- **Reduced Energy**: Lower RMS energy in depressed individuals
- **Slower Speech**: Reduced tempo in depression
- **Monotone Voice**: Lower spectral centroid variation

## 🔒 Privacy & Ethics

- **Non-diagnostic**: Results are for informational purposes only
- **Privacy-focused**: Secure data handling and processing
- **Consent-based**: User consent required for data processing
- **Resource Links**: Mental health support resources provided
- **Professional Disclaimer**: Clear guidance to seek professional help

## 📈 Performance Metrics

### Text Model
- **Dataset Size**: 75,000 samples
- **Balance**: 50.7% non-depression, 49.3% depression
- **Features**: 1000 TF-IDF features
- **Algorithm**: Random Forest (100 estimators)

### Audio Model
- **Features**: 41 comprehensive audio features
- **Analysis**: Research-based depression indicators
- **Processing**: Real-time audio analysis
- **Support**: Multiple audio formats

## 🛠️ Development

### Training New Models
```bash
# Train text model
python train_models.py --dataset augmented_dataset_75000.csv --train-text-only

# Train audio model
python train_models.py --dataset augmented_dataset_75000.csv --train-audio-only
```

### Testing
```bash
# Test text model
python test_depression_model.py

# Test API endpoints
python -c "import requests; print(requests.get('http://localhost:5000/api/status').json())"
```

## 📞 Mental Health Resources

- **National Suicide Prevention Lifeline**: 988
- **Crisis Text Line**: Text HOME to 741741
- **SAMHSA National Helpline**: 1-800-662-4357
- **National Institute of Mental Health**: https://www.nimh.nih.gov/

## ⚠️ Important Disclaimer

This tool is for informational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of qualified health providers with questions about mental health conditions.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Dataset: Multimodal Depression Analysis Dataset
- Audio Processing: Librosa library
- ML Framework: Scikit-learn
- Web Framework: Flask
- Research: Depression detection in speech patterns

---

**EmpathyWave** - Empowering mental health awareness through AI technology.