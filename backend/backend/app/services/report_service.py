from datetime import datetime
from typing import List
from ..models import NewsArticle, ArticleAnalysis, StockAnalysisResponse

async def generate_report(
    ticker: str,
    articles: List[NewsArticle],
    analyses: List[ArticleAnalysis]
) -> StockAnalysisResponse:
    """Generate a comprehensive analysis report."""
    
    # Calculate overall sentiment score
    sentiment_scores = [analysis.sentiment_score for analysis in analyses]
    overall_score = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
    
    # Determine overall sentiment
    if overall_score >= 0.3:
        overall_sentiment = "positive"
    elif overall_score <= -0.3:
        overall_sentiment = "negative"
    else:
        overall_sentiment = "neutral"
    
    # Generate trading implications
    trading_implications = []
    if overall_sentiment == "positive":
        trading_implications.append(f"Strong positive sentiment suggests potential buying opportunity for {ticker}")
    elif overall_sentiment == "negative":
        trading_implications.append(f"Negative sentiment indicates caution advised for {ticker}")
    else:
        trading_implications.append(f"Neutral sentiment suggests monitoring {ticker} for clearer signals")
    
    # Add specific implications based on sentiment strength
    if abs(overall_score) > 0.7:
        trading_implications.append(f"Strong sentiment intensity suggests potential significant price movement for {ticker}")
    
    return StockAnalysisResponse(
        ticker=ticker,
        overall_sentiment=overall_sentiment,
        overall_sentiment_score=overall_score,
        articles=articles,
        analyses=analyses,
        trading_implications=trading_implications,
        timestamp=datetime.utcnow()
    )
