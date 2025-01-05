import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Download, Save } from "lucide-react"
import { Filters } from './Filters'
import { Button } from "@/components/ui/button"
import { StockAnalysis } from '../types'

interface DashboardProps {
  analysis: StockAnalysis
}

export function Dashboard({ analysis }: DashboardProps) {
  const getSentimentColor = (sentiment: number) => {
    if (sentiment >= 0.5) return "bg-green-500"
    if (sentiment <= -0.5) return "bg-red-500"
    return "bg-yellow-500"
  }

  const chartData = analysis.articles.map((article) => ({
    title: article.title.substring(0, 30) + "...",
    sentiment: article.sentiment
  }))

  return (
    <div className="mt-8 space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h2 className="text-2xl font-bold text-foreground">{analysis.ticker}</h2>
          <p className="text-muted-foreground">{analysis.company_name}</p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Button variant="outline" className="text-primary" onClick={() => window.print()}>
            <Download className="mr-2" size={20} />
            Export PDF
          </Button>
          <Button variant="outline" className="text-primary" onClick={() => {
            const csv = [
              ['Title', 'Source', 'Date', 'Sentiment', 'Summary'],
              ...analysis.articles.map(article => [
                article.title,
                article.source,
                new Date(article.published_at).toLocaleDateString(),
                article.sentiment,
                article.summary
              ])
            ].map(row => row.join(',')).join('\n')
            
            const blob = new Blob([csv], { type: 'text/csv' })
            const url = window.URL.createObjectURL(blob)
            const a = document.createElement('a')
            a.href = url
            a.download = `${analysis.ticker}_analysis.csv`
            a.click()
          }}>
            <Download className="mr-2" size={20} />
            Export CSV
          </Button>
          <Button variant="outline" className="text-primary" onClick={() => {
            localStorage.setItem(`analysis_${analysis.analysis_id}`, JSON.stringify(analysis))
          }}>
            <Save className="mr-2" size={20} />
            Save Analysis
          </Button>
        </div>
      </div>
      <Filters onFilterChange={(filters) => {
        console.log('Filters changed:', filters)
        // Will implement filtering in the next step
      }} />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="bg-gray-900 border-gray-800">
          <CardHeader>
            <CardTitle className="text-white">Overall Sentiment</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="title" angle={-45} textAnchor="end" height={100} />
                  <YAxis domain={[-1, 1]} />
                  <Tooltip />
                  <Bar dataKey="sentiment" fill="#FFD700" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gray-900 border-gray-800">
          <CardHeader>
            <CardTitle className="text-white">Key Takeaways</CardTitle>
          </CardHeader>
          <CardContent>
            <ScrollArea className="h-64">
              <ul className="space-y-2">
                {analysis.key_takeaways.map((takeaway, index) => (
                  <li key={index} className="text-gray-300">• {takeaway}</li>
                ))}
              </ul>
            </ScrollArea>
          </CardContent>
        </Card>

        <Card className="bg-gray-900 border-gray-800 md:col-span-2">
          <CardHeader>
            <CardTitle className="text-white">Articles</CardTitle>
          </CardHeader>
          <CardContent>
            <ScrollArea className="h-96">
              <div className="space-y-4">
                {analysis.articles.map((article, index) => (
                  <div key={index} className="p-4 bg-gray-800 rounded-lg">
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="text-white font-medium">{article.title}</h3>
                      <Badge className={getSentimentColor(article.sentiment)}>
                        {article.sentiment.toFixed(2)}
                      </Badge>
                    </div>
                    <p className="text-gray-400 text-sm mb-2">{article.summary}</p>
                    <div className="text-sm text-gray-500">
                      {new Date(article.published_at).toLocaleDateString()}
                    </div>
                  </div>
                ))}
              </div>
            </ScrollArea>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
