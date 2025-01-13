from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime, timezone

class StockAnalysisRequest(BaseModel):
    ticker: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    
    @validator('start_date', 'end_date', pre=True)
    def ensure_timezone(cls, v):
        if v is None:
            return v
        if isinstance(v, datetime):
            return v.replace(tzinfo=timezone.utc) if v.tzinfo is None else v
        return v

class NewsArticle(BaseModel):
    title: str
    description: str
    url: str
    published_at: datetime
    source: str
    
    @validator('published_at', pre=True)
    def ensure_timezone(cls, v):
        if isinstance(v, datetime):
            return v.replace(tzinfo=timezone.utc) if v.tzinfo is None else v
        return v

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
    
    @validator('timestamp', pre=True)
    def ensure_timezone(cls, v):
        if isinstance(v, datetime):
            return v.replace(tzinfo=timezone.utc) if v.tzinfo is None else v
        return v
