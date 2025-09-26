import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import os
from typing import Dict, List, Tuple, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TextDepressionModel:
    """Text-based depression detection model"""
    
    def __init__(self, model_type='random_forest'):
        self.model_type = model_type
        self.model = None
        self.vectorizer = None
        self.is_trained = False
        
    def _initialize_model(self):
        """Initialize the ML model based on type"""
        if self.model_type == 'random_forest':
            self.model = RandomForestClassifier(
                n_estimators=100,
                random_state=42,
                max_depth=10,
                min_samples_split=5
            )
        elif self.model_type == 'svm':
            self.model = SVC(
                kernel='rbf',
                random_state=42,
                probability=True
            )
        else:
            raise ValueError(f"Unsupported model type: {self.model_type}")
    
    def preprocess_text(self, texts: List[str]) -> np.ndarray:
        """Preprocess text data for training/prediction"""
        if self.vectorizer is None:
            self.vectorizer = TfidfVectorizer(
                max_features=5000,
                stop_words='english',
                ngram_range=(1, 2),
                min_df=2,
                max_df=0.95
            )
            return self.vectorizer.fit_transform(texts)
        else:
            return self.vectorizer.transform(texts)
    
    def train(self, X: List[str], y: List[int], test_size=0.2) -> Dict[str, Any]:
        """Train the text depression detection model"""
        logger.info(f"Training {self.model_type} model on {len(X)} samples")
        
        # Initialize model if not done
        if self.model is None:
            self._initialize_model()
        
        # Preprocess text data
        X_processed = self.preprocess_text(X)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_processed, y, test_size=test_size, random_state=42, stratify=y
        )
        
        # Train model
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Cross-validation
        cv_scores = cross_val_score(self.model, X_processed, y, cv=5)
        
        # Get feature importance (for Random Forest)
        feature_importance = None
        if hasattr(self.model, 'feature_importances_'):
            feature_names = self.vectorizer.get_feature_names_out()
            feature_importance = dict(zip(feature_names, self.model.feature_importances_))
            # Sort by importance
            feature_importance = dict(sorted(feature_importance.items(), 
                                           key=lambda x: x[1], reverse=True)[:20])
        
        self.is_trained = True
        
        results = {
            'accuracy': accuracy,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'classification_report': classification_report(y_test, y_pred),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
            'feature_importance': feature_importance
        }
        
        logger.info(f"Model training completed. Accuracy: {accuracy:.4f}")
        return results
    
    def predict(self, texts: List[str]) -> Dict[str, Any]:
        """Predict depression risk from text"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        # Preprocess text
        X_processed = self.preprocess_text(texts)
        
        # Get predictions and probabilities
        predictions = self.model.predict(X_processed)
        probabilities = self.model.predict_proba(X_processed)
        
        results = []
        for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
            risk_score = prob[1] if len(prob) > 1 else pred  # Probability of depression
            
            # Determine risk level
            if risk_score < 0.3:
                risk_level = "no_risk"
            elif risk_score < 0.7:
                risk_level = "at_risk"
            else:
                risk_level = "high_risk"
            
            results.append({
                'text': texts[i],
                'prediction': int(pred),
                'risk_score': float(risk_score),
                'risk_level': risk_level,
                'confidence': float(max(prob))
            })
        
        return {'predictions': results}
    
    def save_model(self, filepath: str):
        """Save the trained model and vectorizer"""
        if not self.is_trained:
            raise ValueError("Model must be trained before saving")
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        model_data = {
            'model': self.model,
            'vectorizer': self.vectorizer,
            'model_type': self.model_type,
            'is_trained': self.is_trained
        }
        
        joblib.dump(model_data, filepath)
        logger.info(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str):
        """Load a pre-trained model and vectorizer"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found: {filepath}")
        
        model_data = joblib.load(filepath)
        self.model = model_data['model']
        self.vectorizer = model_data['vectorizer']
        self.model_type = model_data['model_type']
        self.is_trained = model_data['is_trained']
        
        logger.info(f"Model loaded from {filepath}")
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        return {
            'model_type': self.model_type,
            'is_trained': self.is_trained,
            'has_vectorizer': self.vectorizer is not None,
            'model_params': self.model.get_params() if self.model else None
        }
