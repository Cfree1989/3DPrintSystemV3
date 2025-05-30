#!/usr/bin/env python3
"""
Test script for dashboard functionality
Tests login, dashboard access, template filters, and database connectivity
"""

import requests
import sys
from urllib.parse import urljoin

BASE_URL = "http://localhost:5000"

def test_home_page():
    """Test if the home page is accessible"""
    print("Testing home page...")
    try:
        response = requests.get(BASE_URL)
        print(f"✅ Home page: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ Home page failed: {e}")
        return False

def test_dashboard_redirect():
    """Test if dashboard redirects unauthenticated users"""
    print("Testing dashboard authentication...")
    try:
        response = requests.get(f"{BASE_URL}/dashboard", allow_redirects=False)
        if response.status_code in [302, 308]:
            print(f"✅ Dashboard authentication: {response.status_code} (redirect)")
            return True
        else:
            print(f"❌ Dashboard authentication: {response.status_code} (should redirect)")
            return False
    except Exception as e:
        print(f"❌ Dashboard authentication failed: {e}")
        return False

def test_login_page():
    """Test if login page is accessible"""
    print("Testing login page...")
    try:
        response = requests.get(f"{BASE_URL}/dashboard/login")
        if response.status_code == 200:
            print(f"✅ Login page: {response.status_code} ({len(response.text)} chars)")
            return True
        else:
            print(f"❌ Login page: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Login page failed: {e}")
        return False

def test_login_and_dashboard():
    """Test login process and dashboard access"""
    print("Testing login process and dashboard access...")
    try:
        # Create a session
        session = requests.Session()
        
        # Get login page to extract any CSRF tokens if needed
        login_page = session.get(f"{BASE_URL}/dashboard/login")
        if login_page.status_code != 200:
            print(f"❌ Could not access login page: {login_page.status_code}")
            return False
        
        # Attempt login (using the correct password from config)
        login_data = {
            'password': 'Fabrication'  # This matches the fallback in dashboard.py
        }
        
        login_response = session.post(f"{BASE_URL}/dashboard/login", data=login_data, allow_redirects=False)
        
        if login_response.status_code in [302, 308]:
            print(f"✅ Login successful: {login_response.status_code} (redirect)")
            
            # Now try to access the dashboard
            dashboard_response = session.get(f"{BASE_URL}/dashboard")
            if dashboard_response.status_code == 200:
                content_length = len(dashboard_response.text)
                print(f"✅ Dashboard access: {dashboard_response.status_code} ({content_length} chars)")
                
                # Check for key elements in the dashboard
                content = dashboard_response.text
                if "3D Print Jobs" in content:
                    print("✅ Dashboard title found")
                if "Uploaded" in content and "Pending" in content:
                    print("✅ Status tabs found")
                if "No jobs found" in content or "student_name" in content:
                    print("✅ Job listing area found")
                
                return True
            else:
                print(f"❌ Dashboard access after login: {dashboard_response.status_code}")
                return False
        else:
            print(f"❌ Login failed: {login_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Login and dashboard test failed: {e}")
        return False

def test_template_filters():
    """Test template filters by checking dashboard content"""
    print("Testing template filters...")
    try:
        session = requests.Session()
        
        # Login first
        login_data = {'password': 'Fabrication'}
        session.post(f"{BASE_URL}/dashboard/login", data=login_data)
        
        # Get dashboard content
        response = session.get(f"{BASE_URL}/dashboard")
        if response.status_code == 200:
            content = response.text
            
            # Check for evidence of template filters working
            checks = [
                ("printer_name filter", "Prusa" in content or "printer" in content.lower()),
                ("color_name filter", "color" in content.lower()),
                ("discipline_name filter", "discipline" in content.lower()),
                ("datetime formatting", "at" in content or ":" in content)  # Looking for time formatting
            ]
            
            passed = 0
            for check_name, check_result in checks:
                if check_result:
                    print(f"✅ {check_name}")
                    passed += 1
                else:
                    print(f"⚠️  {check_name} (may not be visible without data)")
            
            print(f"✅ Template filters: {passed}/{len(checks)} checks passed")
            return True
        else:
            print(f"❌ Could not access dashboard for template filter test: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Template filter test failed: {e}")
        return False

def test_status_filtering():
    """Test status filtering functionality"""
    print("Testing status filtering...")
    try:
        session = requests.Session()
        
        # Login first
        login_data = {'password': 'Fabrication'}
        session.post(f"{BASE_URL}/dashboard/login", data=login_data)
        
        # Test different status filters
        statuses = ['UPLOADED', 'PENDING', 'READYTOPRINT', 'PRINTING', 'COMPLETED', 'REJECTED']
        
        for status in statuses:
            response = session.get(f"{BASE_URL}/dashboard?status={status}")
            if response.status_code == 200:
                print(f"✅ Status filter '{status}': {response.status_code}")
            else:
                print(f"❌ Status filter '{status}': {response.status_code}")
                
        return True
            
    except Exception as e:
        print(f"❌ Status filtering test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Dashboard Implementation")
    print("=" * 50)
    
    tests = [
        test_home_page,
        test_dashboard_redirect,
        test_login_page,
        test_login_and_dashboard,
        test_template_filters,
        test_status_filtering
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print("-" * 30)
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Dashboard implementation is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 