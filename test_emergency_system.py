#!/usr/bin/env python3
"""
Emergency Email System Test
Tests the emergency alert functionality for high-risk depression detection
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from depression_risk_analyzer import risk_analyzer
from emergency_email_service import email_service
from database import DatabaseManager
import json

def test_risk_analyzer():
    """Test the depression risk analyzer with various message types"""
    
    print("🧪 Testing Depression Risk Analyzer...")
    print("=" * 50)
    
    # Test messages with different risk levels
    test_messages = [
        # Critical risk messages
        {
            'message': "I want to kill myself. I can't take this anymore.",
            'expected_level': 'CRITICAL'
        },
        {
            'message': "I'm planning to end my life tonight. Nobody will miss me.",
            'expected_level': 'CRITICAL'
        },
        {
            'message': "I have pills ready. This is my final goodbye.",
            'expected_level': 'CRITICAL'
        },
        
        # High risk messages
        {
            'message': "I'm severely depressed and feel completely hopeless. There's no point in living.",
            'expected_level': 'HIGH'
        },
        {
            'message': "I'm extremely sad all the time. I feel like a burden to everyone.",
            'expected_level': 'HIGH'
        },
        
        # Medium risk messages
        {
            'message': "I've been feeling really depressed lately and can't sleep.",
            'expected_level': 'MEDIUM'
        },
        {
            'message': "I'm anxious and stressed about everything. I don't want to see anyone.",
            'expected_level': 'MEDIUM'
        },
        
        # Low risk messages
        {
            'message': "I had a good day today. Spent time with friends.",
            'expected_level': 'LOW'
        },
        {
            'message': "Things are getting better. I'm feeling more hopeful.",
            'expected_level': 'LOW'
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_messages, 1):
        print(f"\n{i}. Testing: \"{test_case['message'][:50]}{'...' if len(test_case['message']) > 50 else ''}\"")
        
        # Analyze the message
        assessment = risk_analyzer.analyze_message(
            user_id="test_user_1",
            message=test_case['message']
        )
        
        # Check result
        detected_level = assessment['risk_level']
        expected_level = test_case['expected_level']
        is_correct = detected_level == expected_level
        
        print(f"   Expected: {expected_level}")
        print(f"   Detected: {detected_level}")
        print(f"   Score: {assessment['risk_score']:.2f}")
        print(f"   Emergency Alert: {'YES' if assessment['emergency_alert_required'] else 'NO'}")
        print(f"   Result: {'✅ CORRECT' if is_correct else '❌ INCORRECT'}")
        
        if assessment['indicators']['critical']:
            print(f"   Critical Indicators: {assessment['indicators']['critical']}")
        if assessment['indicators']['high']:
            print(f"   High Risk Indicators: {assessment['indicators']['high']}")
        
        results.append({
            'message': test_case['message'],
            'expected': expected_level,
            'detected': detected_level,
            'correct': is_correct,
            'score': assessment['risk_score'],
            'emergency_required': assessment['emergency_alert_required']
        })
    
    # Summary
    correct_count = sum(1 for r in results if r['correct'])
    total_count = len(results)
    accuracy = (correct_count / total_count) * 100
    
    print(f"\n📊 SUMMARY:")
    print(f"   Accuracy: {correct_count}/{total_count} ({accuracy:.1f}%)")
    print(f"   Emergency Alerts Triggered: {sum(1 for r in results if r['emergency_required'])}")
    
    return results

def test_email_system():
    """Test the emergency email system (without actually sending emails)"""
    
    print("\n📧 Testing Emergency Email System...")
    print("=" * 50)
    
    # Mock user data
    test_user_data = {
        'email': 'testuser@example.com',
        'parent_email': 'parent@example.com'
    }
    
    # Mock risk assessment
    test_risk_assessment = {
        'level': 'CRITICAL',
        'score': 95.5,
        'summary': 'AI analysis detected multiple critical risk indicators including self-harm intentions.'
    }
    
    print(f"User: {test_user_data['email']}")
    print(f"Parent Email: {test_user_data['parent_email']}")
    print(f"Risk Level: {test_risk_assessment['level']}")
    print(f"Risk Score: {test_risk_assessment['score']}")
    
    # Test email template rendering (without actually sending)
    try:
        # Create email service instance
        service = email_service
        
        # Get email template
        template = service._get_emergency_template()
        
        # Format template with test data
        formatted_email = template.format(
            app_name=service.app_name,
            user_email=test_user_data['email'],
            risk_level=test_risk_assessment['level'],
            risk_class='critical',
            timestamp="September 26, 2025 at 10:30 PM",
            analysis_summary=test_risk_assessment['summary']
        )
        
        print("✅ Email template formatted successfully")
        print(f"   Template length: {len(formatted_email)} characters")
        print(f"   Contains emergency contacts: {'SAMHSA' in formatted_email}")
        print(f"   Contains crisis resources: {'988' in formatted_email}")
        
        return True
        
    except Exception as e:
        print(f"❌ Email template test failed: {str(e)}")
        return False

def test_database_integration():
    """Test database integration for emergency alerts"""
    
    print("\n🗄️ Testing Database Integration...")
    print("=" * 50)
    
    try:
        # Initialize database
        db = DatabaseManager()
        
        # Test emergency alert creation
        alert_id = db.create_emergency_alert(
            user_id=999,  # Test user ID
            risk_level='CRITICAL',
            risk_score=95.0,
            parent_email='test@example.com',
            message_content='Test emergency message',
            risk_indicators='["self-harm", "suicidal ideation"]'
        )
        
        if alert_id:
            print(f"✅ Emergency alert created with ID: {alert_id}")
            
            # Test updating alert as sent
            import datetime
            success = db.update_emergency_alert_sent(alert_id, datetime.datetime.now())
            
            if success:
                print("✅ Emergency alert updated as sent")
            else:
                print("❌ Failed to update emergency alert")
            
            # Test retrieving recent alerts
            recent_alerts = db.get_recent_emergency_alerts(999, hours=24)
            print(f"✅ Retrieved {len(recent_alerts)} recent alerts")
            
            return True
        else:
            print("❌ Failed to create emergency alert")
            return False
            
    except Exception as e:
        print(f"❌ Database test failed: {str(e)}")
        return False

def run_comprehensive_test():
    """Run comprehensive test of the emergency system"""
    
    print("🚨 EmpathyWave Emergency Alert System Test")
    print("=" * 60)
    
    # Test 1: Risk Analyzer
    risk_results = test_risk_analyzer()
    
    # Test 2: Email System
    email_success = test_email_system()
    
    # Test 3: Database Integration
    db_success = test_database_integration()
    
    # Final Summary
    print("\n🎯 FINAL TEST RESULTS:")
    print("=" * 30)
    
    # Risk analyzer summary
    emergency_triggers = sum(1 for r in risk_results if r['emergency_required'])
    print(f"Risk Analyzer: {len(risk_results)} tests completed")
    print(f"Emergency Triggers: {emergency_triggers}")
    
    # Email system summary
    print(f"Email System: {'✅ PASS' if email_success else '❌ FAIL'}")
    
    # Database summary
    print(f"Database Integration: {'✅ PASS' if db_success else '❌ FAIL'}")
    
    # Overall status
    all_systems_good = email_success and db_success and emergency_triggers > 0
    
    print(f"\n🚨 EMERGENCY SYSTEM STATUS: {'🟢 OPERATIONAL' if all_systems_good else '🔴 NEEDS ATTENTION'}")
    
    if all_systems_good:
        print("\n✅ The emergency alert system is ready to protect users!")
        print("   - Risk detection is working")
        print("   - Email templates are functional")
        print("   - Database logging is operational")
    else:
        print("\n⚠️  Some components need attention before deployment.")
    
    return all_systems_good

if __name__ == "__main__":
    run_comprehensive_test()