import os
from typing import List
from openai import AsyncOpenAI
from ..models import NewsArticle, ArticleAnalysis

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert financial analyst providing market insights."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            # Parse the response
            analysis_text = response.choices[0].message.content
            import json
            # Clean the response text to ensure it contains only the JSON object
            json_str = analysis_text.strip().replace("```json", "").replace("```", "")
            analysis_data = json.loads(json_str)  # Safely parse JSON
            
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
