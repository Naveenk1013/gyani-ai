import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_endpoint(endpoint, method="GET", data=None):
    """Test an API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data, headers={"Content-Type": "application/json"})
        
        print(f"Testing {method} {endpoint}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ SUCCESS")
            if response.content:
                try:
                    data = response.json()
                    print(f"Response: {json.dumps(data, indent=2)[:200]}...")
                except:
                    print(f"Response: {response.text[:200]}...")
        else:
            print("❌ FAILED")
            print(f"Error: {response.text}")
        
        print("-" * 50)
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print("-" * 50)
        return False

def test_all_endpoints():
    """Test all API endpoints"""
    print("🧪 Starting Gyani AI Backend Tests...")
    print("=" * 60)
    
    # Test basic endpoints
    test_endpoint("/")
    test_endpoint("/health")
    test_endpoint("/api/models")
    test_endpoint("/api/model-keys")
    
    # Test AI generation with different models
    test_prompts = [
        {
            "prompt": "Write a research abstract about renewable energy technologies",
            "model": "meta-llama/llama-3.1-405b-instruct"
        },
        {
            "prompt": "Write Python code to analyze climate data using pandas",
            "model": "qwen/qwen-2.5-coder-32b-instruct"
        },
        {
            "prompt": "Explain the scientific method in academic research",
            "model": "qwen/qwen-2.5-72b-instruct"
        }
    ]
    
    for i, test_data in enumerate(test_prompts, 1):
        print(f"🧪 Testing AI Generation #{i}")
        success = test_endpoint("/api/generate", "POST", test_data)
        if success:
            time.sleep(2)  # Rate limiting protection
    
    print("=" * 60)
    print("🎉 Backend Testing Complete!")

if __name__ == "__main__":
    test_all_endpoints()