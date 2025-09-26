#!/usr/bin/env python3
"""
Emergency Email Setup Guide for EmpathyWave
Step-by-step configuration for Gmail emergency alerts
"""

import os
from dotenv import load_dotenv

def setup_gmail_for_emergency_alerts():
    """
    Guide for setting up Gmail for emergency alerts
    """
    
    print("📧 EmpathyWave Emergency Email Setup Guide")
    print("=" * 50)
    
    print("\n🔐 Step 1: Create Gmail App Password")
    print("-" * 35)
    print("1. Go to your Google Account settings: https://myaccount.google.com/")
    print("2. Navigate to 'Security' → '2-Step Verification' (enable if not already)")
    print("3. Go to 'Security' → 'App passwords'")
    print("4. Select 'Mail' and 'Other (Custom name)'")
    print("5. Enter 'EmpathyWave Emergency Alerts'")
    print("6. Copy the generated 16-character app password")
    
    print("\n⚙️ Step 2: Configure Environment Variables")
    print("-" * 42)
    print("Add these variables to your .env file:")
    print("SENDER_EMAIL=your-gmail-address@gmail.com")
    print("SENDER_PASSWORD=your-16-character-app-password")
    
    print("\n📝 Step 3: Test Configuration")
    print("-" * 30)
    print("Run: python test_emergency_system.py")
    
    print("\n🚨 Step 4: Emergency Alert Triggers")
    print("-" * 36)
    print("Emergency emails are sent when users express:")
    print("• Self-harm intentions")
    print("• Suicidal thoughts")
    print("• Severe depression with hopelessness")
    print("• Crisis-level emotional distress")
    
    print("\n⏰ Step 5: Alert Frequency Limits")
    print("-" * 32)
    print("To prevent spam:")
    print("• Maximum 1 critical alert per 6 hours per user")
    print("• Parents receive comprehensive emergency information")
    print("• Follow-up resources and crisis hotlines included")
    
    print("\n✅ Step 6: Verify Setup")
    print("-" * 25)
    print("Test with these sample high-risk messages:")
    print("1. 'I want to end my life'")
    print("2. 'I'm planning to hurt myself'")
    print("3. 'I feel hopeless and want to die'")
    
    # Check current configuration
    load_dotenv()
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    
    print("\n📊 Current Configuration Status:")
    print("-" * 33)
    print(f"Sender Email: {'✅ Configured' if sender_email else '❌ Missing'}")
    print(f"Sender Password: {'✅ Configured' if sender_password else '❌ Missing'}")
    
    if sender_email and sender_password:
        print("\n🎉 Configuration Complete!")
        print("Emergency email system is ready to protect users.")
        return True
    else:
        print("\n⚠️  Configuration Incomplete")
        print("Please add missing environment variables to .env file.")
        return False

def create_env_template():
    """Create .env template if it doesn't exist"""
    
    env_path = '.env'
    
    if not os.path.exists(env_path):
        print(f"\n📄 Creating {env_path} template...")
        
        env_content = """# Flask Configuration
SECRET_KEY=empathy-wave-enhanced-secret-key-2024
FLASK_ENV=development
PORT=5000

# Database Configuration
DATABASE_URL=sqlite:///empathy_wave.db

# Google Gemini API
GEMINI_API_KEY=your-gemini-api-key-here

# Emergency Email Configuration
SENDER_EMAIL=your-gmail-address@gmail.com
SENDER_PASSWORD=your-16-character-app-password-here
"""
        
        with open(env_path, 'w') as f:
            f.write(env_content)
        
        print(f"✅ Created {env_path} template")
        print("Please edit this file with your actual values.")
        return True
    else:
        print(f"\n📄 {env_path} already exists")
        return False

def test_email_connection():
    """Test email connection without sending actual emails"""
    
    load_dotenv()
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    
    print("\n🔗 Testing Email Connection...")
    print("-" * 30)
    
    if not sender_email or not sender_password:
        print("❌ Email credentials not configured")
        return False
    
    try:
        import smtplib
        import ssl
        
        # Test SMTP connection
        context = ssl.create_default_context()
        
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls(context=context)
            server.login(sender_email, sender_password)
            print("✅ Gmail SMTP connection successful")
            return True
            
    except Exception as e:
        print(f"❌ Email connection failed: {str(e)}")
        print("\n🔧 Troubleshooting:")
        print("1. Verify Gmail app password is correct")
        print("2. Ensure 2-Factor Authentication is enabled")
        print("3. Check internet connection")
        return False

if __name__ == "__main__":
    print("🌊 EmpathyWave Emergency Alert System Setup")
    print("=" * 50)
    
    # Create .env template if needed
    create_env_template()
    
    # Run setup guide
    config_success = setup_gmail_for_emergency_alerts()
    
    # Test connection if configured
    if config_success:
        test_email_connection()
    
    print("\n🚀 Next Steps:")
    print("1. Complete .env configuration")
    print("2. Run: python test_emergency_system.py")
    print("3. Start application: python enhanced_chat_app.py")
    print("4. Test with high-risk messages")
    
    print("\n🆘 Emergency Resources:")
    print("• National Suicide Prevention Lifeline: 988")
    print("• Crisis Text Line: Text HOME to 741741")
    print("• Emergency Services: 911")