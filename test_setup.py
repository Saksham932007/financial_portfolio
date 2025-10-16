"""
Simple test script to verify the agent setup
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        from src.config import Config
        print("✅ Config imported")
        
        from src.data_fetcher import MarketDataFetcher
        print("✅ MarketDataFetcher imported")
        
        from src.technical_analyzer import TechnicalAnalyzer
        print("✅ TechnicalAnalyzer imported")
        
        from src.sentiment_analyzer import SentimentAnalyzer
        print("✅ SentimentAnalyzer imported")
        
        from src.recommendation_engine import RecommendationEngine
        print("✅ RecommendationEngine imported")
        
        from src.risk_manager import RiskManager
        print("✅ RiskManager imported")
        
        from src.output_handler import OutputHandler
        print("✅ OutputHandler imported")
        
        from src.utils.logger import PortfolioLogger
        print("✅ PortfolioLogger imported")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False


def test_config():
    """Test configuration"""
    print("\nTesting configuration...")
    
    try:
        from src.config import Config
        
        # Check API key
        if Config.GEMINI_API_KEY:
            print(f"✅ Gemini API Key configured (length: {len(Config.GEMINI_API_KEY)})")
        else:
            print("⚠️  Gemini API Key not set - please add to .env file")
            return False
        
        print(f"✅ Update interval: {Config.UPDATE_INTERVAL_SECONDS}s")
        print(f"✅ Confidence threshold: {Config.CONFIDENCE_THRESHOLD}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False


def test_data_fetch():
    """Test basic data fetching"""
    print("\nTesting market data fetching...")
    
    try:
        from src.data_fetcher import MarketDataFetcher
        
        fetcher = MarketDataFetcher()
        
        # Try to fetch data for a well-known stock
        print("Fetching data for AAPL...")
        data = fetcher.get_live_price('AAPL')
        
        if data:
            print(f"✅ Successfully fetched AAPL data")
            print(f"   Price: ${data.get('current_price', 0):.2f}")
            print(f"   Volume: {data.get('volume', 0):,}")
            return True
        else:
            print("⚠️  Could not fetch data - may be outside market hours")
            return True  # Don't fail test for this
            
    except Exception as e:
        print(f"❌ Data fetch error: {e}")
        return False


def test_portfolio_file():
    """Test portfolio file exists and is valid"""
    print("\nTesting portfolio file...")
    
    try:
        import json
        
        if not os.path.exists('portfolio.json'):
            print("⚠️  portfolio.json not found - using default")
            return True
        
        with open('portfolio.json', 'r') as f:
            portfolio = json.load(f)
        
        total = len(portfolio.get('portfolio', [])) + \
                len(portfolio.get('watchlist', [])) + \
                len(portfolio.get('forex', []))
        
        print(f"✅ Portfolio file valid")
        print(f"   Total tickers: {total}")
        
        return True
        
    except Exception as e:
        print(f"❌ Portfolio file error: {e}")
        return False


def main():
    """Run all tests"""
    print("="*60)
    print("AI Financial Portfolio Manager - Setup Test")
    print("="*60)
    print()
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Configuration", test_config()))
    results.append(("Portfolio File", test_portfolio_file()))
    results.append(("Data Fetching", test_data_fetch()))
    
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {name}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "="*60)
    if all_passed:
        print("✅ All tests passed! You're ready to run the agent.")
        print("\nTo start the agent:")
        print("  python main.py")
        print("\nFor help:")
        print("  python main.py --help")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("  1. Run: pip install -r requirements.txt")
        print("  2. Add GEMINI_API_KEY to .env file")
        print("  3. Check internet connection")
    print("="*60)
    
    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())
