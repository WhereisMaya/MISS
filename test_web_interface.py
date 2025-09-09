#!/usr/bin/env python3
"""
Test script for Mindseye web interface
"""

import requests
import json
import time

def test_web_interface():
    """Test the web interface endpoints."""
    base_url = "http://localhost:8080"
    
    print("🧪 Testing Mindseye Web Interface")
    print("=" * 50)
    
    try:
        # Test main page
        print("1. Testing main page...")
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Main page loads successfully")
        else:
            print(f"❌ Main page failed: {response.status_code}")
            return
        
        # Test stats endpoint
        print("2. Testing stats endpoint...")
        response = requests.get(f"{base_url}/api/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Stats loaded: {stats}")
        else:
            print(f"❌ Stats failed: {response.status_code}")
        
        # Test bubbles endpoint
        print("3. Testing bubbles endpoint...")
        response = requests.get(f"{base_url}/api/bubbles")
        if response.status_code == 200:
            bubbles = response.json()
            print(f"✅ Bubbles loaded: {len(bubbles)} bubbles found")
        else:
            print(f"❌ Bubbles failed: {response.status_code}")
        
        # Test files endpoint
        print("4. Testing files endpoint...")
        response = requests.get(f"{base_url}/api/files")
        if response.status_code == 200:
            files = response.json()
            print(f"✅ Files loaded: {len(files)} files found")
        else:
            print(f"❌ Files failed: {response.status_code}")
        
        # Test log endpoint
        print("5. Testing log endpoint...")
        response = requests.get(f"{base_url}/api/log")
        if response.status_code == 200:
            log_data = response.text
            print(f"✅ Log loaded: {len(log_data)} characters")
        else:
            print(f"❌ Log failed: {response.status_code}")
        
        print("\n🎉 All tests completed!")
        print(f"🌐 Web interface is running at: {base_url}")
        print("📱 Open your browser and navigate to the URL above")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to web server")
        print("💡 Make sure the server is running: python mindseye_cli.py serve")
    except Exception as e:
        print(f"❌ Error testing web interface: {e}")

if __name__ == "__main__":
    test_web_interface()
