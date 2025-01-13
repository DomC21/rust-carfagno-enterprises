from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
import logging
from app.models import StockAnalysisRequest, StockAnalysisResponse, NewsArticle
from app.services.news_service import get_news_articles, setup_logging
from app.services.analysis_service import analyze_articles
from app.services.report_service import generate_report
import os
from dotenv import load_dotenv

load_dotenv()
setup_logging()

app = FastAPI(title="Rust: A Tool by Carfagno Enterprises")

@app.get("/api/health")
async def health_check():
    """Health check endpoint to verify API is running."""
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}

# Configure CORS
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "https://stock-news-app-miq8bqnu.devinapps.com",
    "https://rust-carfagno-enterprises-3.onrender.com"
]
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

@app.get("/api/check-env")
async def check_env():
    """Check if required environment variables are set."""
    return {
        "NEWS_API_KEY": str(bool(os.getenv("NEWS_API_KEY"))),
        "OPENAI_API_KEY": str(bool(os.getenv("OPENAI_API_KEY")))
    }

@app.post("/api/analyze", response_model=StockAnalysisResponse)
async def analyze_stock(request: StockAnalysisRequest):
    try:
        # Ensure request dates are timezone-aware
        if request.start_date and request.start_date.tzinfo is None:
            request.start_date = request.start_date.replace(tzinfo=timezone.utc)
        if request.end_date and request.end_date.tzinfo is None:
            request.end_date = request.end_date.replace(tzinfo=timezone.utc)
            
        # Fetch news articles
        raw_articles = await get_news_articles(request.ticker)
        
        # Debug logging
        logging.info(f"Raw articles received: {len(raw_articles) if raw_articles else 0}")
        if raw_articles and len(raw_articles) > 0:
            logging.info(f"First article structure: {raw_articles[0]}")
        
        if not raw_articles:
            raise HTTPException(status_code=404, detail="No news articles found for the given ticker")
            
        # Convert raw articles to NewsArticle objects
        from datetime import datetime
        articles = []
        for idx, article in enumerate(raw_articles):
            try:
                # Debug logging
                print(f"Processing article {idx}...")
                print(f"Article data: {article}")
                
                # Extract data with fallbacks
                title = article.get("title")
                if not title:
                    print(f"Warning: No title found for article {idx}")
                    continue
                    
                description = article.get("description", "No description available")
                source_name = article.get("source", {}).get("name", "Unknown Source")
                url = article.get("url", "")
                published_at_str = article.get("publishedAt", "")
                
                if not published_at_str:
                    logging.warning(f"No publishedAt found for article {idx}")
                    published_at = datetime.now(timezone.utc)
                else:
                    try:
                        # Handle both 'Z' and ISO 8601 formats
                        if published_at_str.endswith('Z'):
                            published_at_str = published_at_str[:-1] + '+00:00'
                        published_at = datetime.fromisoformat(published_at_str).replace(tzinfo=timezone.utc)
                    except ValueError as e:
                        logging.warning(f"Invalid date format for article {idx}: {e}")
                        # Try alternative parsing method
                        try:
                            published_at = datetime.strptime(published_at_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                        except ValueError:
                            logging.error(f"Failed to parse date with both methods: {published_at_str}")
                            published_at = datetime.now(timezone.utc)
                
                articles.append(
                    NewsArticle(
                        title=title,
                        description=description,
                        source=source_name,
                        url=url,
                        published_at=published_at
                    )
                )
                print(f"Successfully processed article {idx}")
            except Exception as e:
                print(f"Error processing article {idx}: {str(e)}")
                print(f"Article data that caused error: {article}")
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
