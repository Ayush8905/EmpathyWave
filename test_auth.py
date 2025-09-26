#!/usr/bin/env python3
"""
Test script for EmpathyWave authentication system
"""

import requests
import json

# Base URL for the Flask app
BASE_URL = "http://127.0.0.1:5000"

def test_authentication_system():
    """Test the complete authentication flow"""
    print("🔐 Testing EmpathyWave Authentication System...")
    
    # Test data
    test_user = {
        "email": "testuser@example.com",
        "password": "TestPassword123!",
        "parent_phone": "+1234567890",
        "parent_email": "parent@example.com"
    }
    
    session = requests.Session()
    
    try:
        # Test 1: Check if login page loads
        print("\n1. Testing login page access...")
        response = session.get(f"{BASE_URL}/login")
        if response.status_code == 200:
            print("✅ Login page accessible")
        else:
            print(f"❌ Login page failed with status: {response.status_code}")
            return
        
        # Test 2: Check if signup page loads
        print("\n2. Testing signup page access...")
        response = session.get(f"{BASE_URL}/signup")
        if response.status_code == 200:
            print("✅ Signup page accessible")
        else:
            print(f"❌ Signup page failed with status: {response.status_code}")
            return
        
        # Test 3: Test user registration
        print("\n3. Testing user registration...")
        response = session.post(f"{BASE_URL}/signup", data=test_user)
        if response.status_code == 200 or response.status_code == 302:
            print("✅ User registration successful")
        else:
            print(f"❌ User registration failed with status: {response.status_code}")
        
        # Test 4: Test user login
        print("\n4. Testing user login...")
        login_data = {
            "email": test_user["email"],
            "password": test_user["password"]
        }
        response = session.post(f"{BASE_URL}/login", data=login_data)
        if response.status_code == 200 or response.status_code == 302:
            print("✅ User login successful")
        else:
            print(f"❌ User login failed with status: {response.status_code}")
        
        # Test 5: Test protected route access
        print("\n5. Testing protected route access...")
        response = session.get(f"{BASE_URL}/chat")
        if response.status_code == 200:
            print("✅ Protected route accessible after login")
        else:
            print(f"❌ Protected route failed with status: {response.status_code}")
        
        # Test 6: Test logout
        print("\n6. Testing logout...")
        response = session.post(f"{BASE_URL}/logout")
        if response.status_code == 200 or response.status_code == 302:
            print("✅ Logout successful")
        else:
            print(f"❌ Logout failed with status: {response.status_code}")
        
        # Test 7: Test protected route access after logout
        print("\n7. Testing protected route access after logout...")
        response = session.get(f"{BASE_URL}/chat")
        if response.status_code == 302:  # Should redirect to login
            print("✅ Protected route properly redirects after logout")
        else:
            print(f"❌ Protected route security failed with status: {response.status_code}")
        
        print("\n🎉 Authentication system test completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the Flask application. Make sure it's running on http://127.0.0.1:5000")
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")

if __name__ == "__main__":
    test_authentication_system()