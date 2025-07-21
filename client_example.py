import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print("Health Check:", response.json())
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API. Make sure the server is running.")
        return False

def process_field(field_type: str, value: str, system_instructions: str = None):
    """Process a field using the API"""
    payload = {
        "field_type": field_type,
        "value": value
    }
    
    if system_instructions:
        payload["system_instructions"] = system_instructions
    
    try:
        response = requests.post(f"{BASE_URL}/process", json=payload)
        if response.status_code == 200:
            result = response.json()
            #print(f"\nProcessing: {field_type} = '{value}'")
            print(f"Field: {field_type}, Value: {value}, Result: {result['result']}")
            return result
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API. Make sure the server is running.")
        return None

def main():
    """Example usage of the API"""
    print("Agentic Agent API Client Example")
    print("=" * 40)
    
    # Test health first
    if not test_health():
        return
    
    # Example 1: Process an email address
    print("\n" + "=" * 40)
    process_field("Email Address", "pleaseformatme @gmail..com")
    
    # Example 2: Process a state
    print("\n" + "=" * 40)
    process_field("Email Address", "agent _projectQgmail.co")
    
    # Example 3: Process with custom instructions
    print("\n" + "=" * 40)
    process_field("State", "Wl")
    process_field("State", "CO v")


if __name__ == "__main__":
    main() 