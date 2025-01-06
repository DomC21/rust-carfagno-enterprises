import os
from typing import List
import openai
from ..models import NewsArticle, ArticleAnalysis

openai.api_key = os.getenv("OPENAI_API_KEY")

async def analyze_articles(articles: List[NewsArticle]) -> List[ArticleAnalysis]:
    """Analyze news articles using ChatGPT."""
    
    analyses = []
    
    for article in articles:
        # Prepare prompt for ChatGPT
        prompt = f"""
        Analyze this financial news article:
        Title: {article.title}
        Description: {article.description}
        Source: {article.source}
        
        Please provide:
        1. A brief summary
        2. Sentiment (positive/neutral/negative)
        3. Sentiment score (-1.0 to 1.0)
        4. Key takeaways (3 points)
        5. Significant quotes
        
        Format as JSON.
        """
        
        try: 
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a financial analyst expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            # Parse the response
            import json
            analysis_text = response.choices[0].message.content
            try:
                analysis_data = json.loads(analysis_text)
            except json.JSONDecodeError:
                print(f"Error parsing ChatGPT response: {analysis_text}")
                continue
                
            # Ensure all required fields are present
            required_fields = ["summary", "sentiment", "sentiment_score", "key_takeaways", "significant_quotes"]
            if not all(field in analysis_data for field in required_fields):
                print(f"Missing required fields in analysis data: {analysis_data}")
                continue
            
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
            # Provide default analysis when ChatGPT analysis fails
            analyses.append(
                ArticleAnalysis(
                    summary="Unable to generate summary at this time.",
                    sentiment="neutral",
                    sentiment_score=0.0,
                    key_takeaways=["Analysis unavailable"],
                    significant_quotes=["No quotes available"]
                )
            )
    
    return analyses
