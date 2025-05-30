#!/usr/bin/env python3

import requests
import sys

def test_application():
    """Test all application components"""
    
    print("=== Application Testing ===")
    
    # Test 1: Basic pages
    try:
        resp = requests.get('http://localhost:5000/dashboard/login')
        print(f"Login page: {resp.status_code}")
        
        resp = requests.get('http://localhost:5000/submit')  
        print(f"Submit page: {resp.status_code}")
    except Exception as e:
        print(f"Basic pages: FAILED - {e}")
        return False
    
    # Test 2: Staff login workflow
    try:
        session = requests.Session()
        resp = session.post('http://localhost:5000/dashboard/login', 
                           data={'password': 'Fabrication'})
        print(f"Login POST: {resp.status_code}")
        
        if resp.status_code != 200:
            print("Login: FAILED - Wrong status code")
            return False
            
        resp = session.get('http://localhost:5000/dashboard/')
        print(f"Dashboard: {resp.status_code}")
        print(f"Dashboard size: {len(resp.text)} chars")
        
        # Test 3: Check modal elements
        html = resp.text
        modal_tests = {
            'approval-modal': 'approval-modal' in html,
            'rejection-modal': 'rejection-modal' in html, 
            'approval-form': 'approval-form' in html,
            'rejection-form': 'rejection-form' in html,
            'showApprovalModal': 'showApprovalModal' in html,
            'showRejectionModal': 'showRejectionModal' in html,
            'handleApprovalClick': 'handleApprovalClick' in html,
            'handleRejectionClick': 'handleRejectionClick' in html
        }
        
        print("\n=== Modal Elements ===")
        for test, result in modal_tests.items():
            status = "PASS" if result else "FAIL"
            print(f"{test}: {status}")
            
        # Test 4: CSS checks
        css_tests = {
            'modal_css': '#approval-modal, #rejection-modal' in html,
            'button_css': '.btn-approve' in html,
            'centering_css': 'display: flex' in html
        }
        
        print("\n=== CSS Tests ===") 
        for test, result in css_tests.items():
            status = "PASS" if result else "FAIL"
            print(f"{test}: {status}")
            
        # Test 5: API endpoints
        api_tests = {}
        try:
            resp = session.get('http://localhost:5000/dashboard/api/stats')
            api_tests['stats_api'] = resp.status_code == 200
        except:
            api_tests['stats_api'] = False
            
        print("\n=== API Tests ===")
        for test, result in api_tests.items():
            status = "PASS" if result else "FAIL" 
            print(f"{test}: {status}")
            
        # Overall result
        all_tests = list(modal_tests.values()) + list(css_tests.values()) + list(api_tests.values())
        passed = sum(all_tests)
        total = len(all_tests)
        
        print(f"\n=== Results ===")
        print(f"Passed: {passed}/{total}")
        print(f"Success rate: {passed/total*100:.1f}%")
        
        return passed == total
        
    except Exception as e:
        print(f"Dashboard workflow: FAILED - {e}")
        return False

if __name__ == "__main__":
    success = test_application()
    sys.exit(0 if success else 1) 