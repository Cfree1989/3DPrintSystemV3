#!/usr/bin/env python3
"""
Test script for Sound Notification System
Tests that all sound notification components are properly integrated into the dashboard.
"""

import requests
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '3DPrintSystem'))

BASE_URL = 'http://localhost:5000'

def test_sound_notification_integration():
    """Test that sound notification components are present in dashboard"""
    print("🔊 TESTING SOUND NOTIFICATION SYSTEM")
    print("=" * 50)
    
    try:
        # Create a session for login persistence
        session = requests.Session()
        
        # Test staff login
        print("🔐 Testing staff login...")
        login_data = {'password': 'Fabrication'}
        login_response = session.post(f'{BASE_URL}/dashboard/login', data=login_data)
        
        if login_response.status_code != 200:
            print(f"❌ Login failed with status {login_response.status_code}")
            return False
        
        print("✅ Login successful!")
        
        # Test dashboard access and sound components
        print("📱 Testing dashboard sound notification features...")
        dashboard_response = session.get(f'{BASE_URL}/dashboard/')
        
        if dashboard_response.status_code != 200:
            print(f"❌ Dashboard access failed with status {dashboard_response.status_code}")
            return False
        
        dashboard_html = dashboard_response.text
        
        # Test for sound notification components
        sound_components = {
            'Sound Toggle Button': 'id="sound-toggle"',
            'Sound Icon': 'id="sound-icon"',
            'Sound Text': 'id="sound-text"',
            'SoundNotificationManager Class': 'class SoundNotificationManager',
            'Toggle Function': 'function toggleSoundNotifications()',
            'Sound Manager Instance': 'const soundManager',
            'Audio File URL': 'sounds/new-job.mp3',
            'New Job Detection': 'onNewJobDetected',
            'LocalStorage Persistence': 'soundNotificationsEnabled',
            'User Interaction Handling': 'userInteracted'
        }
        
        results = {}
        for component, search_text in sound_components.items():
            found = search_text in dashboard_html
            results[component] = found
            status = "✅" if found else "❌"
            print(f"  {status} {component}: {'Found' if found else 'Missing'}")
        
        # Test sound directory exists
        print("📂 Testing sound file directory...")
        try:
            sounds_response = session.get(f'{BASE_URL}/static/sounds/README.md')
            if sounds_response.status_code == 200:
                print("  ✅ Sound directory accessible")
                results['Sound Directory'] = True
            else:
                print("  ❌ Sound directory not accessible")
                results['Sound Directory'] = False
        except Exception as e:
            print(f"  ❌ Sound directory test failed: {e}")
            results['Sound Directory'] = False
        
        # Summary
        print("\n" + "=" * 50)
        print("🏁 SOUND NOTIFICATION TEST SUMMARY")
        total_components = len(results)
        passed_components = sum(results.values())
        
        print(f"Components tested: {total_components}")
        print(f"Components found: {passed_components}")
        print(f"Success rate: {(passed_components/total_components)*100:.1f}%")
        
        if passed_components == total_components:
            print("🎉 ALL SOUND NOTIFICATION TESTS PASSED!")
            return True
        else:
            print(f"⚠️ {total_components - passed_components} components missing")
            return False
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    success = test_sound_notification_integration()
    sys.exit(0 if success else 1) 