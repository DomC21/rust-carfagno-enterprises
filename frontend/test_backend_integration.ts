import axios from 'axios';

const BACKEND_URL = 'https://rust-carfagno-enterprises-3.onrender.com';
const TEST_TICKERS = ['AAPL', 'GOOGL', 'MSFT'];

async function testBackendIntegration() {
  console.log('Testing backend integration...');
  
  for (const ticker of TEST_TICKERS) {
    try {
      console.log(`Testing analysis for ${ticker}...`);
      const response = await axios.post(`${BACKEND_URL}/api/analyze`, {
        ticker,
        days: 7
      });
      
      console.log(`Response for ${ticker}:`, {
        status: response.status,
        sentiment: response.data.overall_sentiment,
        articleCount: response.data.articles.length
      });
    } catch (error) {
      console.error(`Error testing ${ticker}:`, error.response?.data || error.message);
    }
  }
}

testBackendIntegration();
