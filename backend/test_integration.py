import asyncio
import json
import aiohttp
import sys
from datetime import datetime

API_URL = "https://rust-carfagno-enterprises-3.onrender.com"
TEST_TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]

async def test_health():
    print("\nTesting Health Check...")
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/api/health") as response:
            print(f"Status: {response.status}")
            if response.status == 200:
                data = await response.json()
                print(f"Response: {json.dumps(data, indent=2)}")
            return response.status == 200

async def test_stock_analysis(ticker):
    print(f"\nTesting Stock Analysis for {ticker}...")
    async with aiohttp.ClientSession() as session:
        payload = {"ticker": ticker, "days": 7}
        async with session.post(f"{API_URL}/api/analyze", json=payload) as response:
            print(f"Status: {response.status}")
            if response.status == 200:
                data = await response.json()
                print(f"Articles analyzed: {len(data['articles'])}")
                print(f"Overall sentiment: {data['overall_sentiment']}")
                return True
            else:
                error = await response.text()
                print(f"Error: {error}")
                return False

async def main():
    print(f"Starting integration tests at {datetime.now().isoformat()}")
    print(f"Testing API at: {API_URL}")
    
    # Test health check
    health_ok = await test_health()
    if not health_ok:
        print("❌ Health check failed")
        sys.exit(1)
    print("✅ Health check passed")
    
    # Test stock analysis for multiple tickers
    results = []
    for ticker in TEST_TICKERS:
        success = await test_stock_analysis(ticker)
        results.append((ticker, success))
        await asyncio.sleep(1)  # Rate limiting
    
    # Print summary
    print("\nTest Summary:")
    all_passed = True
    for ticker, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {ticker}")
        if not success:
            all_passed = False
    
    if all_passed:
        print("\nAll tests passed!")
        sys.exit(0)
    else:
        print("\nSome tests failed.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
