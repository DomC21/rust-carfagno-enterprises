from typing import List, Dict, Any
import aiohttp
import os
from dotenv import load_dotenv
import asyncio
from datetime import datetime, timedelta
import logging

load_dotenv()

def setup_logging():
    """Configure logging for the news service."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

setup_logging()

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

def extract_domain(url: str) -> str:
    """Extract domain from URL, handling common formats."""
    if not url:
        return ""
    # Remove protocol and www
    domain = url.lower().replace("https://", "").replace("http://", "").replace("www.", "")
    # Get the domain part
    return domain.split("/")[0] if "/" in domain else domain

def is_whitelisted_source(source: Dict[str, Any]) -> bool:
    """Check if the article source is in the whitelist using strict matching."""
    if not source:
        logging.warning("Empty source object received")
        return False
    
    source_name = source.get("name", "").lower().strip()
    source_url = source.get("url", "").lower().strip()
    source_domain = extract_domain(source_url)
    
    logging.info(f"Checking source: {source_name} (URL: {source_url}, Domain: {source_domain})")
    
    # First check for exact source name matches
    for source_type, whitelist_variants in WHITELISTED_SOURCES.items():
        for variant in whitelist_variants:
            variant_lower = variant.lower().strip()
            
            # Exact name match
            if source_name == variant_lower:
                logging.info(f"Matched whitelisted source name: {source_name} ({source_type})")
                return True
            
            # Domain match
            variant_domain = extract_domain(variant_lower)
            if variant_domain and (source_domain == variant_domain):
                logging.info(f"Matched whitelisted domain: {source_domain} ({source_type})")
                return True
            
            # Partial name match for specific cases
            if (source_type == "bloomberg" and "bloomberg" in source_name) or \
               (source_type == "reuters" and "reuters" in source_name) or \
               (source_type == "cnbc" and "cnbc" in source_name) or \
               (source_type == "wall street journal" and ("wsj" in source_name or "wall street journal" in source_name)):
                logging.info(f"Matched whitelisted source pattern: {source_name} ({source_type})")
                return True
    
    logging.warning(f"Rejected non-whitelisted source: {source_name} ({source_url})")
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
                total_articles = len(data["articles"])
                logging.info(f"Processing {total_articles} articles for ticker {ticker}")
                
                for article in data["articles"]:
                    published_at = datetime.fromisoformat(article["publishedAt"].replace("Z", "+00:00"))
                    source = article["source"]
                    logging.info(f"Checking source: {source.get('name', 'Unknown')} ({source.get('url', 'No URL')})")
                    
                    if start_date <= published_at <= end_date:
                        if is_whitelisted_source(source):
                            articles.append(article)
                            logging.info(f"Added article from {source.get('name', 'Unknown')}")
                        else:
                            logging.info(f"Skipped article from non-whitelisted source: {source.get('name', 'Unknown')}")
                    else:
                        logging.info(f"Skipped article due to date range: {published_at}")
                
                # Sort by published date
                articles.sort(key=lambda x: x["publishedAt"], reverse=True)
                
                logging.info(f"Found {len(articles)} articles from whitelisted sources")
                return articles
                
    except asyncio.TimeoutError:
        raise Exception("Timeout while fetching news articles")
    except Exception as e:
        raise Exception(f"Failed to fetch news articles: {str(e)}")
