import joblib

# Load the trained model
model_data = joblib.load('data/models/text_model.pkl')
print("Model loaded successfully!")

model = model_data['model']
vectorizer = model_data['vectorizer']

# Test predictions
test_texts = [
    "I feel really sad and hopeless today",
    "I'm having a great day and feeling wonderful",
    "Everything seems pointless and I can't find joy in anything",
    "I love spending time with my friends and family"
]

print("\nTesting model predictions:")
for text in test_texts:
    test_vec = vectorizer.transform([text])
    prediction = model.predict(test_vec)[0]
    probability = model.predict_proba(test_vec)[0]
    
    result = "Depression Risk" if prediction == 1 else "No Depression Risk"
    confidence = max(probability)
    
    print(f"\nText: '{text}'")
    print(f"Prediction: {result}")
    print(f"Confidence: {confidence:.4f}")
