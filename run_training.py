#!/usr/bin/env python3
"""
Run depression detection model training
"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import os

def main():
    print("Training Depression Detection Model...")
    
    # Load data
    df = pd.read_csv('augmented_dataset_75000.csv')
    df['binary_label'] = (df['label'] == 2).astype(int)
    print(f"Label distribution: {df['binary_label'].value_counts().to_dict()}")
    
    # Clean data
    df_clean = df.dropna(subset=['text', 'binary_label'])
    texts = df_clean['text'].astype(str).tolist()
    labels = df_clean['binary_label'].tolist()
    
    print(f"Training on {len(texts)} samples")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=labels
    )
    
    print(f"Train: {len(X_train)}, Test: {len(X_test)}")
    
    # Vectorize text
    vectorizer = TfidfVectorizer(
        max_features=1000,
        stop_words='english',
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.95
    )
    
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    print(f"Feature matrix shape: {X_train_vec.shape}")
    
    # Train model
    model = RandomForestClassifier(
        n_estimators=50,
        random_state=42,
        max_depth=10,
        min_samples_split=5
    )
    
    print("Training model...")
    model.fit(X_train_vec, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test_vec)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save model
    os.makedirs('data/models', exist_ok=True)
    model_data = {
        'model': model,
        'vectorizer': vectorizer,
        'accuracy': accuracy
    }
    
    joblib.dump(model_data, 'data/models/text_model.pkl')
    print("Model saved successfully!")
    
    # Test prediction
    test_text = "I feel really sad and hopeless today"
    test_vec = vectorizer.transform([test_text])
    prediction = model.predict(test_vec)[0]
    probability = model.predict_proba(test_vec)[0]
    
    print(f"\nTest Prediction:")
    print(f"Text: '{test_text}'")
    print(f"Prediction: {'Depression Risk' if prediction == 1 else 'No Depression Risk'}")
    print(f"Confidence: {max(probability):.4f}")
    
    print("\nTraining completed successfully!")

if __name__ == '__main__':
    main()
