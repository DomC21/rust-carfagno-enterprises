import csv
from io import StringIO
from typing import List
from ...models import NewsArticle, ArticleAnalysis, StockAnalysisResponse

def generate_csv_report(analysis: StockAnalysisResponse) -> StringIO:
    """Generate a CSV report from the stock analysis."""
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Stock Analysis Report', analysis.ticker])
    writer.writerow([])
    
    # Overall Analysis
    writer.writerow(['Overall Analysis'])
    writer.writerow(['Overall Sentiment', analysis.overall_sentiment])
    writer.writerow(['Sentiment Score', f"{analysis.overall_sentiment_score:.2f}"])
    writer.writerow([])
    
    # Trading Implications
    writer.writerow(['Trading Implications'])
    for implication in analysis.trading_implications:
        writer.writerow(['•', implication])
    writer.writerow([])
    
    # Article Analysis
    writer.writerow(['Article Analysis'])
    writer.writerow(['Title', 'Source', 'Published Date', 'Sentiment', 'Score', 'Summary'])
    
    for article, analysis in zip(analysis.articles, analysis.analyses):
        writer.writerow([
            article.title,
            article.source,
            article.published_at,
            analysis.sentiment,
            f"{analysis.sentiment_score:.2f}",
            analysis.summary
        ])
    writer.writerow([])
    
    # Key Takeaways and Quotes
    for i, (article, analysis) in enumerate(zip(analysis.articles, analysis.analyses)):
        writer.writerow([f'Article {i+1} Key Takeaways'])
        for takeaway in analysis.key_takeaways:
            writer.writerow(['•', takeaway])
        writer.writerow([])
        
        writer.writerow([f'Article {i+1} Significant Quotes'])
        for quote in analysis.significant_quotes:
            writer.writerow(['•', quote])
        writer.writerow([])
    
    output.seek(0)
    return output
