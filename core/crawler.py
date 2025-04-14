from typing import Optional, Dict, Any, List
import asyncio
import logging
from datetime import datetime
from urllib.parse import urljoin
from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CrawlerRunConfig,
    CacheMode,
    LLMConfig,
    LLMContentFilter,
    DefaultMarkdownGenerator,
)

class BaseCrawler:
    def __init__(
        self,
        browser_config: Optional[BrowserConfig] = None,
        llm_config: Optional[LLMConfig] = None,
        cache_mode: CacheMode = CacheMode.BYPASS
    ):
        self.browser_config = browser_config or BrowserConfig(
            headless=True,
            java_script_enabled=True,
            viewport_width=1280,
            viewport_height=720
        )
        self.llm_config = llm_config
        self.cache_mode = cache_mode
        self.crawler = None
        self.logger = logging.getLogger(__name__)

    async def __aenter__(self):
        self.crawler = AsyncWebCrawler(config=self.browser_config)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.crawler:
            await self.crawler.close()

    async def crawl_url(
        self,
        url: str,
        run_config: CrawlerRunConfig,
        retries: int = 3
    ) -> Optional[str]:
        """Crawl a URL with retries."""
        for attempt in range(retries):
            try:
                result = await self.crawler.arun(
                    url=url,
                    config=run_config,
                    bypass_cache=True,
                    magic=True
                )
                if result.success:
                    self.logger.info(f"✅ Crawled {url}")
                    return result.markdown.fit_html
                else:
                    self.logger.warning(f"Attempt {attempt+1} failed for {url}: {result.error_message}")
            except Exception as e:
                self.logger.error(f"Exception crawling {url}: {e}")
            await asyncio.sleep(3 + attempt * 2)
        return None

    def create_link_extractor_config(
        self,
        instruction: str,
        chunk_token_threshold: int = 2000
    ) -> CrawlerRunConfig:
        """Create a configuration for extracting links."""
        link_filter = LLMContentFilter(
            llm_config=self.llm_config,
            instruction=instruction,
            chunk_token_threshold=chunk_token_threshold,
            verbose=True
        )

        link_generator = DefaultMarkdownGenerator(
            content_filter=link_filter,
            options={"ignore_links": False}
        )

        return CrawlerRunConfig(
            cache_mode=self.cache_mode,
            markdown_generator=link_generator,
        )

    def create_content_extractor_config(
        self,
        instruction: str,
        chunk_token_threshold: int = 5000
    ) -> CrawlerRunConfig:
        """Create a configuration for extracting content."""
        content_filter = LLMContentFilter(
            llm_config=self.llm_config,
            instruction=instruction,
            chunk_token_threshold=chunk_token_threshold,
            verbose=True
        )

        content_generator = DefaultMarkdownGenerator(
            content_filter=content_filter,
            options={"ignore_links": False}
        )

        return CrawlerRunConfig(
            cache_mode=self.cache_mode,
            markdown_generator=content_generator,
        ) 