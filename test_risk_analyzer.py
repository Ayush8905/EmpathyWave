#!/usr/bin/env python3
"""
Test script for the depression risk analyzer
"""

from depression_risk_analyzer import risk_analyzer

def test_risk_analyzer():
    """Test various messages with the risk analyzer"""
    
    test_messages = [
        "I going to kill my self",
        "I want to kill myself",
        "I'm going to end it all",
        "suicide seems like the only option",
        "I feel depressed today",
        "I'm having a good day",
        "kill myself",
        "end my life",
        "I'm fine"
    ]
    
    print("🔍 Testing Depression Risk Analyzer")
    print("=" * 50)
    
    for message in test_messages:
        try:
            result = risk_analyzer.analyze_message('test_user', message)
            
            print(f"\n📝 Message: '{message}'")
            print(f"⚠️  Risk Level: {result['risk_level']}")
            print(f"📊 Risk Score: {result['risk_score']}")
            print(f"🚨 Emergency Alert: {result['emergency_alert_required']}")
            
            if result['indicators']['critical']:
                print(f"🔴 Critical Indicators: {result['indicators']['critical']}")
            if result['indicators']['high']:
                print(f"🟠 High Indicators: {result['indicators']['high']}")
            if result['indicators']['moderate']:
                print(f"🟡 Moderate Indicators: {result['indicators']['moderate']}")
                
        except Exception as e:
            print(f"❌ Error analyzing '{message}': {e}")
        
        print("-" * 30)

if __name__ == "__main__":
    test_risk_analyzer()