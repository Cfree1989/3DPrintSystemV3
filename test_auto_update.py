#!/usr/bin/env python3
"""
Test script for auto-updating dashboard functionality
"""

import requests
import json
import time
from datetime import datetime

# Base URL for the application
BASE_URL = 'http://localhost:5000'

def test_login():
    """Test staff login functionality"""
    print("🔐 Testing staff login...")
    
    session = requests.Session()
    
    # Get login page first
    login_page = session.get(f'{BASE_URL}/dashboard/login')
    print(f"Login page status: {login_page.status_code}")
    
    # Attempt login
    login_data = {'password': 'Fabrication'}
    login_response = session.post(f'{BASE_URL}/dashboard/login', data=login_data)
    print(f"Login response status: {login_response.status_code}")
    
    # Check if redirected to dashboard
    dashboard_response = session.get(f'{BASE_URL}/dashboard/')
    print(f"Dashboard access status: {dashboard_response.status_code}")
    
    if dashboard_response.status_code == 200 and 'Staff Dashboard' in dashboard_response.text:
        print("✅ Login successful!")
        return session
    else:
        print("❌ Login failed!")
        return None

def test_api_stats(session):
    """Test the auto-updating API stats endpoint"""
    print("\n📊 Testing API stats endpoint...")
    
    try:
        response = session.get(f'{BASE_URL}/dashboard/api/stats')
        print(f"API Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("✅ API returned valid JSON")
                print(f"API Success: {data.get('success')}")
                
                # Test stats structure
                stats = data.get('stats', {})
                expected_keys = ['uploaded', 'pending', 'ready', 'printing', 'completed', 'paidpickedup', 'rejected']
                print(f"Stats keys: {list(stats.keys())}")
                
                for key in expected_keys:
                    if key in stats:
                        print(f"  ✅ {key}: {stats[key]}")
                    else:
                        print(f"  ❌ Missing key: {key}")
                
                # Test jobs data
                jobs = data.get('jobs', [])
                print(f"Jobs count: {len(jobs)}")
                if jobs:
                    job_keys = jobs[0].keys() if jobs else []
                    print(f"Job data keys: {list(job_keys)}")
                
                print(f"Current status: {data.get('current_status')}")
                print(f"Timestamp: {data.get('timestamp')}")
                
                return True
                
            except json.JSONDecodeError:
                print("❌ API response is not valid JSON")
                print(f"Response preview: {response.text[:200]}")
                return False
        else:
            print(f"❌ API returned status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing API: {str(e)}")
        return False

def test_mark_reviewed(session):
    """Test the mark as reviewed functionality"""
    print("\n👁️ Testing mark as reviewed API...")
    
    # First get some jobs to test with
    response = session.get(f'{BASE_URL}/dashboard/api/stats')
    if response.status_code == 200:
        data = response.json()
        jobs = data.get('jobs', [])
        
        if jobs:
            test_job_id = jobs[0]['id']
            print(f"Testing with job ID: {test_job_id[:8]}...")
            
            # Test mark as reviewed
            mark_response = session.post(f'{BASE_URL}/dashboard/api/mark-reviewed/{test_job_id}')
            print(f"Mark reviewed status: {mark_response.status_code}")
            
            if mark_response.status_code == 200:
                try:
                    result = mark_response.json()
                    print(f"Mark reviewed success: {result.get('success')}")
                    print(f"Message: {result.get('message')}")
                    return True
                except:
                    print("❌ Invalid JSON response")
                    return False
            else:
                print(f"❌ Failed to mark as reviewed")
                return False
        else:
            print("ℹ️ No jobs available to test mark as reviewed")
            return True
    else:
        print("❌ Could not get jobs for testing")
        return False

def test_dashboard_html():
    """Test dashboard HTML contains auto-updating JavaScript"""
    print("\n📱 Testing dashboard HTML for auto-update features...")
    
    session = test_login()
    if not session:
        return False
    
    dashboard_response = session.get(f'{BASE_URL}/dashboard/')
    if dashboard_response.status_code == 200:
        html = dashboard_response.text
        
        # Check for auto-update features
        features = {
            'Last updated indicator': 'id="last-updated"',
            'Auto-update JavaScript': 'updateDashboard()',
            'Polling interval': 'POLL_INTERVAL',
            'Job age calculation': 'calculateJobAge',
            'Mark as reviewed function': 'markAsReviewed',
            'Visual alert styling': 'unreviewed-job',
            'NEW badge': 'new-badge'
        }
        
        for feature_name, search_text in features.items():
            if search_text in html:
                print(f"  ✅ {feature_name}: Found")
            else:
                print(f"  ❌ {feature_name}: Missing")
        
        return True
    else:
        print("❌ Could not access dashboard")
        return False

def test_job_details(session):
    """Test the specific job details and formatting in API response"""
    print("\n🔍 Testing detailed job data and formatting...")
    
    try:
        response = session.get(f'{BASE_URL}/dashboard/api/stats')
        if response.status_code == 200:
            data = response.json()
            jobs = data.get('jobs', [])
            
            if jobs:
                job = jobs[0]  # Test first job
                print(f"📋 Sample job details:")
                print(f"  ID: {job.get('id', 'N/A')[:8]}...")
                print(f"  Student: {job.get('student_name', 'N/A')}")
                print(f"  Email: {job.get('student_email', 'N/A')}")
                print(f"  Discipline: {job.get('discipline', 'N/A')}")
                print(f"  Class: {job.get('class_number', 'N/A')}")
                print(f"  Printer: {job.get('printer', 'N/A')}")
                print(f"  Color: {job.get('color', 'N/A')}")
                print(f"  Material: {job.get('material', 'N/A')}")
                print(f"  Cost: ${job.get('cost_usd', 'N/A')}")
                print(f"  Created: {job.get('created_at', 'N/A')}")
                print(f"  Display name: {job.get('display_name', 'N/A')}")
                print(f"  Original filename: {job.get('original_filename', 'N/A')}")
                print(f"  Staff viewed: {job.get('staff_viewed_at', 'N/A')}")
                
                # Test if all expected fields are present
                expected_fields = ['id', 'student_name', 'student_email', 'discipline', 'class_number', 
                                 'printer', 'color', 'material', 'created_at', 'display_name', 'original_filename']
                missing_fields = [field for field in expected_fields if field not in job]
                if missing_fields:
                    print(f"  ❌ Missing fields: {missing_fields}")
                else:
                    print(f"  ✅ All expected fields present")
                
                return True
            else:
                print("  ℹ️ No jobs available for testing")
                return True
        else:
            print(f"  ❌ API returned status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ Error testing job details: {str(e)}")
        return False

def main():
    """Run all auto-update tests"""
    print("🧪 TESTING AUTO-UPDATING DASHBOARD FUNCTIONALITY")
    print("=" * 50)
    
    start_time = datetime.now()
    
    # Test login
    session = test_login()
    if not session:
        print("\n❌ Cannot proceed without login")
        return
    
    # Test API stats
    api_success = test_api_stats(session)
    
    # Test mark as reviewed
    mark_success = test_mark_reviewed(session)
    
    # Test dashboard HTML
    html_success = test_dashboard_html()
    
    # Test job details
    job_details_success = test_job_details(session)
    
    # Summary
    print("\n" + "=" * 50)
    print("🏁 TEST SUMMARY")
    print(f"Login: ✅ Success")
    print(f"API Stats: {'✅ Success' if api_success else '❌ Failed'}")
    print(f"Mark Reviewed: {'✅ Success' if mark_success else '❌ Failed'}")
    print(f"Dashboard HTML: {'✅ Success' if html_success else '❌ Failed'}")
    print(f"Job Details: {'✅ Success' if job_details_success else '❌ Failed'}")
    
    end_time = datetime.now()
    print(f"Test duration: {(end_time - start_time).total_seconds():.2f} seconds")
    
    if all([api_success, mark_success, html_success, job_details_success]):
        print("\n🎉 ALL AUTO-UPDATE TESTS PASSED!")
    else:
        print("\n⚠️ Some tests failed. Check output above.")

if __name__ == '__main__':
    main() 