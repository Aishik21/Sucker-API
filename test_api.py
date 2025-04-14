import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base URL for the API
BASE_URL = "http://localhost:8000"
API_KEY = "TuTu42021"  # Using the exact API key from .env file

print("\nEnvironment Variables:")
print(f"API_KEY: {API_KEY}")
print(f"GEMINI_API_KEY: {os.getenv('GEMINI_API_KEY')}")

def test_health():
    """Test the health endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print("Health Check Response:", response.json())

def test_crawl():
    """Test the crawl endpoint"""
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    print("\nCrawl Headers:", headers)
    data = {
        "urls": ["https://example.com"],
        "link_extraction_instruction": "Extract all links from the page",
        "content_extraction_instruction": "Extract the main content from the page",
        "max_depth": 1,
        "rate_limit_delay": 2.0
    }
    response = requests.post(f"{BASE_URL}/crawl", headers=headers, json=data)
    print("Crawl Response:", response.json())

def test_get_data():
    """Test the data endpoint"""
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    print("\nData Headers:", headers)
    response = requests.get(f"{BASE_URL}/data", headers=headers)
    print("Data Response:", response.json())

if __name__ == "__main__":
    print("Testing API endpoints...")
    print("\n1. Testing health endpoint:")
    test_health()
    
    print("\n2. Testing crawl endpoint:")
    test_crawl()
    
    print("\n3. Testing data endpoint:")
    test_get_data() 