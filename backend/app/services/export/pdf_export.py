from typing import List
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
from ...models import NewsArticle, ArticleAnalysis, StockAnalysisResponse

def generate_pdf_report(analysis: StockAnalysisResponse) -> BytesIO:
    """Generate a PDF report from the stock analysis."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30
    )
    story.append(Paragraph(f"Stock Analysis Report - {analysis.ticker}", title_style))
    story.append(Spacer(1, 12))

    # Overall Sentiment
    story.append(Paragraph(f"Overall Sentiment: {analysis.overall_sentiment}", styles['Heading2']))
    story.append(Paragraph(f"Sentiment Score: {analysis.overall_sentiment_score:.2f}", styles['Normal']))
    story.append(Spacer(1, 12))

    # Trading Implications
    story.append(Paragraph("Trading Implications:", styles['Heading2']))
    for implication in analysis.trading_implications:
        story.append(Paragraph(f"• {implication}", styles['Normal']))
    story.append(Spacer(1, 12))

    # Article Analysis
    story.append(Paragraph("Article Analysis:", styles['Heading2']))
    for i, (article, analysis) in enumerate(zip(analysis.articles, analysis.analyses)):
        story.append(Paragraph(f"Article {i+1}: {article.title}", styles['Heading3']))
        story.append(Paragraph(f"Source: {article.source}", styles['Normal']))
        story.append(Paragraph(f"Published: {article.published_at}", styles['Normal']))
        story.append(Paragraph(f"Summary: {analysis.summary}", styles['Normal']))
        story.append(Paragraph(f"Sentiment: {analysis.sentiment} ({analysis.sentiment_score:.2f})", styles['Normal']))
        
        # Key Takeaways
        story.append(Paragraph("Key Takeaways:", styles['Heading4']))
        for takeaway in analysis.key_takeaways:
            story.append(Paragraph(f"• {takeaway}", styles['Normal']))
            
        # Significant Quotes
        story.append(Paragraph("Significant Quotes:", styles['Heading4']))
        for quote in analysis.significant_quotes:
            story.append(Paragraph(f""{quote}"", styles['Normal']))
            
        story.append(Spacer(1, 12))

    doc.build(story)
    buffer.seek(0)
    return buffer
