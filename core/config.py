import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from crawl4ai import LLMConfig, BrowserConfig, CacheMode

class Settings(BaseSettings):
    # API Keys
    GEMINI_API_KEY: str = Field(..., env="GEMINI_API_KEY")
    API_KEY: str = Field(..., env="API_KEY")  # For API authentication
    
    # Crawler Settings
    CRAWLER_HEADLESS: bool = Field(True, env="CRAWLER_HEADLESS")
    CRAWLER_VIEWPORT_WIDTH: int = Field(1280, env="CRAWLER_VIEWPORT_WIDTH")
    CRAWLER_VIEWPORT_HEIGHT: int = Field(720, env="CRAWLER_VIEWPORT_HEIGHT")
    CRAWLER_CACHE_MODE: CacheMode = Field(CacheMode.BYPASS, env="CRAWLER_CACHE_MODE")
    
    # Output Settings
    OUTPUT_DIR: str = Field("output", env="OUTPUT_DIR")
    MASTER_FILE: str = Field("master.json", env="MASTER_FILE")
    
    # Rate Limiting
    RATE_LIMIT_DELAY: float = Field(2.0, env="RATE_LIMIT_DELAY")
    MAX_RETRIES: int = Field(3, env="MAX_RETRIES")

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()

def get_browser_config(settings: Settings) -> BrowserConfig:
    """Create browser configuration from settings."""
    return BrowserConfig(
        headless=settings.CRAWLER_HEADLESS,
        viewport_width=settings.CRAWLER_VIEWPORT_WIDTH,
        viewport_height=settings.CRAWLER_VIEWPORT_HEIGHT,
    )

def get_llm_config(settings: Settings) -> LLMConfig:
    """Create LLM configuration from settings."""
    return LLMConfig(
        api_key=settings.GEMINI_API_KEY,
        model="gemini-pro",
        temperature=0.3,
        max_output_tokens=2048,
    ) 