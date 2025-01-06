import { StockAnalysisRequest, StockAnalysisResponse } from './types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function analyzeStock(request: StockAnalysisRequest): Promise<StockAnalysisResponse> {
  const response = await fetch(`${API_URL}/api/analyze`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(error);
  }

  return response.json();
}
