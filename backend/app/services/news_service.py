from typing import List, Dict, Any
import aiohttp
import os
from dotenv import load_dotenv
import asyncio
from datetime import datetime, timedelta

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_API_BASE_URL = "https://newsapi.org/v2/everything"

async def get_news_articles(ticker: str, days: int = 7) -> List[Dict[str, Any]]:
    """
    Fetch news articles for a given stock ticker from the News API.
    
    Args:
        ticker (str): Stock ticker symbol
        days (int): Number of days to look back for news articles
        
    Returns:
        List[Dict[str, Any]]: List of news articles
    """
    if not NEWS_API_KEY:
        raise ValueError("NEWS_API_KEY environment variable is not set")
        
    # Calculate date range (max 30 days)
    max_days = min(days, 30)
    from_date = (datetime.now() - timedelta(days=max_days)).strftime('%Y-%m-%d')
    
    params = {
        "q": ticker,
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "sortBy": "publishedAt",
        "from": from_date,
        "pageSize": 100  # Maximum allowed by News API
    }
    
    # Define whitelist of reputable sources with their variations
    WHITELISTED_SOURCES = {
        "bloomberg": ["bloomberg", "bloomberg.com", "bloomberg news"],
        "yahoo": ["yahoo", "yahoo finance", "yahoo news", "yahoo entertainment", "yahoo money"],
        "marketwatch": ["marketwatch", "market watch", "marketwatch.com"],
        "reuters": ["reuters", "reuters.com", "thomson reuters"],
        "cnbc": ["cnbc", "cnbc.com"],
        "wall street journal": ["wall street journal", "wsj", "wsj.com", "the wall street journal"]
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
                
                # Filter and sort articles
                all_articles = data["articles"]
                if not all_articles:
                    return []
                
                # Filter by whitelisted sources with flexible matching
                filtered_articles = []
                for article in all_articles:
                    source_name = article.get("source", {}).get("name", "").lower().strip()
                    source_domain = article.get("url", "").lower()
                    
                    # Debug logging
                    print(f"Checking source: {source_name} (URL: {source_domain})")
                    
                    # Check each main source and its variations with exact matching
                    for main_source, variations in WHITELISTED_SOURCES.items():
                        # Check exact source name match
                        if any(variation == source_name for variation in variations):
                            print(f"Matched source name {source_name} to {main_source}")
                            filtered_articles.append(article)
                            break
                        # Check domain match (extract domain from URL)
                        domain = source_domain.split("//")[-1].split("/")[0].lower()
                        if any(variation == domain or domain.endswith("." + variation) for variation in variations):
                            print(f"Matched domain {domain} to {main_source}")
                            filtered_articles.append(article)
                            break
                
                # Sort by published date
                filtered_articles.sort(key=lambda x: x.get("publishedAt", ""), reverse=True)
                
                print(f"Found {len(all_articles)} articles, {len(filtered_articles)} from whitelisted sources")
                return filtered_articles
                
    except asyncio.TimeoutError:
        raise Exception("Timeout while fetching news articles")
    except Exception as e:
        raise Exception(f"Failed to fetch news articles: {str(e)}")
