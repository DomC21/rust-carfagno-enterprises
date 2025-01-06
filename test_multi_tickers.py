import asyncio
import aiohttp
import time
from datetime import datetime

# Test tickers (more than 20 as requested)
TEST_TICKERS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", 
    "NVDA", "TSLA", "JPM", "V", "WMT",
    "PG", "JNJ", "UNH", "HD", "BAC",
    "MA", "XOM", "PFE", "DIS", "CSCO",
    "NFLX", "ADBE", "CRM", "INTC", "VZ"
]

async def test_ticker(session, ticker):
    start_time = time.time()
    try:
        url = "https://rust-carfagno-enterprises-3.onrender.com/analyze"
        async with session.post(url, json={"ticker": ticker}) as response:
            if response.status == 200:
                data = await response.json()
                duration = time.time() - start_time
                print(f"✓ {ticker}: Success ({duration:.2f}s)")
                print(f"  Sentiment: {data['overall_sentiment']} ({data['overall_sentiment_score']:.2f})")
                print(f"  Articles analyzed: {len(data['articles'])}")
                return True, duration
            else:
                duration = time.time() - start_time
                print(f"✗ {ticker}: Failed with status {response.status}")
                return False, duration
    except Exception as e:
        print(f"✗ {ticker}: Error - {str(e)}")
        return False, time.time() - start_time

async def main():
    print(f"Starting performance test at {datetime.now()}")
    print(f"Testing {len(TEST_TICKERS)} tickers: {', '.join(TEST_TICKERS)}")
    print("-" * 50)

    async with aiohttp.ClientSession() as session:
        tasks = [test_ticker(session, ticker) for ticker in TEST_TICKERS]
        results = await asyncio.gather(*tasks)

    successes = sum(1 for success, _ in results if success)
    total_time = sum(duration for _, duration in results)
    avg_time = total_time / len(TEST_TICKERS)

    print("\nTest Summary:")
    print("-" * 50)
    print(f"Total tickers tested: {len(TEST_TICKERS)}")
    print(f"Successful analyses: {successes}")
    print(f"Failed analyses: {len(TEST_TICKERS) - successes}")
    print(f"Average processing time: {avg_time:.2f}s")
    print(f"Total test duration: {total_time:.2f}s")
    print("-" * 50)

if __name__ == "__main__":
    asyncio.run(main())
