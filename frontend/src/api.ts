import { StockAnalysis } from './types'

const API_URL = (import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000').trim()

export async function analyzeStock(ticker: string, companyName: string): Promise<StockAnalysis> {
  const response = await fetch(`${API_URL}/api/analyze`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ ticker, company_name: companyName }),
  })
  
  if (!response.ok) {
    throw new Error('Failed to analyze stock')
  }
  
  return response.json()
}

export async function getAnalysisHistory(): Promise<StockAnalysis[]> {
  const savedAnalyses = Object.keys(localStorage)
    .filter(key => key.startsWith('analysis_'))
    .map(key => JSON.parse(localStorage.getItem(key) || '{}'))
  return savedAnalyses
}
