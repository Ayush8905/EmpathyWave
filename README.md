# Depression Detection Chatbot System

A privacy-aware Flask-based web application that uses machine learning models to assess depression risk through text and audio analysis, integrated with Google Gemini API for conversational support.

## Features

- **Dual Model Approach**: Text-based and audio-based depression risk assessment
- **Privacy-First**: Secure data handling with user consent management
- **Real-time Chat**: Integrated chatbot powered by Google Gemini API
- **Non-Diagnostic**: Provides risk assessment and mental health resources only
- **Modular Architecture**: Scalable and maintainable codebase

## Project Structure

```
depression-detection-system/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── text_model.py
│   │   ├── audio_model.py
│   │   └── model_utils.py
│   ├── preprocessing/
│   │   ├── text_preprocessor.py
│   │   ├── audio_preprocessor.py
│   │   └── feature_extractor.py
│   ├── api/
│   │   ├── prediction_routes.py
│   │   ├── chatbot_routes.py
│   │   └── audio_routes.py
│   ├── auth/
│   │   ├── consent_manager.py
│   │   └── privacy_manager.py
│   └── templates/
│       ├── index.html
│       ├── chat.html
│       └── consent.html
├── data/
│   ├── raw/
│   ├── processed/
│   └── models/
├── notebooks/
│   ├── data_exploration.ipynb
│   ├── text_model_training.ipynb
│   └── audio_model_training.ipynb
├── tests/
├── config.py
├── requirements.txt
└── run.py
```

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Download spaCy model: `python -m spacy download en_core_web_sm`
4. Set up environment variables in `.env` file
5. Run the application: `python run.py`

## Usage

1. Navigate to the web interface
2. Complete consent form
3. Choose interaction mode (text or voice)
4. Interact with the chatbot
5. Receive depression risk assessment
6. Access mental health resources

## Ethical Considerations

- Non-diagnostic results only
- User consent required for data processing
- Secure data storage with anonymization
- Clear privacy policy and opt-out options
- Mental health resource links provided

## License

This project is for educational and research purposes only.
