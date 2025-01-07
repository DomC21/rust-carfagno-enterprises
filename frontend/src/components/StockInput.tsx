import React, { useState } from 'react';
import { Button } from './ui/button';

interface StockInputProps {
  onSubmit: (ticker: string) => void;
  isLoading: boolean;
}

const StockInput: React.FC<StockInputProps> = ({ onSubmit, isLoading }) => {
  const [ticker, setTicker] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (ticker.trim()) {
      onSubmit(ticker.trim().toUpperCase());
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-4 items-center">
      <div className="flex-1">
        <input
          type="text"
          data-testid="stock-input"
          value={ticker}
          onChange={(e) => setTicker(e.target.value)}
          placeholder="Enter stock ticker (e.g., AAPL)"
          className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white text-black"
          disabled={isLoading}
        />
      </div>
      <Button type="submit" data-testid="analyze-button" disabled={isLoading || !ticker.trim()}>
        {isLoading ? 'Analyzing...' : 'Analyze'}
      </Button>
    </form>
  );
};

export default StockInput;
