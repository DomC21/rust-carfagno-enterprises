import { useState } from "react"
import { Search } from "lucide-react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

interface StockInputProps {
  onSubmit: (ticker: string, companyName: string) => void
}

export function StockInput({ onSubmit }: StockInputProps) {
  const [ticker, setTicker] = useState("")
  const [companyName, setCompanyName] = useState("")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (ticker) {
      onSubmit(ticker.toUpperCase(), companyName)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4 w-full max-w-xl mx-auto">
      <div className="flex flex-col sm:flex-row gap-4">
        <Input
          placeholder="Stock Ticker (e.g., AAPL)"
          value={ticker}
          onChange={(e) => setTicker(e.target.value)}
          className="flex-1"
        />
        <Input
          placeholder="Company Name (optional)"
          value={companyName}
          onChange={(e) => setCompanyName(e.target.value)}
          className="flex-1"
        />
        <Button type="submit" className="bg-[#FFD700] text-black hover:bg-[#FFD700]/90">
          <Search className="mr-2" size={20} />
          Analyze
        </Button>
      </div>
    </form>
  )
}
