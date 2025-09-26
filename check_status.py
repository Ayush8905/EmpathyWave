#!/usr/bin/env python3
"""
Quick Database Check - Emergency Alert Status
"""

import sqlite3
from datetime import datetime

def check_emergency_status():
    try:
        conn = sqlite3.connect('empathy_wave.db')
        cursor = conn.cursor()
        
        # Check current emergency alerts
        cursor.execute("SELECT COUNT(*) FROM emergency_alerts")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM emergency_alerts WHERE created_at > datetime('now', '-1 hour')")
        recent = cursor.fetchone()[0]
        
        print(f"🏥 Emergency Alert Status:")
        print(f"   Total alerts in database: {total}")
        print(f"   Recent alerts (last hour): {recent}")
        
        if recent == 0:
            print("✅ NO RECENT ALERTS - Email system ready!")
        else:
            print("⚠️  Recent alerts exist - may affect cooldown")
            
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_emergency_status()