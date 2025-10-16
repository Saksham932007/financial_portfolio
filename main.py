"""
AI Financial Portfolio Manager Agent - Main Orchestrator
Coordinates all modules in a continuous monitoring loop
"""

import json
import time
import asyncio
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

from src.config import Config
from src.data_fetcher import MarketDataFetcher
from src.technical_analyzer import TechnicalAnalyzer
from src.sentiment_analyzer import SentimentAnalyzer
from src.recommendation_engine import RecommendationEngine
from src.risk_manager import RiskManager
from src.output_handler import OutputHandler
from src.utils.logger import PortfolioLogger


class PortfolioManagerAgent:
    """Main AI Financial Portfolio Manager Agent"""
    
    def __init__(self, portfolio_file: str = 'portfolio.json'):
        self.logger = PortfolioLogger.get_logger('portfolio_manager')
        
        # Initialize all modules
        self.data_fetcher = MarketDataFetcher()
        self.technical_analyzer = TechnicalAnalyzer()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.recommendation_engine = RecommendationEngine()
        self.risk_manager = RiskManager()
        self.output_handler = OutputHandler()
        
        # Load portfolio
        self.portfolio_file = portfolio_file
        self.portfolio = self._load_portfolio()
        
        self.logger.info(f"Portfolio Manager Agent initialized")
        self.logger.info(f"Loaded {len(self.portfolio)} tickers from portfolio")
        self.logger.info(f"Configuration: {Config.get_config_dict()}")
    
    def _load_portfolio(self) -> List[Dict[str, str]]:
        """Load portfolio from JSON file"""
        try:
            with open(self.portfolio_file, 'r') as f:
                data = json.load(f)
            
            # Combine all ticker lists
            tickers = []
            tickers.extend(data.get('portfolio', []))
            tickers.extend(data.get('watchlist', []))
            tickers.extend(data.get('forex', []))
            
            return tickers
            
        except FileNotFoundError:
            self.logger.error(f"Portfolio file not found: {self.portfolio_file}")
            return []
        except json.JSONDecodeError as e:
            self.logger.error(f"Error parsing portfolio file: {e}")
            return []
    
    def analyze_stock(self, ticker_info: Dict[str, str]) -> Dict[str, Any]:
        """
        Perform complete analysis for a single stock
        
        Args:
            ticker_info: Dictionary with ticker, name, and market
            
        Returns:
            Complete recommendation dictionary
        """
        ticker = ticker_info.get('ticker')
        name = ticker_info.get('name', ticker)
        
        self.logger.info(f"Starting analysis for {ticker} ({name})")
        
        try:
            # Step 1: Fetch live market data
            self.logger.info(f"[{ticker}] Step 1/5: Fetching live market data...")
            price_data = self.data_fetcher.get_live_price(ticker)
            
            if not price_data:
                self.logger.error(f"Failed to fetch price data for {ticker}")
                return None
            
            current_price = price_data['current_price']
            self.logger.info(f"[{ticker}] Current price: ${current_price:.2f}")
            
            # Step 2: Get historical data and perform technical analysis
            self.logger.info(f"[{ticker}] Step 2/5: Performing technical analysis...")
            historical_data = self.data_fetcher.get_historical_data(ticker, period='1y', interval='1d')
            
            technical_data = None
            if historical_data is not None and not historical_data.empty:
                technical_data = self.technical_analyzer.analyze(ticker, historical_data)
            
            if not technical_data:
                self.logger.warning(f"Technical analysis failed for {ticker}, using fallback")
                technical_data = self.technical_analyzer.get_quick_indicators(ticker, historical_data)
            
            # Step 3: Perform sentiment analysis
            self.logger.info(f"[{ticker}] Step 3/5: Analyzing news sentiment...")
            sentiment_data = self.sentiment_analyzer.analyze_sentiment(ticker, name)
            
            if not sentiment_data:
                self.logger.warning(f"Sentiment analysis failed for {ticker}, using fallback")
                sentiment_data = self.sentiment_analyzer.get_simple_sentiment(ticker)
            
            # Step 4: Calculate risk management levels
            self.logger.info(f"[{ticker}] Step 4/5: Calculating risk management levels...")
            risk_data = self.risk_manager.calculate_risk_levels(
                ticker,
                current_price,
                historical_data,
                technical_data
            )
            
            # Step 5: Generate recommendation
            self.logger.info(f"[{ticker}] Step 5/5: Generating trading recommendation...")
            recommendation = self.recommendation_engine.generate_recommendation(
                ticker,
                current_price,
                technical_data,
                sentiment_data,
                risk_data
            )
            
            if not recommendation:
                self.logger.error(f"Failed to generate recommendation for {ticker}")
                return None
            
            # Save and display recommendation
            self.output_handler.save_recommendation(recommendation)
            self.output_handler.print_recommendation(recommendation)
            
            self.logger.info(f"✅ Analysis complete for {ticker}")
            
            return recommendation
            
        except Exception as e:
            PortfolioLogger.log_error('PortfolioManagerAgent.analyze_stock', e, {
                'ticker': ticker
            })
            return None
    
    def run_analysis_cycle(self) -> List[Dict[str, Any]]:
        """
        Run one complete analysis cycle for all stocks in portfolio
        
        Returns:
            List of all recommendations
        """
        self.logger.info("\n" + "="*80)
        self.logger.info("🚀 Starting new analysis cycle")
        self.logger.info(f"Analyzing {len(self.portfolio)} tickers")
        self.logger.info("="*80 + "\n")
        
        recommendations = []
        
        for i, ticker_info in enumerate(self.portfolio, 1):
            ticker = ticker_info.get('ticker')
            self.logger.info(f"\n[{i}/{len(self.portfolio)}] Analyzing {ticker}...")
            
            recommendation = self.analyze_stock(ticker_info)
            
            if recommendation:
                recommendations.append(recommendation)
            
            # Brief pause between stocks to avoid rate limiting
            if i < len(self.portfolio):
                time.sleep(2)
        
        # Print summary
        self.logger.info("\n" + "="*80)
        self.logger.info("📊 Analysis Cycle Complete")
        self.logger.info("="*80)
        
        summary = self.output_handler.create_summary_report(recommendations)
        print(summary)
        
        return recommendations
    
    def run_continuous_monitoring(self):
        """
        Run continuous monitoring loop
        Analyzes portfolio at regular intervals
        """
        self.logger.info("\n" + "="*80)
        self.logger.info("🤖 AI FINANCIAL PORTFOLIO MANAGER AGENT")
        self.logger.info("="*80)
        self.logger.info(f"Monitoring {len(self.portfolio)} tickers")
        self.logger.info(f"Update interval: {Config.UPDATE_INTERVAL_SECONDS} seconds")
        self.logger.info(f"Confidence threshold: {Config.CONFIDENCE_THRESHOLD}%")
        self.logger.info("\n⚠️  DISCLAIMER: This is an AI-generated analysis and does NOT")
        self.logger.info("   constitute professional financial advice.\n")
        self.logger.info("="*80 + "\n")
        
        cycle_count = 0
        
        try:
            while True:
                cycle_count += 1
                self.logger.info(f"\n🔄 Starting cycle #{cycle_count} at {datetime.now()}")
                
                # Run analysis cycle
                recommendations = self.run_analysis_cycle()
                
                # Log cycle completion
                self.logger.info(f"\n✅ Cycle #{cycle_count} completed")
                self.logger.info(f"Generated {len(recommendations)} recommendations")
                
                # Wait for next cycle
                self.logger.info(f"\n⏳ Waiting {Config.UPDATE_INTERVAL_SECONDS} seconds until next cycle...")
                self.logger.info(f"   Next cycle will start at {datetime.now().replace(second=0, microsecond=0) + timedelta(seconds=Config.UPDATE_INTERVAL_SECONDS)}")
                
                time.sleep(Config.UPDATE_INTERVAL_SECONDS)
                
        except KeyboardInterrupt:
            self.logger.info("\n\n🛑 Agent stopped by user")
            self.logger.info(f"Total cycles completed: {cycle_count}")
            self.logger.info("Thank you for using AI Financial Portfolio Manager!")
        except Exception as e:
            PortfolioLogger.log_error('PortfolioManagerAgent.run_continuous_monitoring', e, {
                'cycle': cycle_count
            })
            raise
    
    def run_single_analysis(self, ticker: str = None):
        """
        Run a single analysis (for testing or manual use)
        
        Args:
            ticker: Optional specific ticker to analyze
        """
        if ticker:
            # Analyze specific ticker
            ticker_info = {'ticker': ticker, 'name': ticker, 'market': 'UNKNOWN'}
            self.analyze_stock(ticker_info)
        else:
            # Analyze all tickers once
            self.run_analysis_cycle()


from datetime import timedelta


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='AI Financial Portfolio Manager Agent',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                          # Run continuous monitoring
  python main.py --single                 # Run single analysis cycle
  python main.py --ticker AAPL            # Analyze specific stock
  python main.py --portfolio my_stocks.json  # Use custom portfolio file

⚠️  DISCLAIMER: This is an AI-generated analysis tool and does NOT constitute
   professional financial advice. Always do your own research and consult with
   a qualified financial advisor before making investment decisions.
        """
    )
    
    parser.add_argument(
        '--portfolio',
        default='portfolio.json',
        help='Path to portfolio JSON file (default: portfolio.json)'
    )
    parser.add_argument(
        '--single',
        action='store_true',
        help='Run a single analysis cycle instead of continuous monitoring'
    )
    parser.add_argument(
        '--ticker',
        help='Analyze a specific ticker symbol'
    )
    
    args = parser.parse_args()
    
    # Create and run agent
    agent = PortfolioManagerAgent(portfolio_file=args.portfolio)
    
    if args.ticker:
        agent.run_single_analysis(ticker=args.ticker)
    elif args.single:
        agent.run_single_analysis()
    else:
        agent.run_continuous_monitoring()


if __name__ == '__main__':
    main()
