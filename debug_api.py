#!/usr/bin/env python3
"""
Debug script to check the raw API response
"""
import requests

def debug_api_response():
    """Debug the API response to see what's wrong"""
    print("🔍 Debugging API Response")
    print("=" * 30)
    
    url = "http://127.0.0.1:5000/api/chat"
    test_data = {
        "message": "Hello, test message",
        "enable_voice": True
    }
    
    try:
        response = requests.post(url, json=test_data, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Raw Content: {response.text[:500]}...")
        
        if response.headers.get('content-type', '').startswith('application/json'):
            try:
                data = response.json()
                print(f"JSON Data: {data}")
            except Exception as e:
                print(f"JSON parsing failed: {e}")
        
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    debug_api_response()