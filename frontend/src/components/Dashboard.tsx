import React from 'react';
import { StockAnalysisResponse } from '../types';
import { exportPDF, exportCSV } from '../api';

interface DashboardProps {
  data: StockAnalysisResponse;
}

const Dashboard: React.FC<DashboardProps> = ({ data }) => {
  const getSentimentColor = (sentiment: string) => {
    switch (sentiment.toLowerCase()) {
      case 'positive':
        return 'text-green-600';
      case 'negative':
        return 'text-red-600';
      default:
        return 'text-yellow-600';
    }
  };

  const handleExportPDF = async () => {
    try {
      const blob = await exportPDF(data);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${data.ticker}_analysis.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Failed to export PDF:', error);
    }
  };

  const handleExportCSV = async () => {
    try {
      const blob = await exportCSV(data);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${data.ticker}_analysis.csv`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Failed to export CSV:', error);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-lg shadow-lg">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-bold">Analysis Results for {data.ticker}</h2>
          <div className="space-x-4">
            <button
              onClick={handleExportPDF}
              className="bg-gold hover:bg-yellow-600 text-black px-4 py-2 rounded transition-colors"
            >
              Export PDF
            </button>
            <button
              onClick={handleExportCSV}
              className="bg-gold hover:bg-yellow-600 text-black px-4 py-2 rounded transition-colors"
            >
              Export CSV
            </button>
          </div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <h3 className="text-lg font-semibold mb-2">Overall Sentiment</h3>
            <p className={`text-xl font-bold ${getSentimentColor(data.overall_sentiment)}`}>
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
            <div key={index} className="border-b pb-4 last:border-b-0">
              <h4 className="font-semibold mb-2">{article.title}</h4>
              <p className="text-sm text-gray-600 mb-2">
                Source: {article.source} | Published: {new Date(article.published_at).toLocaleDateString()}
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
    </div>
  );
};

export default Dashboard;
