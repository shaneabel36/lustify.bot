"""
Test script for Lustify Bot endpoints
"""

import requests
import json

# Base URL
BASE_URL = "http://localhost:5001"

def test_characters_endpoint():
    """Test the characters endpoint"""
    print("Testing /characters endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/characters")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_chat_endpoint():
    """Test the chat endpoint"""
    print("\nTesting /chat endpoint...")
    try:
        # Test with a simple message
        response = requests.post(
            f"{BASE_URL}/chat",
            headers={"Content-Type": "application/json"},
            json={"message": "Hello, how are you?"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_image_endpoint():
    """Test the image generation endpoint"""
    print("\nTesting /generate-image endpoint...")
    try:
        response = requests.post(
            f"{BASE_URL}/generate-image",
            headers={"Content-Type": "application/json"},
            json={"prompt": "A beautiful woman"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_other_endpoints():
    """Test other endpoints"""
    print("\nTesting other endpoints...")
    
    # Test new seed
    try:
        response = requests.post(f"{BASE_URL}/new-seed")
        print(f"/new-seed Status: {response.status_code}")
        print(f"/new-seed Response: {response.json()}")
    except Exception as e:
        print(f"/new-seed Error: {e}")
    
    # Test clear
    try:
        response = requests.post(f"{BASE_URL}/clear")
        print(f"/clear Status: {response.status_code}")
        print(f"/clear Response: {response.json()}")
    except Exception as e:
        print(f"/clear Error: {e}")

if __name__ == "__main__":
    print("=== Lustify Bot Endpoint Testing ===")
    
    # Test all endpoints
    test_characters_endpoint()
    test_chat_endpoint()
    test_image_endpoint()
    test_other_endpoints()
    
    print("\n=== Test Complete ===")