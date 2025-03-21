# test_news_scraper.py
import pytest
from news_scraper import fetch_news

def test_fetch_news():
    # Test with a valid company name
    result = fetch_news("Tesla")
    assert isinstance(result, list)
    assert all('title' in article and 'summary' in article for article in result)