#!/usr/bin/env python3
"""
Real Email Testing Script for EmpathyWave Emergency System
Tests actual email sending with your Gmail credentials
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from emergency_email_service import EmergencyEmailService
from database import DatabaseManager
from dotenv import load_dotenv
import datetime

# Load environment variables
load_dotenv()

def test_real_email_system():
    """Test the real email system with your Gmail credentials"""
    
    print("🚨 Testing REAL EMAIL Emergency System")
    print("=" * 60)
    
    # Initialize services
    email_service = EmergencyEmailService()
    db = DatabaseManager()
    
    # Test user data - using your email as parent for testing
    test_user_data = {
        'user_id': 101,
        'email': 'test.child@example.com',
        'parent_email': 'omd23102004@gmail.com',  # Your email to receive test
        'parent_phone': '+1234567890'
    }
    
    print(f"📧 Email Service Configuration:")
    print(f"   Sender Email: {email_service.sender_email}")
    print(f"   Demo Mode: {'✅ ENABLED' if email_service.demo_mode else '❌ DISABLED (REAL EMAILS)'}")
    print(f"   SMTP Server: {email_service.smtp_server}:{email_service.smtp_port}")
    print(f"   Password Set: {'✅ YES' if email_service.sender_password else '❌ NO'}")
    print()
    
    if email_service.demo_mode:
        print("⚠️  WARNING: Still in demo mode! Check your .env configuration.")
        print("   Make sure EMAIL_DEMO_MODE=false and SENDER_PASSWORD is set")
        return
    
    # Test critical risk assessment
    critical_risk_assessment = {
        'level': 'CRITICAL',
        'score': 350.0,
        'summary': 'URGENT: User expressed explicit suicide ideation with detailed plans. Multiple critical indicators detected including "I want to kill myself", "end my life", and "suicide is the only way". Immediate intervention required.'
    }
    
    print("🚨 TESTING CRITICAL EMERGENCY EMAIL")
    print(f"   👤 Test User: {test_user_data['email']}")
    print(f"   📧 Sending to: {test_user_data['parent_email']} (YOUR EMAIL)")
    print(f"   ⚠️  Risk Level: {critical_risk_assessment['level']}")
    print(f"   📊 Risk Score: {critical_risk_assessment['score']}")
    print()
    
    try:
        print("📤 Attempting to send real emergency email...")
        
        # Send the emergency email
        result = email_service.send_emergency_alert(
            user_data=test_user_data,
            risk_assessment=critical_risk_assessment
        )
        
        if result:
            print("✅ SUCCESS: Emergency email sent successfully!")
            print(f"   📧 Check your inbox: {test_user_data['parent_email']}")
            print("   📄 Email contains:")
            print("      • Crisis hotlines and emergency contacts")
            print("      • Professional mental health resources") 
            print("      • Immediate action recommendations")
            print("      • User risk assessment details")
            
            # Create database record
            try:
                alert_id = db.create_emergency_alert(
                    user_id=test_user_data['user_id'],
                    risk_level=critical_risk_assessment['level'],
                    risk_score=critical_risk_assessment['score'],
                    parent_email=test_user_data['parent_email'],
                    message_content='Test suicide message for emergency system',
                    risk_indicators='["kill myself", "suicide ideation", "end my life"]'
                )
                
                # Mark as sent
                db.update_emergency_alert_sent(alert_id, datetime.datetime.now())
                print(f"   📊 Database record created (Alert ID: {alert_id})")
                
            except Exception as db_error:
                print(f"   ⚠️  Database error (email still sent): {db_error}")
                
        else:
            print("❌ FAILED: Could not send emergency email")
            print("   Check the error messages above for details")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        
        # Common error troubleshooting
        if "authentication" in str(e).lower() or "password" in str(e).lower():
            print("\n🔧 AUTHENTICATION ERROR - Possible Solutions:")
            print("   1. Enable 'Less secure app access' in Gmail settings")
            print("   2. OR use Gmail App Password instead:")
            print("      • Go to Google Account → Security → App Passwords")
            print("      • Generate new App Password for 'EmpathyWave'")
            print("      • Replace regular password with 16-character App Password")
            
        elif "connection" in str(e).lower():
            print("\n🔧 CONNECTION ERROR - Check:")
            print("   • Internet connection")
            print("   • Gmail SMTP settings (smtp.gmail.com:587)")
            print("   • Firewall/antivirus blocking connection")
            
    print("\n" + "=" * 60)
    print("🎯 Real Email Test Complete!")
    
    if not email_service.demo_mode:
        print("✅ Your EmpathyWave emergency email system is configured for REAL email sending!")
        print("🛡️ When users express suicide risk, parents will receive immediate alerts.")
    else:
        print("⚠️  Still in demo mode - check .env configuration")

def test_gmail_connection():
    """Test basic Gmail SMTP connection"""
    print("\n🔗 Testing Gmail SMTP Connection...")
    
    import smtplib
    import ssl
    
    try:
        # Test connection to Gmail SMTP
        context = ssl.create_default_context()
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls(context=context)
            server.login("omd23102004@gmail.com", "qwertyuiop@123@")
            print("✅ Gmail SMTP Connection Successful!")
            return True
            
    except Exception as e:
        print(f"❌ Gmail Connection Failed: {e}")
        return False

if __name__ == "__main__":
    # First test basic connection
    connection_ok = test_gmail_connection()
    
    if connection_ok:
        # Then test full email system
        test_real_email_system()
    else:
        print("\n💡 Fix Gmail connection issues first, then run this test again.")
        print("   Consider using Gmail App Password for better security.")