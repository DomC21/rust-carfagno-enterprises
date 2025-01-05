from newsapi import NewsApiClient
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from typing import Optional, List
from models import Article

load_dotenv()

class NewsService:
    def __init__(self):
        self.api = NewsApiClient(api_key=os.getenv('NEWS_API_KEY'))

    async def get_stock_news(self, ticker: str, company_name: Optional[str] = None) -> list[Article]:
        print(f"\n=== News API Request ===")
        print(f"Ticker: {ticker}")
        print(f"Company Name: {company_name}")
        
        # Get news from the last 7 days
        from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        
        try:
            # Construct a more specific query for better results
            search_query = f'"{ticker}"'  # Exact match for ticker
            if company_name:
                search_query += f' OR "{company_name}"'  # Exact match for company name
            search_query += ' AND (stock OR market OR earnings OR trading OR investment)'
            
            print(f"Search Query: {search_query}")
            print(f"From Date: {from_date}")
            
            response = self.api.get_everything(
                q=search_query,
                from_param=from_date,
                language='en',
                sort_by='relevancy',
                page_size=10  # Reduced for testing
            )
            
            print("\n=== News API Response ===")
            print(f"Status: {response.get('status')}")
            print(f"Total Results: {response.get('totalResults', 0)}")
            
            if response.get('status') != 'ok':
                error_msg = f"News API error: {response.get('message', 'Unknown error')}"
                print(f"Error: {error_msg}")
                raise Exception(error_msg)
            
            if not response.get('articles'):
                print(f"No articles found for query: {search_query}")
                return []
                
            print(f"Found {len(response['articles'])} articles")
            
            articles = []
            for article in response['articles']:
                # Skip articles without meaningful content
                if not article.get('content') and not article.get('description'):
                    continue
                    
                try:
                    articles.append(
                        Article(
                            title=article['title'],
                            url=article['url'],
                            source=article['source']['name'],
                            published_at=datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ'),
                            content=article.get('content') or article.get('description') or '',
                        )
                    )
                except (KeyError, ValueError) as e:
                    print(f"Error parsing article: {str(e)}")
                    continue
            
            if not articles:
                print("No valid articles found after filtering")
                
            return articles
        except Exception as e:
            print(f"Error fetching news: {str(e)}")
            raise  # Re-raise to handle in the API endpoint
