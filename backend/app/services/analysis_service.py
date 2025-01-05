import openai
from datetime import datetime
import os
import uuid
from dotenv import load_dotenv
from models import Article, AnalysisResponse

load_dotenv()

class AnalysisService:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')

    async def analyze_article(self, article: Article) -> Article:
        try:
            # Create a prompt for GPT to analyze the article
            prompt = f"""Analyze the following article about stocks/financial markets:
            Title: {article.title}
            Content: {article.content}
            
            Please provide a JSON response with the following structure:
            {{
                "summary": "2-3 sentence summary",
                "sentiment": float between -1 and 1 (-1 very negative, 0 neutral, 1 very positive),
                "key_takeaways": ["takeaway 1", "takeaway 2", "takeaway 3"],
                "significant_quotes": ["most impactful quote 1", "most impactful quote 2"]
            }}
            """

            client = openai.AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a financial analyst expert. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={ "type": "json_object" }
            )

            analysis = response.choices[0].message.content
            if not analysis:
                raise ValueError("No response content from OpenAI")
            
            # Parse the JSON response
            import json
            try:
                result = json.loads(analysis)
                article.summary = result['summary']
                article.sentiment = float(result['sentiment'])
                article.key_takeaways = result['key_takeaways']
                article.significant_quotes = result['significant_quotes']
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error parsing OpenAI response: {str(e)}")
                article.summary = "Error analyzing article"
                article.sentiment = 0.0
                article.key_takeaways = ["Error analyzing article"]
                article.significant_quotes = []

            return article
        except Exception as e:
            print(f"Error analyzing article: {str(e)}")
            article.summary = "Error analyzing article"
            article.sentiment = 0.0
            article.key_takeaways = ["Error analyzing article"]
            article.significant_quotes = []
            return article

    async def analyze_stock_news(self, ticker: str, company_name: str, articles: list[Article]) -> AnalysisResponse:
        # Analyze each article
        analyzed_articles = []
        summaries = []
        sentiment_scores = []
        all_key_takeaways = []
        all_significant_quotes = []
        
        for article in articles:
            analyzed_article = await self.analyze_article(article)
            if analyzed_article.sentiment is not None:
                sentiment_scores.append(analyzed_article.sentiment)
            if analyzed_article.summary:
                summaries.append(analyzed_article.summary)
            if analyzed_article.key_takeaways:
                all_key_takeaways.extend(analyzed_article.key_takeaways)
            if analyzed_article.significant_quotes:
                all_significant_quotes.extend(analyzed_article.significant_quotes)
            analyzed_articles.append(analyzed_article)

        # Calculate overall sentiment
        overall_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0

        return AnalysisResponse(
            ticker=ticker,
            company_name=company_name,
            articles=analyzed_articles,
            summaries=summaries,
            sentiment_scores=sentiment_scores,
            overall_sentiment=overall_sentiment,
            key_takeaways=all_key_takeaways,
            significant_quotes=all_significant_quotes
        )
