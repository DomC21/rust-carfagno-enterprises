from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import uuid4

def serialize_datetime(dt: datetime) -> str:
    """Convert datetime to ISO format string."""
    return dt.isoformat()

class StockRequest(BaseModel):
    ticker: str
    company_name: Optional[str] = None

class Article(BaseModel):
    title: str
    url: str
    source: str
    published_at: datetime
    content: str
    sentiment: Optional[float] = None
    summary: Optional[str] = None
    key_takeaways: Optional[List[str]] = None
    significant_quotes: Optional[List[str]] = None

    def dict(self, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        d['published_at'] = serialize_datetime(d['published_at'])
        return d

class AnalysisResponse(BaseModel):
    analysis_id: str = Field(default_factory=lambda: str(uuid4()))
    ticker: str
    company_name: Optional[str]
    articles: List[Article]
    summaries: List[str]
    sentiment_scores: List[float]
    overall_sentiment: float
    key_takeaways: List[str]
    significant_quotes: List[str]
    analysis_timestamp: datetime = Field(default_factory=datetime.now)

    def dict(self, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        d['analysis_timestamp'] = serialize_datetime(d['analysis_timestamp'])
        return d
