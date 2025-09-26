import pandas as pd
import numpy as np
import librosa
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import StandardScaler
import joblib
import os
from typing import Dict, List, Tuple, Any, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AudioDataset(Dataset):
    """Custom dataset for audio data"""
    
    def __init__(self, features, labels):
        self.features = torch.FloatTensor(features)
        self.labels = torch.LongTensor(labels)
    
    def __len__(self):
        return len(self.features)
    
    def __getitem__(self, idx):
        return self.features[idx], self.labels[idx]

class AudioCNN(nn.Module):
    """CNN model for audio depression detection"""
    
    def __init__(self, input_size=40, num_classes=2):
        super(AudioCNN, self).__init__()
        
        self.conv1 = nn.Conv1d(1, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv1d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv1d(64, 128, kernel_size=3, padding=1)
        
        self.pool = nn.MaxPool1d(2)
        self.dropout = nn.Dropout(0.5)
        
        # Calculate the size after convolutions
        self.fc_input_size = self._get_conv_output_size(input_size)
        
        self.fc1 = nn.Linear(self.fc_input_size, 256)
        self.fc2 = nn.Linear(256, 64)
        self.fc3 = nn.Linear(64, num_classes)
        
        self.relu = nn.ReLU()
        self.softmax = nn.Softmax(dim=1)
    
    def _get_conv_output_size(self, input_size):
        """Calculate the output size after convolutions"""
        size = input_size
        size = size // 2  # After first pool
        size = size // 2  # After second pool
        size = size // 2  # After third pool
        return 128 * size
    
    def forward(self, x):
        # Reshape for conv1d (batch_size, channels, sequence_length)
        x = x.unsqueeze(1)
        
        x = self.relu(self.conv1(x))
        x = self.pool(x)
        
        x = self.relu(self.conv2(x))
        x = self.pool(x)
        
        x = self.relu(self.conv3(x))
        x = self.pool(x)
        
        x = x.view(x.size(0), -1)  # Flatten
        
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        
        x = self.relu(self.fc2(x))
        x = self.dropout(x)
        
        x = self.fc3(x)
        
        return x

class AudioDepressionModel:
    """Audio-based depression detection model"""
    
    def __init__(self, model_type='random_forest', use_deep_learning=False):
        self.model_type = model_type
        self.use_deep_learning = use_deep_learning
        self.model = None
        self.scaler = None
        self.is_trained = False
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
    def _initialize_model(self):
        """Initialize the ML model based on type"""
        if self.use_deep_learning:
            self.model = AudioCNN().to(self.device)
        elif self.model_type == 'random_forest':
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
    
    def extract_audio_features(self, audio_data: np.ndarray, sr: int = 16000) -> np.ndarray:
        """Extract comprehensive audio features"""
        features = []
        
        # MFCC features
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
        
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=audio_data, sr=sr)
        features.append(np.mean(spectral_bandwidth))
        features.append(np.std(spectral_bandwidth))
        
        # Zero crossing rate
        zcr = librosa.feature.zero_crossing_rate(audio_data)
        features.append(np.mean(zcr))
        features.append(np.std(zcr))
        
        # Chroma features
        chroma = librosa.feature.chroma_stft(y=audio_data, sr=sr)
        features.extend(np.mean(chroma, axis=1))
        features.extend(np.std(chroma, axis=1))
        
        # Tonnetz features
        tonnetz = librosa.feature.tonnetz(y=audio_data, sr=sr)
        features.extend(np.mean(tonnetz, axis=1))
        features.extend(np.std(tonnetz, axis=1))
        
        # Rhythm features
        tempo, _ = librosa.beat.beat_track(y=audio_data, sr=sr)
        features.append(tempo)
        
        # RMS energy
        rms = librosa.feature.rms(y=audio_data)
        features.append(np.mean(rms))
        features.append(np.std(rms))
        
        return np.array(features)
    
    def preprocess_audio_features(self, features: np.ndarray) -> np.ndarray:
        """Preprocess audio features"""
        if self.scaler is None:
            self.scaler = StandardScaler()
            return self.scaler.fit_transform(features)
        else:
            return self.scaler.transform(features)
    
    def train(self, X: np.ndarray, y: List[int], test_size=0.2) -> Dict[str, Any]:
        """Train the audio depression detection model"""
        logger.info(f"Training {self.model_type} model on {len(X)} samples")
        
        # Initialize model if not done
        if self.model is None:
            self._initialize_model()
        
        # Preprocess features
        X_processed = self.preprocess_audio_features(X)
        
        if self.use_deep_learning:
            return self._train_deep_learning(X_processed, y, test_size)
        else:
            return self._train_traditional_ml(X_processed, y, test_size)
    
    def _train_traditional_ml(self, X: np.ndarray, y: List[int], test_size: float) -> Dict[str, Any]:
        """Train traditional ML model"""
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        # Train model
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Cross-validation
        cv_scores = cross_val_score(self.model, X, y, cv=5)
        
        self.is_trained = True
        
        results = {
            'accuracy': accuracy,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'classification_report': classification_report(y_test, y_pred),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
        }
        
        logger.info(f"Model training completed. Accuracy: {accuracy:.4f}")
        return results
    
    def _train_deep_learning(self, X: np.ndarray, y: List[int], test_size: float) -> Dict[str, Any]:
        """Train deep learning model"""
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        # Create datasets
        train_dataset = AudioDataset(X_train, y_train)
        test_dataset = AudioDataset(X_test, y_test)
        
        train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
        test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)
        
        # Training setup
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        
        # Training loop
        num_epochs = 50
        train_losses = []
        
        for epoch in range(num_epochs):
            self.model.train()
            epoch_loss = 0
            
            for batch_features, batch_labels in train_loader:
                batch_features = batch_features.to(self.device)
                batch_labels = batch_labels.to(self.device)
                
                optimizer.zero_grad()
                outputs = self.model(batch_features)
                loss = criterion(outputs, batch_labels)
                loss.backward()
                optimizer.step()
                
                epoch_loss += loss.item()
            
            train_losses.append(epoch_loss / len(train_loader))
            
            if epoch % 10 == 0:
                logger.info(f"Epoch {epoch}, Loss: {epoch_loss / len(train_loader):.4f}")
        
        # Evaluation
        self.model.eval()
        correct = 0
        total = 0
        all_predictions = []
        all_labels = []
        
        with torch.no_grad():
            for batch_features, batch_labels in test_loader:
                batch_features = batch_features.to(self.device)
                batch_labels = batch_labels.to(self.device)
                
                outputs = self.model(batch_features)
                _, predicted = torch.max(outputs.data, 1)
                
                total += batch_labels.size(0)
                correct += (predicted == batch_labels).sum().item()
                
                all_predictions.extend(predicted.cpu().numpy())
                all_labels.extend(batch_labels.cpu().numpy())
        
        accuracy = correct / total
        self.is_trained = True
        
        results = {
            'accuracy': accuracy,
            'train_losses': train_losses,
            'classification_report': classification_report(all_labels, all_predictions),
            'confusion_matrix': confusion_matrix(all_labels, all_predictions).tolist()
        }
        
        logger.info(f"Deep learning model training completed. Accuracy: {accuracy:.4f}")
        return results
    
    def predict(self, audio_features: np.ndarray) -> Dict[str, Any]:
        """Predict depression risk from audio features"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        # Preprocess features
        X_processed = self.preprocess_audio_features(audio_features)
        
        if self.use_deep_learning:
            return self._predict_deep_learning(X_processed)
        else:
            return self._predict_traditional_ml(X_processed)
    
    def _predict_traditional_ml(self, X: np.ndarray) -> Dict[str, Any]:
        """Predict using traditional ML model"""
        predictions = self.model.predict(X)
        probabilities = self.model.predict_proba(X)
        
        results = []
        for pred, prob in zip(predictions, probabilities):
            risk_score = prob[1] if len(prob) > 1 else pred
            
            if risk_score < 0.3:
                risk_level = "no_risk"
            elif risk_score < 0.7:
                risk_level = "at_risk"
            else:
                risk_level = "high_risk"
            
            results.append({
                'prediction': int(pred),
                'risk_score': float(risk_score),
                'risk_level': risk_level,
                'confidence': float(max(prob))
            })
        
        return {'predictions': results}
    
    def _predict_deep_learning(self, X: np.ndarray) -> Dict[str, Any]:
        """Predict using deep learning model"""
        self.model.eval()
        
        with torch.no_grad():
            X_tensor = torch.FloatTensor(X).to(self.device)
            outputs = self.model(X_tensor)
            probabilities = torch.softmax(outputs, dim=1)
            predictions = torch.argmax(outputs, dim=1)
        
        results = []
        for pred, prob in zip(predictions.cpu().numpy(), probabilities.cpu().numpy()):
            risk_score = prob[1] if len(prob) > 1 else pred
            
            if risk_score < 0.3:
                risk_level = "no_risk"
            elif risk_score < 0.7:
                risk_level = "at_risk"
            else:
                risk_level = "high_risk"
            
            results.append({
                'prediction': int(pred),
                'risk_score': float(risk_score),
                'risk_level': risk_level,
                'confidence': float(max(prob))
            })
        
        return {'predictions': results}
    
    def save_model(self, filepath: str):
        """Save the trained model and scaler"""
        if not self.is_trained:
            raise ValueError("Model must be trained before saving")
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        if self.use_deep_learning:
            model_data = {
                'model_state_dict': self.model.state_dict(),
                'scaler': self.scaler,
                'model_type': self.model_type,
                'use_deep_learning': self.use_deep_learning,
                'is_trained': self.is_trained
            }
        else:
            model_data = {
                'model': self.model,
                'scaler': self.scaler,
                'model_type': self.model_type,
                'use_deep_learning': self.use_deep_learning,
                'is_trained': self.is_trained
            }
        
        joblib.dump(model_data, filepath)
        logger.info(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str):
        """Load a pre-trained model and scaler"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found: {filepath}")
        
        model_data = joblib.load(filepath)
        self.scaler = model_data['scaler']
        self.model_type = model_data['model_type']
        self.use_deep_learning = model_data['use_deep_learning']
        self.is_trained = model_data['is_trained']
        
        if self.use_deep_learning:
            self.model = AudioCNN().to(self.device)
            self.model.load_state_dict(model_data['model_state_dict'])
        else:
            self.model = model_data['model']
        
        logger.info(f"Model loaded from {filepath}")
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        return {
            'model_type': self.model_type,
            'use_deep_learning': self.use_deep_learning,
            'is_trained': self.is_trained,
            'has_scaler': self.scaler is not None,
            'device': str(self.device)
        }
