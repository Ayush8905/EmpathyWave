#!/usr/bin/env python3
"""
Training script for depression detection models
Supports both text and audio models using the augmented_dataset_75000.csv
"""

import os
import sys
import pandas as pd
import numpy as np
import argparse
import logging
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent / 'app'))

from preprocessing.data_loader import DepressionDatasetLoader
from models.text_model import TextDepressionModel
from models.audio_model import AudioDepressionModel
from config import Config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('training.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def create_directories():
    """Create necessary directories"""
    directories = [
        'data/raw',
        'data/processed',
        'data/models',
        'logs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"Created directory: {directory}")

def train_text_model(dataset_path: str, text_column: str, label_column: str, 
                    model_type: str = 'random_forest'):
    """Train text-based depression detection model"""
    logger.info("Starting text model training...")
    
    # Load and prepare data
    loader = DepressionDatasetLoader(dataset_path)
    texts, labels = loader.prepare_text_data(text_column, label_column)
    
    # Initialize and train model
    text_model = TextDepressionModel(model_type=model_type)
    
    # Split data
    splits = loader.split_data(texts, labels, test_size=0.2, val_size=0.1)
    
    # Train on training data
    train_texts = splits['train']['texts']
    train_labels = splits['train']['labels']
    
    results = text_model.train(train_texts, train_labels)
    
    # Save model
    model_path = Config.TEXT_MODEL_PATH
    text_model.save_model(model_path)
    
    logger.info("Text model training completed!")
    logger.info(f"Accuracy: {results['accuracy']:.4f}")
    logger.info(f"Cross-validation mean: {results['cv_mean']:.4f} ± {results['cv_std']:.4f}")
    
    return text_model, results

def train_audio_model(dataset_path: str, audio_column: str, label_column: str,
                     audio_dir: str = None, model_type: str = 'random_forest',
                     use_deep_learning: bool = False):
    """Train audio-based depression detection model"""
    logger.info("Starting audio model training...")
    
    # Load and prepare data
    loader = DepressionDatasetLoader(dataset_path)
    audio_files, labels = loader.prepare_audio_data(audio_column, label_column, audio_dir)
    
    # Initialize audio model
    audio_model = AudioDepressionModel(model_type=model_type, use_deep_learning=use_deep_learning)
    
    # Extract features from audio files
    logger.info("Extracting audio features...")
    features = []
    valid_labels = []
    
    for i, (audio_file, label) in enumerate(zip(audio_files, labels)):
        try:
            import librosa
            # Load audio file
            audio_data, sr = librosa.load(audio_file, sr=16000)
            
            # Extract features
            feature_vector = audio_model.extract_audio_features(audio_data, sr)
            features.append(feature_vector)
            valid_labels.append(label)
            
            if (i + 1) % 100 == 0:
                logger.info(f"Processed {i + 1}/{len(audio_files)} audio files")
                
        except Exception as e:
            logger.warning(f"Failed to process {audio_file}: {str(e)}")
            continue
    
    features = np.array(features)
    logger.info(f"Extracted features from {len(features)} audio files")
    
    # Split data
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(
        features, valid_labels, test_size=0.2, random_state=42, stratify=valid_labels
    )
    
    # Train model
    results = audio_model.train(features, valid_labels)
    
    # Save model
    model_path = Config.AUDIO_MODEL_PATH
    audio_model.save_model(model_path)
    
    logger.info("Audio model training completed!")
    logger.info(f"Accuracy: {results['accuracy']:.4f}")
    
    return audio_model, results

def main():
    parser = argparse.ArgumentParser(description='Train depression detection models')
    parser.add_argument('--dataset', type=str, required=True, 
                       help='Path to the dataset CSV file')
    parser.add_argument('--text-column', type=str, default='text',
                       help='Name of the text column')
    parser.add_argument('--label-column', type=str, default='label',
                       help='Name of the label column')
    parser.add_argument('--audio-column', type=str, default='audio_file',
                       help='Name of the audio file column')
    parser.add_argument('--audio-dir', type=str, default=None,
                       help='Directory containing audio files')
    parser.add_argument('--text-model', type=str, default='random_forest',
                       choices=['random_forest', 'svm'],
                       help='Text model type')
    parser.add_argument('--audio-model', type=str, default='random_forest',
                       choices=['random_forest', 'svm'],
                       help='Audio model type')
    parser.add_argument('--use-deep-learning', action='store_true',
                       help='Use deep learning for audio model')
    parser.add_argument('--train-text-only', action='store_true',
                       help='Train only text model')
    parser.add_argument('--train-audio-only', action='store_true',
                       help='Train only audio model')
    
    args = parser.parse_args()
    
    # Create directories
    create_directories()
    
    # Explore dataset first
    logger.info("Exploring dataset...")
    loader = DepressionDatasetLoader(args.dataset)
    exploration = loader.explore_dataset()
    
    logger.info(f"Dataset shape: {exploration['shape']}")
    logger.info(f"Columns: {exploration['columns']}")
    
    if 'missing_values' in exploration:
        missing = exploration['missing_values']
        logger.info(f"Missing values: {missing}")
    
    # Train text model
    if not args.train_audio_only:
        try:
            text_model, text_results = train_text_model(
                args.dataset, 
                args.text_column, 
                args.label_column,
                args.text_model
            )
        except Exception as e:
            logger.error(f"Text model training failed: {str(e)}")
            if args.train_text_only:
                return
    
    # Train audio model
    if not args.train_text_only:
        try:
            audio_model, audio_results = train_audio_model(
                args.dataset,
                args.audio_column,
                args.label_column,
                args.audio_dir,
                args.audio_model,
                args.use_deep_learning
            )
        except Exception as e:
            logger.error(f"Audio model training failed: {str(e)}")
            if args.train_audio_only:
                return
    
    logger.info("All model training completed successfully!")

if __name__ == '__main__':
    main()
