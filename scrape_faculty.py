import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Print environment variables for debugging
print("Environment variables:")
print(f"API_KEY from env: {os.getenv('API_KEY')}")
print(f"GEMINI_API_KEY from env: {os.getenv('GEMINI_API_KEY')}")

# API endpoint
API_URL = "http://localhost:8000"
API_KEY = "TuTu42021"  # Using the API key from your .env file

# Request headers
headers = {
    "Content-Type": "application/json",
    "X-API-Key": API_KEY
}

# Request payload
payload = {
    "urls": ["https://www.engineering.pitt.edu/programs/nuclear/faculty/"],
    "link_extraction_instruction": "Extract all faculty member links and profiles",
    "content_extraction_instruction": """Extract faculty member information in JSON format with the following fields:
        - name: Full name of the faculty member
        - title: Academic title and position
        - email: Email address if available
        - phone: Phone number if available
        - education: List of educational qualifications
        - research_interests: Research interests and areas of expertise""",
    "max_depth": 1,
    "rate_limit_delay": 2.0
}

print("Using API Key:", API_KEY)

# Make the API request
try:
    # First check if the API is running
    health_check = requests.get(f"{API_URL}/health")
    print(f"Health check response: {health_check.status_code}")
    print(f"Health check response text: {health_check.text}")
    
    if health_check.status_code == 200:
        print("API is running")
        
        # Make the crawl request
        response = requests.post(f"{API_URL}/crawl", json=payload, headers=headers)
        print(f"Crawl response status: {response.status_code}")
        print(f"Crawl response: {response.text}")
        
        if response.status_code == 200:
            # Get the crawled data
            data_response = requests.get(f"{API_URL}/data", headers=headers)
            if data_response.status_code == 200:
                data = data_response.json()
                # Save the data to a file
                with open("faculty_data.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                print("Faculty data has been saved to faculty_data.json")
            else:
                print(f"Error getting data: {data_response.status_code}")
                print(data_response.text)
        else:
            print(f"Error starting crawl: {response.status_code}")
            print(response.text)
    else:
        print("API is not running")
except requests.exceptions.ConnectionError:
    print("Could not connect to the API. Make sure the API server is running.") 