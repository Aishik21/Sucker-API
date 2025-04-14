import pytest
from core.crawler import BaseCrawler
from core.config import settings, get_browser_config, get_llm_config
from core.processor import DataProcessor

@pytest.mark.asyncio
async def test_crawler_initialization():
    browser_config = get_browser_config(settings)
    llm_config = get_llm_config(settings)
    
    async with BaseCrawler(
        browser_config=browser_config,
        llm_config=llm_config
    ) as crawler:
        assert crawler is not None
        assert crawler.crawler is not None

@pytest.mark.asyncio
async def test_config_creation():
    browser_config = get_browser_config(settings)
    llm_config = get_llm_config(settings)
    
    async with BaseCrawler(
        browser_config=browser_config,
        llm_config=llm_config
    ) as crawler:
        link_config = crawler.create_link_extractor_config(
            "Extract all links from the page"
        )
        assert link_config is not None
        
        content_config = crawler.create_content_extractor_config(
            "Extract the main content from the page"
        )
        assert content_config is not None

def test_data_processor():
    processor = DataProcessor()
    test_data = {"test": "data"}
    
    # Test saving data
    filepath = processor.save_data(test_data)
    assert filepath is not None
    
    # Test updating master file
    processor.update_master_file([test_data])
    
    # Test loading master file
    loaded_data = processor.load_master_file()
    assert len(loaded_data) > 0
    assert loaded_data[0] == test_data 