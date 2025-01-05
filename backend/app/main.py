from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import StockAnalysisRequest, StockAnalysisResponse
from .services.news_service import get_news_articles
from .services.analysis_service import analyze_articles
from .services.report_service import generate_report
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Rust: A Tool by Carfagno Enterprises")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins in development
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
        articles = await get_news_articles(request.ticker)
        
        if not articles:
            raise HTTPException(status_code=404, detail="No news articles found for the given ticker")
        
        # Analyze articles using ChatGPT
        analysis_results = await analyze_articles(articles)
        
        # Generate final report
        report = await generate_report(request.ticker, articles, analysis_results)
        
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
