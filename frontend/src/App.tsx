import React, { useState } from 'react'
import Header from './components/Header'
import StockInput from './components/StockInput'
import Dashboard from './components/Dashboard'
import { StockAnalysisResponse } from './types'
import './index.css'

const App: React.FC = () => {
  const [loading, setLoading] = useState(false)
  const [data, setData] = useState<StockAnalysisResponse | null>(null)

  const handleStockSubmit = async (ticker: string) => {
    setLoading(true)
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ticker }),
      })
      if (!response.ok) {
        throw new Error('Failed to fetch stock analysis')
      }
      const responseData: StockAnalysisResponse = await response.json()
      setData(responseData)
    } catch (error) {
      console.error('Error analyzing stock:', error)
      setData(null)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-black text-white">
      <Header />
      <main className="container mx-auto px-4 py-8">
        <StockInput onSubmit={handleStockSubmit} isLoading={loading} />
        {data && <Dashboard data={data} />}
        {loading ? (
          <div className="text-center mt-12 p-8 bg-brand-dark rounded-lg border border-brand-gold">
            <h2 className="text-2xl font-bold brand-gold mb-4">Analyzing Stock Data</h2>
            <p className="text-gray-400">Please wait while we fetch and analyze the latest news...</p>
          </div>
        ) : !data && (
          <div className="text-center mt-12 p-8 bg-brand-dark rounded-lg border border-brand-gold">
            <h2 className="text-2xl font-bold brand-gold mb-4">Welcome to Rust</h2>
            <p className="text-gray-400">
              Enter a stock ticker to analyze news and sentiment using advanced AI technology
            </p>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
