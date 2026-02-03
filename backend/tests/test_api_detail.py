
import requests
import json

def test_policy_detail():
    url = "http://127.0.0.1:8000/api/policy/HOU_001"
    try:
        print(f"📡 Requesting: {url}")
        response = requests.get(url)
        print(f"📊 Status Code: {response.status_code}")
        
        try:
            data = response.json()
            print(f"📄 Response Body:\n{json.dumps(data, indent=2, ensure_ascii=False)}")
        except Exception as e:
            print(f"⚠️ Response not JSON: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    test_policy_detail()
