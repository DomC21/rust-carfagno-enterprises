export interface Article {
  title: string
  url: string
  source: string
  published_at: string
  content: string
  sentiment: number
  summary: string
  key_takeaways: string[]
  significant_quotes: string[]
}

export interface StockAnalysis {
  analysis_id: string
  ticker: string
  company_name: string
  articles: Article[]
  summaries: string[]
  sentiment_scores: number[]
  overall_sentiment: number
  key_takeaways: string[]
  significant_quotes: string[]
  analysis_timestamp: string
}
