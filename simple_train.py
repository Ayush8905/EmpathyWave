#!/usr/bin/env python3
"""
Simple training script for depression detection
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import os

def main():
    print("🚀 Starting Depression Detection Model Training...")
    
    # Load dataset
    print("📊 Loading dataset...")
    df = pd.read_csv('augmented_dataset_75000.csv')
    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    
    # Check label distribution
    print(f"\nLabel distribution:")
    print(df['label'].value_counts())
    
    # Prepare data
    print("\n🔧 Preparing data...")
    # Convert labels: 0 -> 0 (no depression), 2 -> 1 (depression)
    df['binary_label'] = (df['label'] == 2).astype(int)
    
    # Remove missing values
    df_clean = df.dropna(subset=['text', 'binary_label'])
    print(f"Clean dataset shape: {df_clean.shape}")
    
    # Extract text and labels
    texts = df_clean['text'].astype(str).tolist()
    labels = df_clean['binary_label'].tolist()
    
    print(f"Text samples: {len(texts)}")
    print(f"Label distribution: {pd.Series(labels).value_counts().to_dict()}")
    
    # Split data
    print("\n📈 Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=labels
    )
    
    print(f"Training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")
    
    # Vectorize text
    print("\n🔤 Vectorizing text...")
    vectorizer = TfidfVectorizer(
        max_features=5000,
        stop_words='english',
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.95
    )
    
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    print(f"Feature matrix shape: {X_train_vec.shape}")
    
    # Train model
    print("\n🤖 Training Random Forest model...")
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        max_depth=10,
        min_samples_split=5
    )
    
    model.fit(X_train_vec, y_train)
    
    # Evaluate model
    print("\n📊 Evaluating model...")
    y_pred = model.predict(X_test_vec)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save model
    print("\n💾 Saving model...")
    os.makedirs('data/models', exist_ok=True)
    
    model_data = {
        'model': model,
        'vectorizer': vectorizer,
        'accuracy': accuracy
    }
    
    joblib.dump(model_data, 'data/models/text_model.pkl')
    print("✅ Model saved successfully!")
    
    # Test prediction
    print("\n🧪 Testing prediction...")
    test_text = "I feel really sad and hopeless today"
    test_vec = vectorizer.transform([test_text])
    prediction = model.predict(test_vec)[0]
    probability = model.predict_proba(test_vec)[0]
    
    print(f"Test text: '{test_text}'")
    print(f"Prediction: {'Depression' if prediction == 1 else 'No Depression'}")
    print(f"Probability: {probability}")
    
    print("\n🎉 Training completed successfully!")

if __name__ == '__main__':
    main()
