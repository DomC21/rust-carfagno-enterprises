import { StockAnalysisRequest, StockAnalysisResponse } from './types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function analyzeStock(request: StockAnalysisRequest): Promise<StockAnalysisResponse> {
  const response = await fetch(`${API_URL}/analyze`, {
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

export async function exportPDF(analysis: StockAnalysisResponse): Promise<Blob> {
  const response = await fetch(`${API_URL}/export/pdf`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(analysis),
  });

  if (!response.ok) {
    throw new Error('Failed to generate PDF');
  }

  return response.blob();
}

export async function exportCSV(analysis: StockAnalysisResponse): Promise<Blob> {
  const response = await fetch(`${API_URL}/export/csv`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(analysis),
  });

  if (!response.ok) {
    throw new Error('Failed to generate CSV');
  }

  return response.blob();
}
