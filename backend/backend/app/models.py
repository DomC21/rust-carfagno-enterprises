from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class StockAnalysisRequest(BaseModel):
    ticker: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class NewsArticle(BaseModel):
    title: str
    description: str
    url: str
    published_at: datetime
    source: str

class ArticleAnalysis(BaseModel):
    summary: str
    sentiment: str
    sentiment_score: float
    key_takeaways: List[str]
    significant_quotes: List[str]

class StockAnalysisResponse(BaseModel):
    ticker: str
    overall_sentiment: str
    overall_sentiment_score: float
    articles: List[NewsArticle]
    analyses: List[ArticleAnalysis]
    trading_implications: List[str]
    timestamp: datetime
