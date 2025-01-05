import { useState } from 'react'
import { Header } from './components/Header'
import { StockInput } from './components/StockInput'
import { Dashboard } from './components/Dashboard'
import { StockAnalysis } from './types'
import { analyzeStock } from './api'

function App() {
  const [analysis, setAnalysis] = useState<StockAnalysis | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleAnalyze = async (ticker: string, companyName: string) => {
    try {
      setLoading(true)
      setError(null)
      const result = await analyzeStock(ticker, companyName)
      setAnalysis(result)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to analyze stock')
      console.error('Analysis error:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-black">
      <Header />
      <main className="container mx-auto py-8 px-4">
        <StockInput onSubmit={handleAnalyze} />
        {error && (
          <div className="mt-4 p-4 bg-destructive/10 text-destructive rounded-md">
            {error}
          </div>
        )}
        {loading && (
          <div className="mt-4 text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto" />
            <p className="mt-2 text-muted-foreground">Analyzing stock...</p>
          </div>
        )}
        {analysis && <Dashboard analysis={analysis} />}
      </main>
    </div>
  )
}

export default App
