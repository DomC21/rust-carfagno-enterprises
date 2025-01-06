from typing import List, Dict, Any
import requests
import os
from dotenv import load_dotenv

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
        response = requests.get(NEWS_API_BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data["status"] != "ok":
            raise ValueError(f"News API error: {data.get('message', 'Unknown error')}")
            
        return data["articles"]
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch news articles: {str(e)}")
