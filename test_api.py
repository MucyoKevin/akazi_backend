#!/usr/bin/env python3
"""
Simple API test script for Akazi Backend
Run this after starting the Django server to test basic functionality
"""

import requests
import json

BASE_URL = "http://localhost:8000"
headers = {'Content-Type': 'application/json'}

def test_service_categories():
    """Test fetching service categories"""
    print("Testing service categories...")
    try:
        response = requests.get(f"{BASE_URL}/api/services/categories/")
        if response.status_code == 200:
            data = response.json()
            categories = data.get('results', data) if isinstance(data, dict) else data
            print(f"✅ Found {len(categories)} service categories")
            for cat in categories[:3]:  # Show first 3
                print(f"   - {cat['name']}: {cat['description'][:50]}...")
        else:
            print(f"❌ Failed to fetch categories: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_services():
    """Test fetching services"""
    print("\nTesting services...")
    try:
        response = requests.get(f"{BASE_URL}/api/services/")
        if response.status_code == 200:
            data = response.json()
            services = data.get('results', data) if isinstance(data, dict) else data
            print(f"✅ Found {len(services)} services")
            for service in services[:3]:  # Show first 3
                print(f"   - {service['name']}: RWF {service['base_price']}")
        else:
            print(f"❌ Failed to fetch services: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_featured_providers():
    """Test fetching featured providers"""
    print("\nTesting featured providers...")
    try:
        response = requests.get(f"{BASE_URL}/api/services/featured-providers/")
        if response.status_code == 200:
            providers = response.json()
            print(f"✅ Found {len(providers)} featured providers")
            for provider in providers[:3]:  # Show first 3
                print(f"   - {provider['user']['username']}: Rating {provider['rating']}")
        else:
            print(f"❌ Failed to fetch featured providers: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_user_registration():
    """Test user registration (without actually creating a user)"""
    print("\nTesting user registration endpoint availability...")
    try:
        # Test with invalid data to check if endpoint exists
        response = requests.post(f"{BASE_URL}/api/auth/register/", 
                               headers=headers, 
                               data=json.dumps({}))
        if response.status_code in [400, 422]:  # Bad request is expected
            print("✅ Registration endpoint is available")
        else:
            print(f"⚠️  Registration endpoint response: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_admin_access():
    """Test admin panel access"""
    print("\nTesting admin panel access...")
    try:
        response = requests.get(f"{BASE_URL}/admin/")
        if response.status_code == 200:
            print("✅ Admin panel is accessible")
        elif response.status_code == 302:
            print("✅ Admin panel is accessible (redirecting to login)")
        else:
            print(f"⚠️  Admin panel response: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("🧪 Testing Akazi Backend API")
    print("=" * 40)
    
    # Test basic endpoints
    test_service_categories()
    test_services()
    test_featured_providers()
    test_user_registration()
    test_admin_access()
    
    print("\n" + "=" * 40)
    print("🎉 API testing completed!")
    print("\n📋 Sample Test Users:")
    print("Customers: alice_customer, bob_customer")
    print("Providers: john_cleaner, marie_plumber, paul_electrician")
    print("Password: testpass123")
    print("\n🔗 Access the admin at: http://localhost:8000/admin/")

if __name__ == "__main__":
    main()
