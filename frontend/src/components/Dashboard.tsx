import React from 'react';
import { StockAnalysisResponse } from '../types';
import { Button } from './ui/button';

interface DashboardProps {
  data: StockAnalysisResponse;
}

const Dashboard: React.FC<DashboardProps> = ({ data }) => {
  const getSentimentColor = (sentiment: string) => {
    switch (sentiment.toLowerCase()) {
      case 'positive':
        return 'text-green-600 transition-colors duration-500 hover:text-green-400 glow-green';
      case 'negative':
        return 'text-red-600 transition-colors duration-500 hover:text-red-400 glow-red';
      default:
        return 'text-yellow-600 transition-colors duration-500 hover:text-yellow-400 glow-yellow';
    }
  };

  return (
    <div className="space-y-6" data-testid="analysis-results">
      <div className="bg-white p-6 rounded-lg shadow-lg">
        <h2 className="text-2xl font-bold mb-4">Analysis Results for {data.ticker}</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <h3 className="text-lg font-semibold mb-2">Overall Sentiment</h3>
            <p className={`text-xl font-bold ${getSentimentColor(data.overall_sentiment)}`} data-testid="sentiment-score">
              {data.overall_sentiment.toUpperCase()} ({data.overall_sentiment_score.toFixed(2)})
            </p>
          </div>
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-lg">
        <h3 className="text-xl font-bold mb-4">Trading Implications</h3>
        <ul className="list-disc pl-5 space-y-2">
          {data.trading_implications.map((implication, index) => (
            <li key={index} className="text-gray-700">{implication}</li>
          ))}
        </ul>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-lg">
        <h3 className="text-xl font-bold mb-4">News Analysis</h3>
        <div className="space-y-6">
          {data.articles.map((article, index) => (
            <div key={index} className="border-b pb-4 last:border-b-0" data-testid="article-summary">
              <h4 className="font-semibold mb-2">{article.title}</h4>
              <p className="text-sm text-gray-600 mb-2">
                Source: {article.source} | Published: {new Date(article.published_at).toLocaleString()}
              </p>
              <div className="pl-4 border-l-4 border-blue-500">
                <p className="text-gray-700 mb-2">{data.analyses[index].summary}</p>
                <p className={`font-semibold ${getSentimentColor(data.analyses[index].sentiment)}`}>
                  Sentiment: {data.analyses[index].sentiment} ({data.analyses[index].sentiment_score.toFixed(2)})
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="flex gap-4 mt-6">
        <Button
          onClick={() => window.open('/api/export/pdf', '_blank')}
          data-testid="export-pdf"
          variant="outline"
        >
          Export PDF
        </Button>
        <Button
          onClick={() => window.open('/api/export/csv', '_blank')}
          data-testid="export-csv"
          variant="outline"
        >
          Export CSV
        </Button>
        <Button
          onClick={() => window.location.reload()}
          data-testid="clear-button"
          variant="outline"
        >
          Clear Results
        </Button>
      </div>
    </div>
  );
};

export default Dashboard;
