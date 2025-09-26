#!/usr/bin/env python3
"""
STEP-BY-STEP Gmail Setup for EmpathyWave Emergency Emails
"""

def show_setup_guide():
    print("🔐 Gmail App Password Setup for EmpathyWave")
    print("=" * 60)
    print()
    print("📧 Your Email: omd23102004@gmail.com")
    print("🎯 Goal: Send real emergency emails to parents")
    print()
    print("STEP 1: Enable 2-Factor Authentication")
    print("=" * 40)
    print("1. Go to: https://myaccount.google.com/security")
    print("2. Find '2-Step Verification' section")
    print("3. Click 'Get started' and follow the steps")
    print("4. Use your phone number for verification")
    print()
    print("STEP 2: Create App Password")
    print("=" * 40)
    print("1. Still on the Security page, scroll to 'App passwords'")
    print("2. Click 'App passwords' (you may need to sign in again)")
    print("3. Select 'Mail' as the app")
    print("4. Select 'Other (custom name)' as device")
    print("5. Type: 'EmpathyWave Emergency System'")
    print("6. Click 'Generate'")
    print("7. Copy the 16-character password (like: abcd efgh ijkl mnop)")
    print()
    print("STEP 3: Test the System")
    print("=" * 40)
    print("Run this command with your App Password:")
    print("  python test_app_password.py")
    print()
    print("💡 Why App Password?")
    print("   • More secure than regular passwords")
    print("   • Required by Gmail for automated systems")
    print("   • Allows EmpathyWave to send emergency emails safely")
    print()
    print("🚨 URGENT: Once set up, parents will receive REAL emails")
    print("   when users express suicide thoughts!")

if __name__ == "__main__":
    show_setup_guide()