#!/usr/bin/env python3
"""
Test the depression detection model
"""

import joblib
import os

def test_model():
    print("🧪 Testing Depression Detection Model...")
    
    # Check if model exists
    model_path = 'data/models/text_model.pkl'
    if not os.path.exists(model_path):
        print("❌ Model file not found!")
        return False
    
    # Load model
    try:
        model_data = joblib.load(model_path)
        print("✅ Model loaded successfully!")
        
        model = model_data['model']
        vectorizer = model_data['vectorizer']
        
        # Test cases
        test_cases = [
            "I feel really sad and hopeless today",
            "I'm having a great day and feeling wonderful",
            "Everything seems pointless and I can't find joy in anything",
            "I love spending time with my friends and family",
            "I don't want to wake up tomorrow",
            "I'm excited about my new job opportunity"
        ]
        
        print("\n📊 Test Results:")
        print("-" * 60)
        
        for i, text in enumerate(test_cases, 1):
            # Make prediction
            text_vec = vectorizer.transform([text])
            prediction = model.predict(text_vec)[0]
            probability = model.predict_proba(text_vec)[0]
            
            # Determine risk level
            risk_score = probability[1] if len(probability) > 1 else prediction
            if risk_score < 0.3:
                risk_level = "No Risk"
            elif risk_score < 0.7:
                risk_level = "At Risk"
            else:
                risk_level = "High Risk"
            
            result = "Depression Risk" if prediction == 1 else "No Depression Risk"
            confidence = max(probability)
            
            print(f"\nTest {i}:")
            print(f"Text: '{text}'")
            print(f"Prediction: {result}")
            print(f"Risk Level: {risk_level}")
            print(f"Confidence: {confidence:.4f}")
            print(f"Risk Score: {risk_score:.4f}")
        
        print("\n" + "=" * 60)
        print("🎉 Model testing completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error loading model: {str(e)}")
        return False

if __name__ == '__main__':
    test_model()
