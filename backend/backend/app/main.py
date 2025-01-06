from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from app.models import StockAnalysisRequest, StockAnalysisResponse, NewsArticle
from app.services.news_service import get_news_articles
from app.services.analysis_service import analyze_articles
from app.services.report_service import generate_report
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Rust: A Tool by Carfagno Enterprises")

@app.get("/health")
async def health_check():
    return Response(status_code=200)

# Configure CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Configured via environment variable
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Rust: A Tool by Carfagno Enterprises"}

@app.post("/analyze", response_model=StockAnalysisResponse)
async def analyze_stock(request: StockAnalysisRequest):
    try:
        # Fetch news articles
        raw_articles = await get_news_articles(request.ticker)
        
        if not raw_articles:
            raise HTTPException(status_code=404, detail="No news articles found for the given ticker")
            
        # Convert raw articles to NewsArticle objects
        from datetime import datetime
        articles = []
        for article in raw_articles:
            try:
                published_at = datetime.strptime(
                    article.get("publishedAt", ""), 
                    "%Y-%m-%dT%H:%M:%SZ"
                )
                articles.append(
                    NewsArticle(
                        title=article.get("title", "No title"),
                        description=article.get("description", "No description"),
                        source=article.get("source", {}).get("name", "Unknown"),
                        url=article.get("url", ""),
                        published_at=published_at
                    )
                )
            except (ValueError, TypeError) as e:
                print(f"Error processing article: {str(e)}")
                continue
        
        if not articles:
            raise HTTPException(status_code=404, detail="No valid articles found for processing")
            
        # Analyze articles using ChatGPT
        analysis_results = await analyze_articles(articles)
        
        # Generate final report
        report = await generate_report(request.ticker, articles, analysis_results)
        
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
