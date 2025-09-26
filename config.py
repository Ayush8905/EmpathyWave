import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///depression_detection.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Google Gemini API
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    
    # Emergency Email Configuration
    SENDER_EMAIL = os.environ.get('SENDER_EMAIL', 'empathywave.support@gmail.com')
    SENDER_PASSWORD = os.environ.get('SENDER_PASSWORD', '')
    
    # Model paths
    TEXT_MODEL_PATH = 'data/models/text_model.pkl'
    AUDIO_MODEL_PATH = 'data/models/audio_model.pkl'
    
    # Data paths
    RAW_DATA_PATH = 'data/raw/'
    PROCESSED_DATA_PATH = 'data/processed/'
    
    # Audio settings
    AUDIO_SAMPLE_RATE = 16000
    AUDIO_DURATION = 30  # seconds
    AUDIO_CHUNK_SIZE = 1024
    
    # Text processing
    MAX_TEXT_LENGTH = 512
    MIN_TEXT_LENGTH = 10
    
    # Privacy settings
    DATA_RETENTION_DAYS = 30
    ANONYMIZE_DATA = True
    
    # Risk levels
    RISK_LEVELS = {
        'no_risk': (0.0, 0.3),
        'at_risk': (0.3, 0.7),
        'high_risk': (0.7, 1.0)
    }

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
