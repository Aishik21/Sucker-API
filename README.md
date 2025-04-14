# Web Crawler API

A general-purpose web crawler API that uses LLM-powered content extraction and can be configured for various crawling tasks.

## Features

- Configurable web crawling with LLM-powered content extraction
- Asynchronous processing for better performance
- Data persistence with automatic backups
- REST API interface for easy integration
- Rate limiting and retry mechanisms
- Configurable through environment variables
- Comprehensive logging system
- Standalone scraping script for specific use cases

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your configuration:
```env
GEMINI_API_KEY=your_api_key_here
API_KEY=your_api_key_here
CRAWLER_HEADLESS=true
CRAWLER_VIEWPORT_WIDTH=1280
CRAWLER_VIEWPORT_HEIGHT=720
OUTPUT_DIR=output
MASTER_FILE=master.json
RATE_LIMIT_DELAY=2.0
MAX_RETRIES=3
```

4. Create necessary directories:
```bash
mkdir output logs
```

## Running the API

Start the API server:
```bash
uvicorn api.main:app --reload
```

The API will be available at `http://localhost:8000`

## Deployment

The API can be deployed for free on several platforms:

### Render
1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set the following environment variables:
   - `GEMINI_API_KEY`
   - `API_KEY`
   - `CRAWLER_HEADLESS=true`
   - `CRAWLER_VIEWPORT_WIDTH=1280`
   - `CRAWLER_VIEWPORT_HEIGHT=720`
   - `OUTPUT_DIR=/app/output`
   - `MASTER_FILE=master.json`
   - `RATE_LIMIT_DELAY=2.0`
   - `MAX_RETRIES=3`
4. Deploy!

### Railway
1. Create a new project on Railway
2. Connect your GitHub repository
3. Set the environment variables as above
4. Deploy!

### Heroku
1. Create a new app on Heroku
2. Connect your GitHub repository
3. Set the environment variables as above
4. Deploy!

### Fly.io
1. Install the Fly.io CLI
2. Run `fly launch`
3. Set the environment variables as above
4. Run `fly deploy`

## Standalone Scraping Script

The project includes a standalone scraping script (`scrape.py`) for specific use cases. To run it:

```bash
python scrape.py
```

This script uses the same core functionality as the API but is configured for specific scraping tasks.

## API Endpoints

### POST /crawl
Start a new crawling job.

Request body:
```json
{
    "urls": ["https://example.com"],
    "link_extraction_instruction": "Extract all links from the page",
    "content_extraction_instruction": "Extract the main content from the page",
    "max_depth": 5,
    "rate_limit_delay": 2.0
}
```

### GET /data
Retrieve all crawled data.

### GET /health
Check the API health status.

## Example Usage

```python
import requests

# Start a crawling job
response = requests.post(
    "http://localhost:8000/crawl",
    json={
        "urls": ["https://example.com"],
        "link_extraction_instruction": "Extract all links from the page",
        "content_extraction_instruction": "Extract the main content from the page"
    }
)

# Get crawled data
data = requests.get("http://localhost:8000/data").json()
```

## Configuration

The API can be configured through environment variables:

- `GEMINI_API_KEY`: Your Gemini API key
- `API_KEY`: Your API key for authentication
- `CRAWLER_HEADLESS`: Whether to run the browser in headless mode
- `CRAWLER_VIEWPORT_WIDTH`: Browser viewport width
- `CRAWLER_VIEWPORT_HEIGHT`: Browser viewport height
- `OUTPUT_DIR`: Directory to store crawled data
- `MASTER_FILE`: Name of the master data file
- `RATE_LIMIT_DELAY`: Delay between requests in seconds
- `MAX_RETRIES`: Maximum number of retries for failed requests

## Project Structure

```
.
├── api/
│   └── main.py           # FastAPI application
├── core/
│   ├── crawler.py        # Base crawler implementation
│   ├── config.py         # Configuration management
│   ├── processor.py      # Data processing utilities
│   └── logger.py         # Logging functionality
├── tests/
│   └── test_crawler.py   # Test cases
├── output/              # Directory for crawled data
├── logs/               # Directory for log files
├── scrape.py           # Standalone scraping script
├── requirements.txt    # Project dependencies
├── Dockerfile         # Docker configuration
├── docker-compose.yml # Docker Compose configuration
├── Procfile          # Heroku/Render configuration
└── README.md          # This file
``` 