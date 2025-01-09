from typing import List, Dict, Any
import aiohttp
import os
from dotenv import load_dotenv
import asyncio
from datetime import datetime, timedelta, timezone
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
            
            # Domain match - only for specific domains
            if ".com" in variant_lower:  # Only match domains for .com variants
                variant_domain = extract_domain(variant_lower)
                if variant_domain and source_domain:
                    # Strict domain matching
                    if source_domain == variant_domain or source_domain.endswith("." + variant_domain):
                        logging.info(f"Matched whitelisted domain: {source_domain} ({source_type})")
                        return True
            
            # Strict partial name match for specific cases
            if source_type in ["bloomberg", "reuters", "cnbc", "wall street journal"]:
                if source_type == "bloomberg" and source_name.startswith("bloomberg"):
                    logging.info(f"Matched Bloomberg source: {source_name}")
                    return True
                elif source_type == "reuters" and source_name.startswith("reuters"):
                    logging.info(f"Matched Reuters source: {source_name}")
                    return True
                elif source_type == "cnbc" and source_name.startswith("cnbc"):
                    logging.info(f"Matched CNBC source: {source_name}")
                    return True
                elif source_type == "wall street journal" and (source_name.startswith("wsj") or source_name.startswith("wall street journal")):
                    logging.info(f"Matched Wall Street Journal source: {source_name}")
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
    
    # Calculate date range with timezone awareness
    end_date = datetime.now(timezone.utc)
    start_date = (end_date - timedelta(days=days)).replace(tzinfo=timezone.utc)
    
    # Format dates in ISO 8601 format for News API
    start_date_str = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_date_str = end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    logging.info(f"Date range: {start_date_str} to {end_date_str}")
    
    # Use formatted dates for News API request
    params = {
        "q": ticker,
        "from": start_date_str,  # ISO 8601 format for precise filtering
        "to": end_date_str,
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 100  # Maximum allowed by News API
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
                    try:
                        # Parse datetime with explicit UTC timezone
                        published_at_str = article["publishedAt"].replace("Z", "+00:00")
                        published_at = datetime.fromisoformat(published_at_str).replace(tzinfo=timezone.utc)
                        source = article["source"]
                        source_name = source.get('name', 'Unknown')
                        source_url = source.get('url', 'No URL')
                        
                        logging.info(f"Processing article from {source_name} ({source_url})")
                        logging.info(f"Published at: {published_at.isoformat()}")
                        
                        # All datetime objects are already timezone-aware, compare directly
                        if start_date <= published_at <= end_date:
                            if is_whitelisted_source(source):
                                articles.append(article)
                                logging.info(f"✓ Added article from whitelisted source: {source_name}")
                            else:
                                logging.warning(f"✗ Rejected article from non-whitelisted source: {source_name}")
                        else:
                            logging.info(f"✗ Skipped article outside date range: {published_at.isoformat()} (range: {start_date.isoformat()} to {end_date.isoformat()})")
                    except Exception as e:
                        logging.error(f"Error processing article: {str(e)}")
                        continue
                
                # Sort by published date
                articles.sort(key=lambda x: x["publishedAt"], reverse=True)
                
                logging.info(f"Found {len(articles)} articles from whitelisted sources")
                return articles
                
    except asyncio.TimeoutError:
        raise Exception("Timeout while fetching news articles")
    except Exception as e:
        raise Exception(f"Failed to fetch news articles: {str(e)}")
