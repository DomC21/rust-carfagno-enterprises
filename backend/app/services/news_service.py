from typing import List, Dict, Any
import aiohttp
import os
from dotenv import load_dotenv
import asyncio
from datetime import datetime, timedelta
import logging

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_API_BASE_URL = "https://newsapi.org/v2/everything"

# Whitelist of trusted financial news sources
WHITELISTED_SOURCES = {
    "bloomberg": ["bloomberg", "bloomberg.com", "bloomberg news"],
    "yahoo": ["yahoo finance", "finance.yahoo.com", "yahoo news"],
    "marketwatch": ["marketwatch", "marketwatch.com"],
    "reuters": ["reuters", "reuters.com", "thomson reuters"],
    "cnbc": ["cnbc", "cnbc.com"],
    "wall street journal": ["wall street journal", "wsj", "wsj.com"]
}

def is_whitelisted_source(source: Dict[str, Any]) -> bool:
    """Check if the article source is in the whitelist."""
    if not source:
        return False
    
    source_name = source.get("name", "").lower()
    source_domain = source.get("url", "").lower()
    
    for whitelist_variants in WHITELISTED_SOURCES.values():
        for variant in whitelist_variants:
            if variant in source_name or variant in source_domain:
                logging.info(f"Matched source: {source_name} ({source_domain}) with variant: {variant}")
                return True
    
    logging.info(f"Rejected source: {source_name} ({source_domain})")
    return False

async def get_news_articles(ticker: str, days: int = 30) -> List[Dict[str, Any]]:
    """
    Fetch news articles for a given stock ticker from the News API.
    
    Args:
        ticker (str): Stock ticker symbol
        days (int): Number of days to look back for news articles (default: 30)
        
    Returns:
        List[Dict[str, Any]]: List of filtered news articles from whitelisted sources
    """
    if not NEWS_API_KEY:
        raise ValueError("NEWS_API_KEY environment variable is not set")
    
    # Calculate date range
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    params = {
        "q": ticker,
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 100,  # Maximum allowed by News API
        "from": start_date.strftime("%Y-%m-%d"),
        "to": end_date.strftime("%Y-%m-%d")
    }
    
    try:
        async with aiohttp.ClientSession() as session: 
            async with session.get(NEWS_API_BASE_URL, params=params, timeout=30) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise ValueError(f"News API error: {error_text}")
                
                data = await response.json()
                
                if data["status"] != "ok":
                    raise ValueError(f"News API error: {data.get('message', 'Unknown error')}")
                
                # Filter articles by whitelisted sources and date range
                articles = []
                for article in data["articles"]:
                    published_at = datetime.fromisoformat(article["publishedAt"].replace("Z", "+00:00"))
                    if start_date <= published_at <= end_date and is_whitelisted_source(article["source"]):
                        articles.append(article)
                
                # Sort by published date
                articles.sort(key=lambda x: x["publishedAt"], reverse=True)
                
                logging.info(f"Found {len(articles)} articles from whitelisted sources")
                return articles
                
    except asyncio.TimeoutError:
        raise Exception("Timeout while fetching news articles")
    except Exception as e:
        raise Exception(f"Failed to fetch news articles: {str(e)}")
