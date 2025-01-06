import os
from typing import List
from openai import AsyncOpenAI
from ..models import NewsArticle, ArticleAnalysis

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def analyze_articles(articles: List[NewsArticle]) -> List[ArticleAnalysis]:
    """Analyze news articles using ChatGPT."""
    analyses = []
    
    for article in articles:
        # Prepare detailed prompt for ChatGPT
        prompt = f"""You are an expert financial analyst. Analyze the following news article related to {article.ticker} from a financial and market sentiment perspective. Provide the following detailed output:

Summary:
Summarize the main points of the article in 3-5 sentences, focusing on how the news may impact the stock's performance or market perception.

Sentiment Analysis:
Assess the article's sentiment on a scale from 0% to 100%, where:
0% indicates overwhelmingly negative sentiment (e.g., bad earnings, major lawsuits, or negative economic indicators).
50% indicates neutral sentiment (e.g., mixed messages, uncertainty, or minimal impact).
100% indicates overwhelmingly positive sentiment (e.g., record earnings, favorable market conditions, or groundbreaking developments).

Consider the following factors when assigning sentiment:
- Language Tone: Is the tone positive, negative, or neutral?
- Key Events or Statements: What events or quotes could influence investor sentiment?
- Implications: Does the news suggest growth, risk, or stability for the stock?

Article:
Title: {article.title}
Description: {article.description}
Source: {article.source}

Format the response as JSON with the following structure:
{{
    "summary": "Brief summary here",
    "sentiment": "positive/neutral/negative based on score (0-40% negative, 41-59% neutral, 60-100% positive)",
    "sentiment_score": "percentage converted to -1.0 to 1.0 scale",
    "key_takeaways": ["point 1", "point 2", "point 3"],
    "significant_quotes": ["quote 1", "quote 2"]
}}"""
        
        try:
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a financial analyst expert. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            # Parse the response
            import json
            analysis_text = response.choices[0].message.content
            try:
                analysis_data = json.loads(analysis_text)
                
                # Convert percentage score to -1.0 to 1.0 scale
                percentage_score = float(analysis_data.get("sentiment_score", 50))
                normalized_score = (percentage_score - 50) / 50  # Convert 0-100 to -1.0 to 1.0
                
                analyses.append(
                    ArticleAnalysis(
                        summary=analysis_data["summary"],
                        sentiment=analysis_data["sentiment"],
                        sentiment_score=normalized_score,
                        key_takeaways=analysis_data["key_takeaways"],
                        significant_quotes=analysis_data["significant_quotes"]
                    )
                )
            except json.JSONDecodeError as e:
                print(f"Error parsing ChatGPT response: {analysis_text}")
                print(f"JSON Error: {str(e)}")
                continue
                
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
