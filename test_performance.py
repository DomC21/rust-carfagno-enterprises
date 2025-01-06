import asyncio
import aiohttp
import time
import statistics
from datetime import datetime

async def fetch_analysis(session, ticker):
    url = "https://rust-carfagno-enterprises-3.onrender.com/analyze"
    start_time = time.time()
    try:
        async with session.post(url, json={"ticker": ticker}) as response:
            elapsed = time.time() - start_time
            return {
                "status": response.status,
                "elapsed": elapsed,
                "ticker": ticker
            }
    except Exception as e:
        return {
            "status": "error",
            "elapsed": time.time() - start_time,
            "ticker": ticker,
            "error": str(e)
        }

async def run_concurrent_tests(tickers, concurrency=3):
    print(f"\nStarting performance test at {datetime.now()}")
    print(f"Testing {len(tickers)} tickers with concurrency of {concurrency}")
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for ticker in tickers:
            task = fetch_analysis(session, ticker)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
    
    # Analyze results
    successful_requests = [r for r in results if r["status"] == 200]
    failed_requests = [r for r in results if r["status"] != 200]
    
    if successful_requests:
        response_times = [r["elapsed"] for r in successful_requests]
        avg_time = statistics.mean(response_times)
        max_time = max(response_times)
        min_time = min(response_times)
        
        print("\nPerformance Results:")
        print(f"Total Requests: {len(results)}")
        print(f"Successful Requests: {len(successful_requests)}")
        print(f"Failed Requests: {len(failed_requests)}")
        print(f"\nResponse Times:")
        print(f"Average: {avg_time:.2f}s")
        print(f"Maximum: {max_time:.2f}s")
        print(f"Minimum: {min_time:.2f}s")
    else:
        print("\nNo successful requests")
    
    if failed_requests:
        print("\nFailed Requests:")
        for req in failed_requests:
            print(f"Ticker: {req['ticker']}, Status: {req['status']}")
            if 'error' in req:
                print(f"Error: {req['error']}")

async def main():
    # Test cases
    test_cases = [
        # Popular tech stocks
        ["AAPL", "MSFT", "GOOGL"],
        # Mixed sector stocks
        ["JPM", "XOM", "PFE", "WMT", "BA"],
        # High volume test
        ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "JPM", "V", "JNJ"]
    ]
    
    for i, tickers in enumerate(test_cases, 1):
        print(f"\n=== Test Case {i}: {len(tickers)} tickers ===")
        await run_concurrent_tests(tickers)
        if i < len(test_cases):
            print("\nWaiting 5 seconds before next test case...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
