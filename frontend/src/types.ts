export interface StockAnalysisRequest {
  ticker: string;
  start_date?: string;
  end_date?: string;
}

export interface NewsArticle {
  title: string;
  description: string;
  url: string;
  published_at: string;
  source: string;
}

export interface ArticleAnalysis {
  summary: string;
  sentiment: string;
  sentiment_score: number;
  key_takeaways: string[];
  significant_quotes: string[];
}

export interface StockAnalysisResponse {
  ticker: string;
  overall_sentiment: string;
  overall_sentiment_score: number;
  articles: NewsArticle[];
  analyses: ArticleAnalysis[];
  trading_implications: string[];
  timestamp: string;
}
