#!/usr/bin/env python3
"""
Reset Emergency Alert History - For Testing Email System
This script clears recent emergency alerts so you can test email sending
"""

import sqlite3
from datetime import datetime, timedelta

def reset_emergency_alerts():
    """Clear recent emergency alerts for testing"""
    
    print("🔄 Resetting Emergency Alert History")
    print("=" * 50)
    
    try:
        # Connect to database
        conn = sqlite3.connect('empathy_wave.db')
        cursor = conn.cursor()
        
        # Check existing alerts
        cursor.execute("SELECT COUNT(*) FROM emergency_alerts")
        total_alerts = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM emergency_alerts WHERE created_at > datetime('now', '-6 hours')")
        recent_alerts = cursor.fetchone()[0]
        
        print(f"📊 Current Status:")
        print(f"   Total emergency alerts: {total_alerts}")
        print(f"   Recent alerts (last 6 hours): {recent_alerts}")
        print()
        
        if recent_alerts > 0:
            # Option 1: Delete all emergency alerts (complete reset)
            print("🗑️  Option 1: Delete ALL emergency alert history")
            print("   This will completely reset the emergency alert system")
            
            # Option 2: Mark old alerts as older (safer)
            print("⏰ Option 2: Mark recent alerts as 8 hours old (safer)")
            print("   This keeps history but allows new alerts to be sent")
            
            choice = input("\nChoose option (1/2): ").strip()
            
            if choice == "1":
                cursor.execute("DELETE FROM emergency_alerts")
                conn.commit()
                print("✅ All emergency alerts deleted")
                
            elif choice == "2":
                # Update timestamps to be 8 hours ago
                eight_hours_ago = (datetime.now() - timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute("UPDATE emergency_alerts SET created_at = ? WHERE created_at > datetime('now', '-6 hours')", 
                             (eight_hours_ago,))
                conn.commit()
                affected = cursor.rowcount
                print(f"✅ Updated {affected} recent alerts to be 8 hours old")
                
            else:
                print("❌ Invalid choice. No changes made.")
                return
                
        else:
            print("✅ No recent alerts found. Email system ready for testing!")
            
        conn.close()
        
        print("\n🚨 Emergency email system is now ready!")
        print("   Next suicide message will trigger a REAL email alert")
        print()
        print("🧪 To test:")
        print("   1. Go to: http://127.0.0.1:5000")
        print("   2. Login with your account")
        print("   3. Type: 'I want to kill myself'")
        print("   4. Check parent email for emergency alert")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure the EmpathyWave database exists and is accessible")

def show_current_alerts():
    """Show current emergency alerts"""
    try:
        conn = sqlite3.connect('empathy_wave.db')
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT user_id, risk_level, risk_score, created_at, email_sent_at 
            FROM emergency_alerts 
            ORDER BY created_at DESC 
            LIMIT 10
        """)
        
        alerts = cursor.fetchall()
        
        if alerts:
            print("\n📋 Recent Emergency Alerts:")
            print("-" * 80)
            for alert in alerts:
                user_id, risk_level, risk_score, created_at, email_sent_at = alert
                email_status = "✅ SENT" if email_sent_at else "❌ NOT SENT"
                print(f"User {user_id}: {risk_level} (score: {risk_score}) - {created_at} - {email_status}")
        else:
            print("\n📋 No emergency alerts found")
            
        conn.close()
        
    except Exception as e:
        print(f"❌ Error showing alerts: {e}")

if __name__ == "__main__":
    print("🚨 EmpathyWave Emergency Alert Reset Tool")
    print("=" * 50)
    print("This tool helps reset the emergency alert system for testing")
    print()
    
    # First show current status
    show_current_alerts()
    
    print("\n" + "=" * 50)
    reset_emergency_alerts()