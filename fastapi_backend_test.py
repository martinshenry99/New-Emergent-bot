#!/usr/bin/env python3
"""
FastAPI Backend Testing
Testing the actual FastAPI backend endpoints
"""

import requests
import json
import os
from pathlib import Path

class FastAPIBackendTester:
    def __init__(self):
        # Get backend URL from frontend .env
        frontend_env_path = Path("/app/frontend/.env")
        self.backend_url = "https://orca-meme-bot.preview.emergentagent.com"
        
        if frontend_env_path.exists():
            with open(frontend_env_path, 'r') as f:
                for line in f:
                    if line.startswith('REACT_APP_BACKEND_URL='):
                        self.backend_url = line.split('=')[1].strip()
                        break
        
        print(f"🌐 Testing backend at: {self.backend_url}")
        
    def test_root_endpoint(self):
        """Test the root API endpoint"""
        try:
            response = requests.get(f"{self.backend_url}/api/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("message") == "Hello World":
                    print("✅ Root endpoint (/api/): WORKING")
                    return True
                else:
                    print(f"❌ Root endpoint: Unexpected response: {data}")
                    return False
            else:
                print(f"❌ Root endpoint: HTTP {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Root endpoint: Error - {e}")
            return False
    
    def test_get_status_endpoint(self):
        """Test GET /api/status endpoint"""
        try:
            response = requests.get(f"{self.backend_url}/api/status", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    print(f"✅ GET /api/status: WORKING (returned {len(data)} items)")
                    return True
                else:
                    print(f"❌ GET /api/status: Expected list, got {type(data)}")
                    return False
            else:
                print(f"❌ GET /api/status: HTTP {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ GET /api/status: Error - {e}")
            return False
    
    def test_post_status_endpoint(self):
        """Test POST /api/status endpoint"""
        try:
            test_data = {
                "client_name": "test_client_review_verification"
            }
            
            response = requests.post(
                f"{self.backend_url}/api/status", 
                json=test_data,
                timeout=10,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("client_name") == test_data["client_name"] and "id" in data and "timestamp" in data:
                    print("✅ POST /api/status: WORKING")
                    return True
                else:
                    print(f"❌ POST /api/status: Unexpected response structure: {data}")
                    return False
            else:
                print(f"❌ POST /api/status: HTTP {response.status_code}")
                print(f"   Response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ POST /api/status: Error - {e}")
            return False
    
    def test_database_connectivity(self):
        """Test database connectivity by creating and retrieving a status check"""
        try:
            # Create a status check
            test_data = {
                "client_name": "database_connectivity_test"
            }
            
            post_response = requests.post(
                f"{self.backend_url}/api/status", 
                json=test_data,
                timeout=10
            )
            
            if post_response.status_code != 200:
                print("❌ Database connectivity: Failed to create status check")
                return False
            
            created_item = post_response.json()
            
            # Retrieve all status checks
            get_response = requests.get(f"{self.backend_url}/api/status", timeout=10)
            
            if get_response.status_code != 200:
                print("❌ Database connectivity: Failed to retrieve status checks")
                return False
            
            all_items = get_response.json()
            
            # Check if our created item is in the list
            found_item = None
            for item in all_items:
                if item.get("id") == created_item.get("id"):
                    found_item = item
                    break
            
            if found_item:
                print("✅ Database connectivity: WORKING")
                return True
            else:
                print("❌ Database connectivity: Created item not found in database")
                return False
                
        except Exception as e:
            print(f"❌ Database connectivity: Error - {e}")
            return False
    
    def run_backend_tests(self):
        """Run all backend tests"""
        print("🚀 TESTING FASTAPI BACKEND...")
        print("=" * 40)
        
        tests = [
            ("Root Endpoint", self.test_root_endpoint),
            ("GET Status Endpoint", self.test_get_status_endpoint),
            ("POST Status Endpoint", self.test_post_status_endpoint),
            ("Database Connectivity", self.test_database_connectivity)
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test_name, test_method in tests:
            print(f"\n🔍 Testing {test_name}...")
            try:
                if test_method():
                    passed_tests += 1
            except Exception as e:
                print(f"❌ {test_name}: Exception - {e}")
        
        print(f"\n📊 BACKEND TEST RESULTS:")
        print(f"✅ Passed: {passed_tests}/{total_tests}")
        print(f"📈 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if passed_tests == total_tests:
            print("🎉 ALL BACKEND TESTS PASSED!")
        else:
            print("⚠️ Some backend tests failed")
        
        return passed_tests == total_tests

def main():
    tester = FastAPIBackendTester()
    success = tester.run_backend_tests()
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)