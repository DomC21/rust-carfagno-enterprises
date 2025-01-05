import sys
import os
from dotenv import load_dotenv

# Add the backend directory to Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Load environment variables
load_dotenv()

print("Python path:", sys.path)
print("\nTesting imports...")

try:
    # Test all required imports
    from app.services.news_service import get_news_articles
    print("✓ Successfully imported news_service")
    from app.services.analysis_service import analyze_articles
    print("✓ Successfully imported analysis_service")
    from app.services.report_service import generate_report
    print("✓ Successfully imported report_service")
    from app.models import StockAnalysisRequest, StockAnalysisResponse
    print("✓ Successfully imported models")
    
    print("\nAll imports successful!")
    
    # Test environment variables
    required_vars = ['NEWS_API_KEY', 'OPENAI_API_KEY', 'CORS_ORIGINS']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"\nWarning: Missing environment variables: {', '.join(missing_vars)}")
    else:
        print("\nAll required environment variables are set!")

except ImportError as e:
    print(f"Error importing modules: {str(e)}")
    sys.exit(1)
except Exception as e:
    print(f"Other error: {str(e)}")
    sys.exit(1)
