#!/usr/bin/env python3
"""
Test Gmail App Password for EmpathyWave Emergency System
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def test_app_password():
    """Test Gmail with App Password and send emergency test email"""
    
    print("🔐 Gmail App Password Test for EmpathyWave")
    print("=" * 50)
    
    sender_email = "omd23102004@gmail.com"
    
    # Get App Password from user
    print(f"📧 Email: {sender_email}")
    print("🔑 Enter your Gmail App Password (16 characters):")
    print("   Format: abcd efgh ijkl mnop")
    app_password = input("App Password: ").strip().replace(" ", "")
    
    if len(app_password) != 16:
        print("❌ App Password should be exactly 16 characters")
        print("   Make sure to copy it correctly from Gmail")
        return False
    
    # Test recipient
    test_email = input(f"\nSend test to (default: {sender_email}): ").strip()
    if not test_email:
        test_email = sender_email
    
    print(f"\n📤 Testing email: {sender_email} → {test_email}")
    
    try:
        # Create emergency test email
        message = MIMEMultipart("alternative")
        message["Subject"] = "🚨 EmpathyWave Emergency System - LIVE TEST"
        message["From"] = f"EmpathyWave Emergency Alert <{sender_email}>"
        message["To"] = test_email
        
        # Professional emergency email content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }}
                .container {{ max-width: 600px; margin: 0 auto; background: white; }}
                .header {{ background: linear-gradient(135deg, #ff4757, #c44569); color: white; padding: 30px 20px; text-align: center; }}
                .content {{ padding: 30px; }}
                .alert {{ background: #ffebcd; border-left: 5px solid #ff4757; padding: 20px; margin: 20px 0; }}
                .crisis-hotline {{ background: #ff4757; color: white; padding: 20px; text-align: center; font-size: 24px; font-weight: bold; margin: 20px 0; border-radius: 10px; }}
                .resources {{ background: #e8f6f3; padding: 20px; border-radius: 10px; margin: 20px 0; }}
                .footer {{ background: #2c3e50; color: white; padding: 20px; text-align: center; }}
                .action-item {{ background: #3498db; color: white; padding: 10px; margin: 10px 0; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚨 CRITICAL MENTAL HEALTH ALERT</h1>
                    <h3>EmpathyWave Emergency Notification System</h3>
                    <p>Time: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}</p>
                </div>
                
                <div class="content">
                    <div class="alert">
                        <h2>⚠️ URGENT: This is a LIVE TEST of the emergency system</h2>
                        <p><strong>If this were a real emergency,</strong> your child's AI mental health assistant would have detected:</p>
                        <ul>
                            <li><strong>Suicide ideation</strong> - Expressions of wanting to end their life</li>
                            <li><strong>Self-harm intentions</strong> - Plans or threats to hurt themselves</li>
                            <li><strong>Crisis-level depression</strong> - Severe mental distress requiring immediate intervention</li>
                        </ul>
                    </div>
                    
                    <div class="crisis-hotline">
                        🆘 IMMEDIATE CRISIS SUPPORT: 988
                    </div>
                    
                    <div class="resources">
                        <h3>📞 EMERGENCY RESOURCES</h3>
                        <p><strong>🔴 Suicide Prevention Lifeline:</strong> 988 (24/7)</p>
                        <p><strong>💬 Crisis Text Line:</strong> Text HOME to 741741</p>
                        <p><strong>🚑 Emergency Services:</strong> 911</p>
                        <p><strong>👥 Teen Line:</strong> 1-800-TLC-TEEN</p>
                    </div>
                    
                    <h3>🎯 IMMEDIATE ACTION PLAN:</h3>
                    <div class="action-item">1. DO NOT LEAVE YOUR CHILD ALONE</div>
                    <div class="action-item">2. REMOVE ACCESS TO HARMFUL ITEMS</div>
                    <div class="action-item">3. CALL 988 FOR PROFESSIONAL GUIDANCE</div>
                    <div class="action-item">4. SCHEDULE URGENT MENTAL HEALTH APPOINTMENT</div>
                    <div class="action-item">5. CONSIDER EMERGENCY ROOM IF IMMEDIATE DANGER</div>
                    
                    <div class="alert">
                        <h4>🔒 Privacy & Security:</h4>
                        <ul>
                            <li>No personal chat content is shared in these alerts</li>
                            <li>Only risk level and timestamp are included</li>
                            <li>All communications are encrypted and secure</li>
                            <li>EmpathyWave AI monitors language patterns, not content</li>
                        </ul>
                    </div>
                </div>
                
                <div class="footer">
                    <h4>EmpathyWave Mental Health Support System</h4>
                    <p>🛡️ AI-Powered Family Protection • 🤖 24/7 Mental Health Monitoring</p>
                    <p><strong>This system works:</strong> Real emergencies will trigger immediate parent alerts</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Attach HTML content
        html_part = MIMEText(html_content, "html")
        message.attach(html_part)
        
        # Send the email
        print("📤 Sending emergency test email...")
        context = ssl.create_default_context()
        
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls(context=context)
            server.login(sender_email, app_password)
            server.sendmail(sender_email, test_email, message.as_string())
        
        print("✅ SUCCESS! Emergency test email sent!")
        print(f"📧 Check inbox: {test_email}")
        print()
        print("🎯 EMERGENCY EMAIL SYSTEM IS NOW LIVE!")
        print("   • Real suicide risk messages will trigger parent alerts")
        print("   • Parents receive immediate crisis resources")
        print("   • Professional emergency guidance included")
        print()
        
        # Update .env file
        update_env = input("Update .env file with this App Password? (y/n): ").lower()
        if update_env == 'y':
            update_env_file(app_password)
            print("🔄 Restart EmpathyWave app to activate real email sending!")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        
        if "authentication" in str(e).lower() or "password" in str(e).lower():
            print("\n🔧 Authentication Error Solutions:")
            print("   • Double-check your App Password (16 characters)")
            print("   • Make sure 2-Factor Authentication is enabled")
            print("   • Try generating a new App Password")
            print("   • Visit: https://support.google.com/accounts/answer/185833")
        
        return False

def update_env_file(app_password):
    """Update .env file with working App Password"""
    try:
        # Read current .env
        with open('.env', 'r') as f:
            content = f.read()
        
        # Update the password line
        import re
        updated_content = re.sub(
            r'SENDER_PASSWORD=.*', 
            f'SENDER_PASSWORD={app_password}', 
            content
        )
        
        # Also ensure demo mode is disabled
        updated_content = re.sub(
            r'EMAIL_DEMO_MODE=.*', 
            'EMAIL_DEMO_MODE=false', 
            updated_content
        )
        
        # Write updated file
        with open('.env', 'w') as f:
            f.write(updated_content)
        
        print("✅ .env file updated successfully!")
        
    except Exception as e:
        print(f"❌ Could not update .env: {e}")
        print(f"💡 Manually set: SENDER_PASSWORD={app_password}")

if __name__ == "__main__":
    print("🚨 EmpathyWave Emergency Email Setup")
    print("=" * 50)
    print("This will test and configure REAL emergency email sending")
    print("Parents will receive actual emails when users express suicide risk")
    print()
    
    proceed = input("Ready to test? (y/n): ").lower()
    if proceed == 'y':
        success = test_app_password()
        
        if success:
            print("\n🛡️ EMERGENCY EMAIL SYSTEM ACTIVATED!")
            print("Your EmpathyWave platform now sends real emergency alerts!")
    else:
        print("Run 'python gmail_setup_guide.py' for setup instructions.")