import requests
import json

def test_health():
    response = requests.get('http://localhost:8000/health')
    print("Health check response:", response.json())

def test_crawl():
    headers = {
        'api-key': 'test_api_key_123',
        'Content-Type': 'application/json'
    }
    
    data = {
        'urls': ['https://example.com'],
        'link_extraction_instruction': 'Extract all links from the page',
        'content_extraction_instruction': 'Extract the main content from the page'
    }
    
    response = requests.post('http://localhost:8000/crawl', headers=headers, json=data)
    print("Crawl response:", response.json())

if __name__ == '__main__':
    print("Testing health endpoint...")
    test_health()
    print("\nTesting crawl endpoint...")
    test_crawl() 