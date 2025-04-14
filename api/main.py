from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio
import logging
from datetime import datetime

from core.crawler import BaseCrawler
from core.config import settings, get_browser_config, get_llm_config
from core.processor import DataProcessor
from core.logger import setup_logger

# Setup logging
logger = setup_logger()

# Initialize FastAPI app
app = FastAPI(
    title="Web Crawler API",
    description="A general-purpose web crawler API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# API Key security
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != settings.API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Invalid API key"
        )
    return api_key

class CrawlRequest(BaseModel):
    urls: List[str]
    link_extraction_instruction: str
    content_extraction_instruction: str
    max_depth: int = 5
    rate_limit_delay: float = 2.0

class CrawlResponse(BaseModel):
    success: bool
    message: str
    data: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None

@app.post("/crawl", response_model=CrawlResponse)
@limiter.limit("5/minute")
async def crawl(
    request: Request,
    crawl_request: CrawlRequest,
    api_key: str = Depends(get_api_key)
):
    try:
        processor = DataProcessor()
        all_data = processor.load_master_file()
        
        browser_config = get_browser_config(settings)
        llm_config = get_llm_config(settings)
        
        async with BaseCrawler(
            browser_config=browser_config,
            llm_config=llm_config,
            cache_mode=settings.CRAWLER_CACHE_MODE
        ) as crawler:
            link_config = crawler.create_link_extractor_config(
                crawl_request.link_extraction_instruction
            )
            content_config = crawler.create_content_extractor_config(
                crawl_request.content_extraction_instruction
            )
            
            for url in crawl_request.urls:
                try:
                    html_content = await crawler.crawl_url(url, link_config)
                    if html_content:
                        extracted_data = {"url": url, "content": html_content}
                        all_data.append(extracted_data)
                        processor.save_data(extracted_data)
                        processor.update_master_file(all_data)
                        await asyncio.sleep(crawl_request.rate_limit_delay)
                except Exception as e:
                    logger.error(f"Error crawling {url}: {str(e)}")
                    continue
        
        processor.create_backup(all_data)
        
        return CrawlResponse(
            success=True,
            message=f"Successfully crawled {len(crawl_request.urls)} URLs",
            data=all_data
        )
        
    except Exception as e:
        logger.error(f"Error during crawling: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error during crawling: {str(e)}"
        )

@app.get("/data", response_model=List[Dict[str, Any]])
@limiter.limit("10/minute")
async def get_data(request: Request, api_key: str = Depends(get_api_key)):
    processor = DataProcessor()
    return processor.load_master_file()

@app.get("/debug/settings")
async def debug_settings():
    return {
        "api_key": settings.API_KEY,
        "gemini_api_key": settings.GEMINI_API_KEY
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    } 