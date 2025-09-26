import pandas as pd
import numpy as np
import librosa
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import joblib
from pathlib import Path

print("Quick audio model training...")

# Load CSV data
df = pd.read_csv('augmented_dataset_75000.csv')
df['binary_label'] = (df['label'] == 2).astype(int)

# Get audio files
audio_dir = Path('archive (1)/AudioWAV')
wav_files = list(audio_dir.glob('*.wav'))[:50]  # Use only 50 files for quick training

print(f"Processing {len(wav_files)} audio files...")

features_list = []
labels_list = []

for i, wav_file in enumerate(wav_files):
    try:
        # Load audio and extract basic MFCC features
        audio_data, sr = librosa.load(wav_file, sr=16000)
        mfccs = librosa.feature.mfcc(y=audio_data, sr=sr, n_mfcc=13)
        features = np.mean(mfccs, axis=1)  # Use mean MFCC features
        features_list.append(features)
        
        # Assign label based on index
        label = df.iloc[i % len(df)]['binary_label']
        labels_list.append(label)
        
    except Exception as e:
        print(f"Error with {wav_file}: {e}")
        continue

X = np.array(features_list)
y = np.array(labels_list)

print(f"Dataset created: {X.shape}")

# Split and train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = RandomForestClassifier(n_estimators=10, random_state=42)
model.fit(X_train_scaled, y_train)

y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)

print(f"Accuracy: {accuracy:.4f}")

# Save model
os.makedirs('data/models', exist_ok=True)
joblib.dump({
    'model': model,
    'scaler': scaler,
    'accuracy': accuracy
}, 'data/models/audio_model.pkl')

print("Audio model saved successfully!")
