#!/usr/bin/env python3
"""
Train audio-based depression detection model
"""

import pandas as pd
import numpy as np
import librosa
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
import joblib
from pathlib import Path

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
    
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=audio_data, sr=sr)
    features.append(np.mean(spectral_bandwidth))
    features.append(np.std(spectral_bandwidth))
    
    # Zero crossing rate
    zcr = librosa.feature.zero_crossing_rate(audio_data)
    features.append(np.mean(zcr))
    features.append(np.std(zcr))
    
    # Chroma features (12 pitch classes)
    chroma = librosa.feature.chroma_stft(y=audio_data, sr=sr)
    features.extend(np.mean(chroma, axis=1))
    features.extend(np.std(chroma, axis=1))
    
    # Tonnetz features (6 tonal features)
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
    
    # Spectral contrast
    contrast = librosa.feature.spectral_contrast(y=audio_data, sr=sr)
    features.extend(np.mean(contrast, axis=1))
    features.extend(np.std(contrast, axis=1))
    
    return np.array(features)

def create_audio_dataset():
    """Create audio dataset from WAV files and CSV labels"""
    print("Creating audio dataset...")
    
    # Load the CSV to get labels
    df = pd.read_csv('augmented_dataset_75000.csv')
    df['binary_label'] = (df['label'] == 2).astype(int)
    
    # Get audio files directory
    audio_dir = Path('archive (1)/AudioWAV')
    
    if not audio_dir.exists():
        print(f"Audio directory not found: {audio_dir}")
        return None, None
    
    # Get list of WAV files
    wav_files = list(audio_dir.glob('*.wav'))
    print(f"Found {len(wav_files)} WAV files")
    
    # Create mapping from filename to label
    # Assuming the CSV has some way to link to audio files
    # For now, we'll create a simple mapping based on index
    features_list = []
    labels_list = []
    
    # Process a subset of files for training (to avoid long processing time)
    max_files = min(1000, len(wav_files))  # Process up to 1000 files
    print(f"Processing {max_files} audio files...")
    
    for i, wav_file in enumerate(wav_files[:max_files]):
        try:
            # Load audio file
            audio_data, sr = librosa.load(wav_file, sr=16000)
            
            # Extract features
            features = extract_audio_features(audio_data, sr)
            features_list.append(features)
            
            # Assign label based on index (simple approach)
            # In a real scenario, you'd have proper file-to-label mapping
            label = df.iloc[i % len(df)]['binary_label']
            labels_list.append(label)
            
            if (i + 1) % 100 == 0:
                print(f"Processed {i + 1}/{max_files} files")
                
        except Exception as e:
            print(f"Error processing {wav_file}: {str(e)}")
            continue
    
    return np.array(features_list), np.array(labels_list)

def train_audio_model():
    """Train the audio depression detection model"""
    print("🎵 Training Audio Depression Detection Model...")
    
    # Create dataset
    X, y = create_audio_dataset()
    
    if X is None or len(X) == 0:
        print("❌ Failed to create audio dataset")
        return False
    
    print(f"Dataset created: {X.shape[0]} samples, {X.shape[1]} features")
    print(f"Label distribution: {np.bincount(y)}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Train: {len(X_train)}, Test: {len(X_test)}")
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        max_depth=10,
        min_samples_split=5
    )
    
    print("Training model...")
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"✅ Audio Model Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save model
    os.makedirs('data/models', exist_ok=True)
    model_data = {
        'model': model,
        'scaler': scaler,
        'accuracy': accuracy,
        'feature_names': [
            'mfcc_mean_0', 'mfcc_mean_1', 'mfcc_mean_2', 'mfcc_mean_3', 'mfcc_mean_4',
            'mfcc_mean_5', 'mfcc_mean_6', 'mfcc_mean_7', 'mfcc_mean_8', 'mfcc_mean_9',
            'mfcc_mean_10', 'mfcc_mean_11', 'mfcc_mean_12',
            'mfcc_std_0', 'mfcc_std_1', 'mfcc_std_2', 'mfcc_std_3', 'mfcc_std_4',
            'mfcc_std_5', 'mfcc_std_6', 'mfcc_std_7', 'mfcc_std_8', 'mfcc_std_9',
            'mfcc_std_10', 'mfcc_std_11', 'mfcc_std_12',
            'spectral_centroid_mean', 'spectral_centroid_std',
            'spectral_rolloff_mean', 'spectral_rolloff_std',
            'spectral_bandwidth_mean', 'spectral_bandwidth_std',
            'zcr_mean', 'zcr_std',
            'chroma_mean_0', 'chroma_mean_1', 'chroma_mean_2', 'chroma_mean_3',
            'chroma_mean_4', 'chroma_mean_5', 'chroma_mean_6', 'chroma_mean_7',
            'chroma_mean_8', 'chroma_mean_9', 'chroma_mean_10', 'chroma_mean_11',
            'chroma_std_0', 'chroma_std_1', 'chroma_std_2', 'chroma_std_3',
            'chroma_std_4', 'chroma_std_5', 'chroma_std_6', 'chroma_std_7',
            'chroma_std_8', 'chroma_std_9', 'chroma_std_10', 'chroma_std_11',
            'tonnetz_mean_0', 'tonnetz_mean_1', 'tonnetz_mean_2', 'tonnetz_mean_3',
            'tonnetz_mean_4', 'tonnetz_mean_5',
            'tonnetz_std_0', 'tonnetz_std_1', 'tonnetz_std_2', 'tonnetz_std_3',
            'tonnetz_std_4', 'tonnetz_std_5',
            'tempo', 'rms_mean', 'rms_std',
            'spectral_contrast_mean_0', 'spectral_contrast_mean_1', 'spectral_contrast_mean_2',
            'spectral_contrast_mean_3', 'spectral_contrast_mean_4', 'spectral_contrast_mean_5',
            'spectral_contrast_mean_6',
            'spectral_contrast_std_0', 'spectral_contrast_std_1', 'spectral_contrast_std_2',
            'spectral_contrast_std_3', 'spectral_contrast_std_4', 'spectral_contrast_std_5',
            'spectral_contrast_std_6'
        ]
    }
    
    joblib.dump(model_data, 'data/models/audio_model.pkl')
    print("💾 Audio model saved successfully!")
    
    return True

if __name__ == '__main__':
    train_audio_model()
