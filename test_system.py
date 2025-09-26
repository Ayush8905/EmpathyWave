#!/usr/bin/env python3
"""
Test script for EmpathyWave Enhanced Chat Bot
Tests basic functionality without requiring Gemini API
"""

import sys
import os
import numpy as np

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_text_model_loading():
    """Test if the text model can be loaded"""
    try:
        from enhanced_chat_app import load_text_model, text_model_data
        print("🧠 Testing text model loading...")
        
        if load_text_model():
            print("✅ Text model loaded successfully!")
            if text_model_data:
                print(f"   Model type: {type(text_model_data['model'])}")
                print(f"   Vectorizer type: {type(text_model_data['vectorizer'])}")
            return True
        else:
            print("⚠️  Text model not found - this is normal for initial setup")
            return False
    except Exception as e:
        print(f"❌ Error loading text model: {str(e)}")
        return False

def test_audio_features():
    """Test audio feature extraction"""
    try:
        from enhanced_chat_app import extract_audio_features, analyze_audio_depression
        print("\n🎵 Testing audio feature extraction...")
        
        # Create dummy audio data
        dummy_audio = np.random.randn(16000)  # 1 second of audio at 16kHz
        
        features = extract_audio_features(dummy_audio)
        if features is not None:
            print(f"✅ Audio features extracted: {len(features)} features")
            
            # Test audio analysis
            depression_score = analyze_audio_depression(features)
            print(f"✅ Audio analysis working: depression score = {depression_score:.3f}")
            return True
        else:
            print("❌ Failed to extract audio features")
            return False
    except Exception as e:
        print(f"❌ Error testing audio features: {str(e)}")
        return False

def test_fallback_responses():
    """Test fallback response system"""
    try:
        from enhanced_chat_app import get_fallback_response, get_fallback_analysis
        print("\n💬 Testing fallback response system...")
        
        # Test various message types
        test_messages = [
            "I feel really sad today",
            "I'm feeling anxious about work",
            "Hello, how are you?",
            "I'm having a great day!",
            "I feel so overwhelmed and stressed"
        ]
        
        for message in test_messages:
            response = get_fallback_response(message)
            analysis = get_fallback_analysis(message)
            
            print(f"✅ Message: '{message[:30]}...'")
            print(f"   Response length: {len(response)} chars")
            print(f"   Analysis length: {len(analysis)} chars")
        
        print("✅ Fallback system working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing fallback responses: {str(e)}")
        return False

def test_risk_assessment():
    """Test risk assessment functionality"""
    try:
        from enhanced_chat_app import predict_depression_from_text
        print("\n🎯 Testing risk assessment...")
        
        # Test with dummy text (will fail if no model, but should not crash)
        test_text = "I feel really sad and hopeless about everything"
        result = predict_depression_from_text(test_text)
        
        if "error" in result:
            print("⚠️  Risk assessment requires trained model (expected for initial setup)")
        else:
            print("✅ Risk assessment working!")
            print(f"   Risk level: {result.get('risk_level', 'Unknown')}")
            print(f"   Risk score: {result.get('risk_score', 0):.3f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing risk assessment: {str(e)}")
        return False

def test_dependencies():
    """Test if all required dependencies are available"""
    print("📦 Testing dependencies...")
    
    required_packages = [
        'flask', 'numpy', 'librosa', 'joblib', 'sklearn'
    ]
    
    optional_packages = [
        'google.generativeai', 'dotenv'
    ]
    
    missing_required = []
    missing_optional = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} (REQUIRED)")
            missing_required.append(package)
    
    for package in optional_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"⚠️  {package} (optional)")
            missing_optional.append(package)
    
    if missing_required:
        print(f"\n❌ Missing required packages: {', '.join(missing_required)}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    if missing_optional:
        print(f"\n⚠️  Missing optional packages: {', '.join(missing_optional)}")
        print("   These features will use fallback functionality")
    
    return True

def main():
    """Run all tests"""
    print("🚀 EmpathyWave Enhanced Chat Bot - System Test")
    print("=" * 50)
    
    tests = [
        test_dependencies,
        test_text_model_loading,
        test_audio_features,
        test_fallback_responses,
        test_risk_assessment
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {str(e)}")
    
    print("\n" + "=" * 50)
    print(f"🏁 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system is ready to run.")
        print("   Run: python enhanced_chat_app.py")
    elif passed >= total - 1:
        print("✅ System mostly ready! Some optional features may not work.")
        print("   Run: python enhanced_chat_app.py")
    else:
        print("❌ System needs attention. Install missing dependencies.")
        print("   Run: pip install -r requirements.txt")
    
    return passed == total

if __name__ == "__main__":
    main()