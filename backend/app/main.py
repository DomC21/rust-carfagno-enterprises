from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
import json
from datetime import datetime
from typing import Dict, List
import os

from models import StockRequest, AnalysisResponse, Article
from services.news_service import NewsService
from services.analysis_service import AnalysisService
from services.report_service import ReportService

app = FastAPI(title="Rust: A Tool by Carfagno Enterprises")

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize services
news_service = NewsService()
analysis_service = AnalysisService()
report_service = ReportService()

# In-memory storage for analysis results
analysis_storage: Dict[str, dict] = {}

# Debug function for storage operations
def debug_storage_operation(operation: str, analysis_id: str | None = None, data: dict | None = None) -> None:
    print(f"\n=== Storage Operation: {operation} ===")
    print(f"Analysis ID: {analysis_id}")
    if data:
        print(f"Data: {json.dumps(data, indent=2)}")
    print(f"Current storage keys: {list(analysis_storage.keys())}")
    print("=" * 50 + "\n")

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_stock(request: StockRequest):
    try:
        print("\n=== Starting Stock Analysis ===")
        print(f"Request: {jsonable_encoder(request)}")
        
        # Fetch news articles
        articles = await news_service.get_stock_news(request.ticker, request.company_name)
        
        if not articles:
            raise HTTPException(status_code=404, detail="No news articles found for the given stock")

        print(f"Found {len(articles)} articles")
        
        # Analyze articles
        analysis = await analysis_service.analyze_stock_news(
            request.ticker,
            request.company_name,
            articles
        )

        # Store analysis for future reference
        analysis_dict = jsonable_encoder(analysis)
        analysis_storage[analysis.analysis_id] = analysis_dict
        debug_storage_operation("Store in analyze_stock", analysis.analysis_id, analysis_dict)
        
        # Return JSON response using FastAPI's jsonable_encoder
        return JSONResponse(content=analysis_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze/test", response_model=AnalysisResponse)
async def test_analysis():
    """Test endpoint for verifying analysis functionality with sample data."""
    try:
        # Sample article for testing
        test_article = Article(
            title="Apple Stock Hits All-Time High on AI Optimism",
            url="https://example.com/article1",
            source="Test News",
            published_at=datetime.now(),
            content="Apple Inc. (AAPL) shares reached a record high today as investors showed optimism about the company's artificial intelligence initiatives. The tech giant is reportedly developing new AI features for its upcoming iPhone models. Analysts expect these developments to significantly boost revenue in the coming quarters."
        )

        # Analyze test article
        analysis = await analysis_service.analyze_stock_news(
            "AAPL",
            "Apple Inc.",
            [test_article]
        )

        # Store analysis for future reference
        analysis_dict = jsonable_encoder(analysis)
        analysis_storage[analysis.analysis_id] = analysis_dict
        debug_storage_operation("Store in test_analysis", analysis.analysis_id, analysis_dict)
        
        # Return JSON response using FastAPI's jsonable_encoder
        return JSONResponse(content=analysis_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analysis/{analysis_id}")
async def get_analysis(analysis_id: str):
    if analysis_id not in analysis_storage:
        raise HTTPException(status_code=404, detail="Analysis not found")
    debug_storage_operation("Retrieve analysis", analysis_id, analysis_storage[analysis_id])
    return JSONResponse(content=analysis_storage[analysis_id])

@app.get("/api/analysis/list")
async def list_analyses():
    analyses = []
    debug_storage_operation("List analyses")
    for aid, analysis in analysis_storage.items():
        try:
            analyses.append(jsonable_encoder({
                "analysis_id": aid,
                "ticker": analysis.get("ticker", "Unknown"),
                "timestamp": analysis.get("analysis_timestamp", datetime.now()),
                "sentiment": analysis.get("overall_sentiment", 0.0)
            }))
        except Exception as e:
            print(f"Error processing analysis {aid}: {str(e)}")
            continue
    return JSONResponse(content=analyses)

@app.get("/api/report/{analysis_id}")
async def get_report(analysis_id: str, format: str = "pdf"):
    if analysis_id not in analysis_storage:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    analysis = AnalysisResponse(**analysis_storage[analysis_id])
    
    if format.lower() == "pdf":
        buffer = report_service.generate_pdf_report(analysis)
        return StreamingResponse(
            buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=stock_analysis_{analysis.ticker}_{analysis_id}.pdf"}
        )
    elif format.lower() == "csv":
        buffer = report_service.generate_csv_report(analysis)
        return StreamingResponse(
            buffer,
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=stock_analysis_{analysis.ticker}_{analysis_id}.csv"}
        )
    else:
        raise HTTPException(status_code=400, detail="Unsupported format. Use 'pdf' or 'csv'")
