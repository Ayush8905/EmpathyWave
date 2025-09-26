#!/usr/bin/env python3
"""
Gmail App Password Setup Guide and Test Script
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

def test_gmail_with_app_password():
    """Test Gmail connection and send a test email"""
    
    print("🔐 Gmail App Password Test")
    print("=" * 50)
    
    # Your credentials
    sender_email = "omd23102004@gmail.com"
    sender_name = "EmpathyWave Emergency System"
    
    # Ask for App Password
    print("📱 To send real emails, you need a Gmail App Password:")
    print("   1. Go to https://myaccount.google.com/security")
    print("   2. Enable 2-Step Verification if not already enabled")
    print("   3. Go to App Passwords section")
    print("   4. Generate password for 'EmpathyWave'")
    print("   5. Use the 16-character password (like: abcd efgh ijkl mnop)")
    print()
    
    app_password = input("Enter your Gmail App Password (16 characters): ").strip()
    
    if not app_password:
        print("❌ No password entered. Exiting.")
        return
    
    # Test email details
    test_parent_email = input("Enter parent email to test (or press Enter to use your email): ").strip()
    if not test_parent_email:
        test_parent_email = sender_email
    
    print(f"\n📧 Testing email from {sender_email} to {test_parent_email}")
    
    try:
        # Create test emergency email
        message = MIMEMultipart("alternative")
        message["Subject"] = "🚨 EmpathyWave Emergency Alert - TEST"
        message["From"] = f"{sender_name} <{sender_email}>"
        message["To"] = test_parent_email
        
        # HTML email content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f4f4f4; }}
                .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
                .header {{ background: linear-gradient(135deg, #ff4757, #ff3838); color: white; padding: 30px 20px; text-align: center; }}
                .content {{ padding: 30px; }}
                .alert-box {{ background: #ffe6e6; border-left: 4px solid #ff4757; padding: 15px; margin: 20px 0; }}
                .resources {{ background: #e8f4f8; padding: 20px; border-radius: 8px; margin: 20px 0; }}
                .footer {{ background: #f8f9fa; padding: 20px; text-align: center; font-size: 12px; color: #666; }}
                .crisis-number {{ font-size: 24px; font-weight: bold; color: #ff4757; text-align: center; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚨 EMERGENCY MENTAL HEALTH ALERT</h1>
                    <h2>EmpathyWave Security System</h2>
                </div>
                
                <div class="content">
                    <div class="alert-box">
                        <h3>⚠️ URGENT ATTENTION REQUIRED</h3>
                        <p><strong>This is a TEST email from EmpathyWave Emergency System</strong></p>
                        <p>Your child's AI mental health assistant has detected concerning messages that may indicate:</p>
                        <ul>
                            <li>Thoughts of self-harm or suicide</li>
                            <li>Severe depression symptoms</li>
                            <li>Crisis-level mental distress</li>
                        </ul>
                    </div>
                    
                    <div class="crisis-number">
                        🆘 CRISIS HOTLINE: 988
                    </div>
                    
                    <div class="resources">
                        <h3>📞 IMMEDIATE RESOURCES</h3>
                        <p><strong>National Suicide Prevention Lifeline:</strong> 988</p>
                        <p><strong>Crisis Text Line:</strong> Text HOME to 741741</p>
                        <p><strong>Emergency Services:</strong> 911</p>
                        <p><strong>Teen Line:</strong> 1-800-TLC-TEEN</p>
                    </div>
                    
                    <h3>🎯 RECOMMENDED IMMEDIATE ACTIONS:</h3>
                    <ol>
                        <li><strong>Stay with your child</strong> - Do not leave them alone</li>
                        <li><strong>Remove harmful items</strong> - Secure medications, sharp objects</li>
                        <li><strong>Contact emergency services</strong> if immediate danger</li>
                        <li><strong>Call crisis hotline</strong> for professional guidance</li>
                        <li><strong>Schedule urgent mental health appointment</strong></li>
                    </ol>
                    
                    <div class="alert-box">
                        <p><strong>⏰ Time:</strong> This alert was generated immediately upon detection</p>
                        <p><strong>🔒 Privacy:</strong> No personal chat content is shared, only risk level</p>
                        <p><strong>🤖 Source:</strong> EmpathyWave AI Mental Health Assistant</p>
                    </div>
                </div>
                
                <div class="footer">
                    <p>This is an automated alert from EmpathyWave Mental Health Support System</p>
                    <p>🛡️ Protecting your family with AI-powered mental health monitoring</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Attach HTML content
        html_part = MIMEText(html_content, "html")
        message.attach(html_part)
        
        # Send email
        print("📤 Sending test email...")
        context = ssl.create_default_context()
        
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls(context=context)
            server.login(sender_email, app_password)
            server.sendmail(sender_email, test_parent_email, message.as_string())
        
        print("✅ SUCCESS! Test emergency email sent successfully!")
        print(f"📧 Check the inbox: {test_parent_email}")
        print("\n🎯 Next Steps:")
        print(f"   1. Update .env file with: SENDER_PASSWORD={app_password}")
        print("   2. Restart EmpathyWave application")
        print("   3. Real emergency emails will now be sent!")
        
        # Update .env file
        update_env = input("\nUpdate .env file automatically? (y/n): ").lower().strip()
        if update_env == 'y':
            update_env_file(app_password)
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        
        if "authentication" in str(e).lower():
            print("\n🔧 Authentication failed. Solutions:")
            print("   • Make sure you're using Gmail App Password (not regular password)")
            print("   • Verify 2-Step Verification is enabled")
            print("   • App Password should be 16 characters with spaces")
        elif "username" in str(e).lower():
            print("\n🔧 Username/Password not accepted:")
            print("   • Use Gmail App Password instead of regular password")
            print("   • Enable 2-Factor Authentication first")

def update_env_file(app_password):
    """Update .env file with the working App Password"""
    try:
        # Read current .env
        with open('.env', 'r') as f:
            lines = f.readlines()
        
        # Update password line
        updated_lines = []
        for line in lines:
            if line.startswith('SENDER_PASSWORD='):
                updated_lines.append(f'SENDER_PASSWORD={app_password}\n')
            else:
                updated_lines.append(line)
        
        # Write updated .env
        with open('.env', 'w') as f:
            f.writelines(updated_lines)
            
        print("✅ .env file updated successfully!")
        print("🔄 Please restart the EmpathyWave application to apply changes.")
        
    except Exception as e:
        print(f"❌ Could not update .env file: {e}")
        print(f"Please manually update SENDER_PASSWORD={app_password} in .env")

if __name__ == "__main__":
    test_gmail_with_app_password()