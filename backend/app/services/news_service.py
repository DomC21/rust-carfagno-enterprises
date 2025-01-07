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
        
    params = {
        "q": ticker,
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
                
                # Filter and sort articles
                articles = data["articles"]
                if not articles:
                    return []
                
                # Sort by published date
                articles.sort(key=lambda x: x.get("publishedAt", ""), reverse=True)
                
                return articles[:10]  # Return only the 10 most recent articles
                
    except asyncio.TimeoutError:
        raise Exception("Timeout while fetching news articles")
    except Exception as e:
        raise Exception(f"Failed to fetch news articles: {str(e)}")
