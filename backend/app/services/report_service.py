import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
from datetime import datetime
from models import AnalysisResponse

class ReportService:
    @staticmethod
    def generate_pdf_report(analysis: AnalysisResponse) -> BytesIO:
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

        # Company Info
        if analysis.company_name:
            story.append(Paragraph(f"Company: {analysis.company_name}", styles['Heading2']))
        story.append(Paragraph(f"Overall Sentiment: {analysis.overall_sentiment:.2f}", styles['Heading2']))
        story.append(Paragraph(f"Analysis Date: {analysis.analysis_timestamp.strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        story.append(Spacer(1, 12))

        # Articles Analysis
        for article in analysis.articles:
            story.append(Paragraph(f"Article: {article.title}", styles['Heading3']))
            story.append(Paragraph(f"Source: {article.source}", styles['Normal']))
            story.append(Paragraph(f"Published: {article.published_at.strftime('%Y-%m-%d')}", styles['Normal']))
            story.append(Paragraph(f"Sentiment: {article.sentiment:.2f}", styles['Normal']))
            story.append(Paragraph(f"Summary: {article.summary}", styles['Normal']))
            
            # Key Takeaways
            if article.key_takeaways:
                story.append(Paragraph("Key Takeaways:", styles['Heading4']))
                for takeaway in article.key_takeaways:
                    story.append(Paragraph(f"• {takeaway}", styles['Normal']))
            
            story.append(Spacer(1, 12))

        doc.build(story)
        buffer.seek(0)
        return buffer

    @staticmethod
    def generate_csv_report(analysis: AnalysisResponse) -> BytesIO:
        # Create a list of dictionaries for the DataFrame
        data = []
        for article in analysis.articles:
            data.append({
                'Title': article.title,
                'Source': article.source,
                'Published Date': article.published_at,
                'Sentiment': article.sentiment,
                'Summary': article.summary,
                'Key Takeaways': '; '.join(article.key_takeaways) if article.key_takeaways else '',
                'URL': article.url
            })

        df = pd.DataFrame(data)
        
        buffer = BytesIO()
        df.to_csv(buffer, index=False)
        buffer.seek(0)
        return buffer
