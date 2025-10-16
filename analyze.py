#!/usr/bin/env python3
"""
Quick analysis script for single stock
Usage: python analyze.py AAPL
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.data_fetcher import MarketDataFetcher
from src.technical_analyzer import TechnicalAnalyzer
from src.sentiment_analyzer import SentimentAnalyzer
from src.recommendation_engine import RecommendationEngine
from src.risk_manager import RiskManager
from src.output_handler import OutputHandler


def quick_analyze(ticker: str):
    """Quickly analyze a single stock"""
    
    print(f"\n🔍 Quick Analysis for {ticker}")
    print("="*60)
    
    try:
        # Initialize
        fetcher = MarketDataFetcher()
        tech_analyzer = TechnicalAnalyzer()
        sent_analyzer = SentimentAnalyzer()
        risk_mgr = RiskManager()
        rec_engine = RecommendationEngine()
        output = OutputHandler()
        
        # Fetch data
        print(f"\n📊 Fetching market data...")
        price_data = fetcher.get_live_price(ticker)
        if not price_data:
            print(f"❌ Could not fetch data for {ticker}")
            return
        
        current_price = price_data['current_price']
        print(f"✅ Current price: ${current_price:.2f}")
        
        # Historical data
        print(f"\n📈 Fetching historical data...")
        historical = fetcher.get_historical_data(ticker, period='1y')
        if historical is None or historical.empty:
            print("⚠️  Limited historical data available")
            return
        print(f"✅ Got {len(historical)} data points")
        
        # Technical analysis
        print(f"\n🔧 Running technical analysis...")
        technical = tech_analyzer.analyze(ticker, historical)
        if technical:
            print(f"✅ Technical analysis complete")
            if 'rsi' in technical:
                print(f"   RSI: {technical['rsi'].get('value', 'N/A')}")
            if 'trend' in technical:
                print(f"   Trend: {technical['trend'].get('direction', 'N/A')}")
        else:
            print("⚠️  Using fallback technical analysis")
            technical = tech_analyzer.get_quick_indicators(ticker, historical)
        
        # Sentiment analysis
        print(f"\n💭 Analyzing news sentiment...")
        sentiment = sent_analyzer.analyze_sentiment(ticker)
        if sentiment:
            print(f"✅ Sentiment: {sentiment.get('overall_sentiment', 'N/A')}")
            print(f"   Score: {sentiment.get('sentiment_score', 0):.2f}")
        else:
            print("⚠️  Using simple sentiment analysis")
            sentiment = sent_analyzer.get_simple_sentiment(ticker)
        
        # Risk management
        print(f"\n⚠️  Calculating risk levels...")
        risk = risk_mgr.calculate_risk_levels(ticker, current_price, historical, technical)
        print(f"✅ Stop Loss: ${risk.get('stop_loss', 0):.2f}")
        print(f"   Take Profit 1: ${risk.get('take_profit_1', 0):.2f}")
        print(f"   Take Profit 2: ${risk.get('take_profit_2', 0):.2f}")
        
        # Generate recommendation
        print(f"\n🎯 Generating recommendation...")
        recommendation = rec_engine.generate_recommendation(
            ticker,
            current_price,
            technical,
            sentiment,
            risk
        )
        
        if recommendation:
            print(f"\n")
            output.print_recommendation(recommendation)
            
            # Save
            output.save_recommendation(recommendation)
            print(f"\n💾 Recommendation saved to output/recommendations/")
        else:
            print("❌ Failed to generate recommendation")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Main entry point"""
    
    if len(sys.argv) < 2:
        print("\n❌ Usage: python analyze.py TICKER")
        print("\nExample:")
        print("  python analyze.py AAPL")
        print("  python analyze.py MSFT")
        print("  python analyze.py EURUSD=X")
        sys.exit(1)
    
    ticker = sys.argv[1].upper()
    quick_analyze(ticker)


if __name__ == '__main__':
    main()
