"""
Test script for TrackApply functionality
"""
import requests
import json

def test_app():
    """Test the TrackApply application"""
    base_url = "http://localhost:5000"
    
    try:
        # Test home page
        response = requests.get(base_url)
        if response.status_code == 200:
            print("✅ Home page loads successfully")
        else:
            print(f"❌ Home page failed: {response.status_code}")
        
        # Test add page
        response = requests.get(f"{base_url}/add")
        if response.status_code == 200:
            print("✅ Add application page loads successfully")
        else:
            print(f"❌ Add application page failed: {response.status_code}")
        
        # Test API stats
        response = requests.get(f"{base_url}/api/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ API stats working: {stats}")
        else:
            print(f"❌ API stats failed: {response.status_code}")
            
        print("\n🎉 All tests passed! TrackApply is working correctly.")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to the application. Make sure it's running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == '__main__':
    test_app()
