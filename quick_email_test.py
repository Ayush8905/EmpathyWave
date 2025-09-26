#!/usr/bin/env python3
"""
Quick Email Test - Try your current password first, then guide through App Password if needed
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

def quick_email_test():
    """Test email sending with current configuration"""
    
    print("🚨 EmpathyWave Emergency Email Test")
    print("=" * 50)
    
    sender_email = "omd23102004@gmail.com"
    sender_password = "qwertyuiop@123@"
    test_recipient = "omd23102004@gmail.com"  # Send to yourself for testing
    
    print(f"📧 From: {sender_email}")
    print(f"📧 To: {test_recipient}")
    print()
    
    # Create test email
    message = MIMEMultipart("alternative")
    message["Subject"] = "🚨 EmpathyWave Emergency Alert - SYSTEM TEST"
    message["From"] = f"EmpathyWave Emergency System <{sender_email}>"
    message["To"] = test_recipient
    
    # Simple HTML content
    html_content = """
    <html>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <div style="background: #ff4757; color: white; padding: 20px; text-align: center; border-radius: 10px;">
            <h1>🚨 EMERGENCY MENTAL HEALTH ALERT</h1>
            <h2>EmpathyWave Test Email</h2>
        </div>
        
        <div style="padding: 20px; background: #f8f9fa; margin: 20px 0; border-radius: 10px;">
            <h3>⚠️ This is a TEST of the emergency email system</h3>
            <p>If you receive this email, it means the EmpathyWave emergency alert system is working correctly!</p>
            
            <div style="background: #ffe6e6; padding: 15px; border-left: 4px solid #ff4757; margin: 20px 0;">
                <h4>In a real emergency, this email would contain:</h4>
                <ul>
                    <li>Crisis hotline numbers (988, 911)</li>
                    <li>Immediate action steps for parents</li>
                    <li>Mental health resources</li>
                    <li>Risk level and timestamp</li>
                </ul>
            </div>
            
            <div style="text-align: center; font-size: 24px; color: #ff4757; margin: 20px 0;">
                🆘 Crisis Hotline: 988
            </div>
        </div>
        
        <div style="text-align: center; font-size: 12px; color: #666; margin-top: 30px;">
            <p>EmpathyWave Mental Health Support System - Test Message</p>
            <p>🛡️ Protecting families with AI-powered mental health monitoring</p>
        </div>
    </body>
    </html>
    """
    
    # Attach content
    html_part = MIMEText(html_content, "html")
    message.attach(html_part)
    
    # Try sending with different methods
    methods = [
        ("Regular Gmail SMTP", "smtp.gmail.com", 587, True),
        ("Gmail SMTP without TLS", "smtp.gmail.com", 587, False),
        ("Gmail SMTP Port 465", "smtp.gmail.com", 465, True),
    ]
    
    for method_name, smtp_server, port, use_tls in methods:
        print(f"🔄 Trying: {method_name}")
        try:
            if port == 465:
                # Use SSL for port 465
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                    server.login(sender_email, sender_password)
                    server.sendmail(sender_email, test_recipient, message.as_string())
            else:
                # Use STARTTLS for port 587
                with smtplib.SMTP(smtp_server, port) as server:
                    if use_tls:
                        context = ssl.create_default_context()
                        server.starttls(context=context)
                    server.login(sender_email, sender_password)
                    server.sendmail(sender_email, test_recipient, message.as_string())
            
            print(f"✅ SUCCESS with {method_name}!")
            print(f"📧 Test email sent to {test_recipient}")
            print(f"📄 Check your inbox for the emergency alert test email")
            print()
            print("🎯 EMERGENCY EMAIL SYSTEM IS NOW WORKING!")
            print("   Real emergency emails will be sent when users express suicide risk.")
            return True
            
        except Exception as e:
            print(f"❌ Failed with {method_name}: {e}")
            continue
    
    # If all methods failed
    print("\n❌ All email methods failed. Gmail security is blocking the connection.")
    print("\n🔧 SOLUTION: Use Gmail App Password")
    print("=" * 50)
    print("1. Go to: https://myaccount.google.com/security")
    print("2. Enable '2-Step Verification' if not already enabled")
    print("3. Scroll down to 'App passwords'")
    print("4. Create new app password for 'EmpathyWave'")
    print("5. Use the 16-character password instead of your regular password")
    print()
    print("Then run: python setup_gmail_email.py")
    
    return False

if __name__ == "__main__":
    success = quick_email_test()
    
    if success:
        print("\n🛡️ Your EmpathyWave emergency email system is ready!")
        print("   When users type suicide messages, parents will receive immediate alerts.")
    else:
        print("\n💡 Need to set up Gmail App Password for security.")
        print("   Don't worry - it's a simple 5-minute process!")