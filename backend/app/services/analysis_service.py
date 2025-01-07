import os
from typing import List
from openai import AsyncOpenAI
from ..models import NewsArticle, ArticleAnalysis

client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    timeout=30.0,  # Set timeout to 30 seconds
    max_retries=2  # Allow 2 retries
)

async def analyze_articles(articles: List[NewsArticle]) -> List[ArticleAnalysis]:
    """Analyze news articles using ChatGPT API."""
    
    analyses = []
    
    for article in articles:
        # Prepare prompt for ChatGPT
        prompt = f"""
        Analyze this financial news article and return a JSON response in the following format:
        {{
            "summary": "Brief summary of the article",
            "sentiment": "positive/neutral/negative",
            "sentiment_score": 0.0,
            "key_takeaways": ["point 1", "point 2", "point 3"],
            "significant_quotes": ["quote 1", "quote 2"]
        }}

        Article to analyze:
        Title: {article.title}
        Description: {article.description}
        Source: {article.source}
        """
        
        try:
            import json
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert financial analyst. Respond only with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            # Parse the response with proper error handling
            if not response or not response.choices:
                raise ValueError("Empty response from ChatGPT API")
                
            analysis_text = response.choices[0].message.content
            if not analysis_text:
                raise ValueError("Empty content in ChatGPT response")
                
            # Parse JSON with error handling
            try:
                analysis_data = json.loads(analysis_text)
            except json.JSONDecodeError as e:
                print(f"JSON parsing error: {str(e)}")
                raise ValueError(f"Invalid JSON response: {analysis_text}")
                
            # Validate required fields
            required_fields = ["summary", "sentiment", "sentiment_score", "key_takeaways", "significant_quotes"]
            missing_fields = [field for field in required_fields if field not in analysis_data]
            if missing_fields:
                raise ValueError(f"Missing required fields in response: {', '.join(missing_fields)}")
            
            analyses.append(
                ArticleAnalysis(
                    summary=analysis_data["summary"],
                    sentiment=analysis_data["sentiment"],
                    sentiment_score=float(analysis_data["sentiment_score"]),
                    key_takeaways=analysis_data["key_takeaways"],
                    significant_quotes=analysis_data["significant_quotes"]
                )
            )
        except Exception as e:
            print(f"Error analyzing article: {str(e)}")
            continue
    
    return analyses
