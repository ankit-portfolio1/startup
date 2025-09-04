#!/usr/bin/env python3
"""
Simple API test script to verify the Django REST API is working correctly.
Run this script to test the main API endpoints.
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000/api"

def test_endpoint(method, endpoint, data=None, headers=None, expected_status=200):
    """Test an API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method.upper() == "PUT":
            response = requests.put(url, json=data, headers=headers)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers)
        
        print(f"{method} {endpoint} - Status: {response.status_code}")
        
        if response.status_code == expected_status:
            print(f"✅ PASS")
            if response.content:
                try:
                    data = response.json()
                    print(f"   Response: {json.dumps(data, indent=2)[:200]}...")
                except:
                    print(f"   Response: {response.text[:200]}...")
        else:
            print(f"❌ FAIL - Expected {expected_status}, got {response.status_code}")
            print(f"   Error: {response.text[:200]}...")
        
        return response
        
    except requests.exceptions.ConnectionError:
        print(f"❌ FAIL - Could not connect to {url}")
        print("   Make sure the Django server is running on localhost:8000")
        return None
    except Exception as e:
        print(f"❌ FAIL - Error: {str(e)}")
        return None

def main():
    print("🧪 Testing Smart Laundry API")
    print("=" * 50)
    
    # Test 1: Check if server is running
    print("\n1. Testing server connectivity...")
    response = test_endpoint("GET", "/services/categories/")
    if not response:
        print("❌ Server is not running. Please start the Django server first:")
        print("   python manage.py runserver")
        sys.exit(1)
    
    # Test 2: Get service categories
    print("\n2. Testing service categories...")
    test_endpoint("GET", "/services/categories/")
    
    # Test 3: Get services
    print("\n3. Testing services...")
    test_endpoint("GET", "/services/services/")
    
    # Test 4: Get service options
    print("\n4. Testing service options...")
    test_endpoint("GET", "/services/options/")
    
    # Test 5: Get FAQs
    print("\n5. Testing FAQs...")
    test_endpoint("GET", "/core/faqs/")
    
    # Test 6: Get site configurations
    print("\n6. Testing site configurations...")
    test_endpoint("GET", "/core/config/")
    
    # Test 7: Get banners
    print("\n7. Testing banners...")
    test_endpoint("GET", "/core/banners/")
    
    # Test 8: Test user registration
    print("\n8. Testing user registration...")
    registration_data = {
        "email": "test@example.com",
        "phone": "+1234567890",
        "first_name": "Test",
        "last_name": "User",
        "password": "testpassword123",
        "password_confirm": "testpassword123"
    }
    response = test_endpoint("POST", "/auth/register/", data=registration_data, expected_status=201)
    
    # Test 9: Test user login
    print("\n9. Testing user login...")
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    response = test_endpoint("POST", "/auth/login/", data=login_data)
    
    if response and response.status_code == 200:
        try:
            login_response = response.json()
            access_token = login_response.get('tokens', {}).get('access')
            
            if access_token:
                headers = {"Authorization": f"Bearer {access_token}"}
                
                # Test 10: Get user profile
                print("\n10. Testing user profile...")
                test_endpoint("GET", "/auth/profile/", headers=headers)
                
                # Test 11: Get user dashboard
                print("\n11. Testing user dashboard...")
                test_endpoint("GET", "/auth/dashboard/", headers=headers)
                
                # Test 12: Get cart
                print("\n12. Testing cart...")
                test_endpoint("GET", "/orders/cart/", headers=headers)
                
                # Test 13: Add item to cart
                print("\n13. Testing add to cart...")
                cart_data = {
                    "service_id": 1,
                    "service_option_id": 1,
                    "quantity": 1
                }
                test_endpoint("POST", "/orders/cart/", data=cart_data, headers=headers, expected_status=201)
                
                # Test 14: Get cart summary
                print("\n14. Testing cart summary...")
                test_endpoint("GET", "/orders/cart/summary/", headers=headers)
                
        except Exception as e:
            print(f"❌ Error processing login response: {e}")
    
    # Test 15: Test contact form
    print("\n15. Testing contact form...")
    contact_data = {
        "name": "Test User",
        "email": "test@example.com",
        "subject": "Test Subject",
        "message": "This is a test message"
    }
    test_endpoint("POST", "/core/contact/", data=contact_data, expected_status=201)
    
    print("\n" + "=" * 50)
    print("🎉 API testing completed!")
    print("\nIf you see any ❌ FAIL messages above, check the Django server logs.")
    print("If all tests show ✅ PASS, your API is working correctly!")

if __name__ == "__main__":
    main()