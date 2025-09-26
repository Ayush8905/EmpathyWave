from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # Register blueprints
    from app.api.prediction_routes import prediction_bp
    from app.api.chatbot_routes import chatbot_bp
    from app.api.audio_routes import audio_bp
    
    app.register_blueprint(prediction_bp, url_prefix='/api/prediction')
    app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')
    app.register_blueprint(audio_bp, url_prefix='/api/audio')
    
    # Main route
    @app.route('/')
    def index():
        return app.send_static_file('index.html')
    
    return app
