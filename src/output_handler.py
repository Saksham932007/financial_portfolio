"""
Output Handler
Formats and stores trading recommendations
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
from src.config import Config
from src.utils.logger import PortfolioLogger


class OutputHandler:
    """Handles output formatting and storage of recommendations"""
    
    def __init__(self, output_dir: str = 'output'):
        self.logger = PortfolioLogger.get_logger('output_handler')
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        self.recommendations_dir = self.output_dir / 'recommendations'
        self.recommendations_dir.mkdir(exist_ok=True)
        
        self.history_dir = self.output_dir / 'history'
        self.history_dir.mkdir(exist_ok=True)
        
        self.logger.info(f"OutputHandler initialized with output directory: {self.output_dir}")
    
    def format_recommendation(self, recommendation: Dict[str, Any]) -> str:
        """
        Format recommendation as pretty JSON string
        
        Args:
            recommendation: Recommendation dictionary
            
        Returns:
            Formatted JSON string
        """
        try:
            return json.dumps(recommendation, indent=2, default=str)
        except Exception as e:
            self.logger.error(f"Error formatting recommendation: {e}")
            return "{}"
    
    def save_recommendation(self, recommendation: Dict[str, Any]) -> bool:
        """
        Save recommendation to file
        
        Args:
            recommendation: Recommendation dictionary
            
        Returns:
            True if saved successfully
        """
        try:
            ticker = recommendation.get('ticker', 'UNKNOWN')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # Save individual recommendation
            filename = f"{ticker}_{timestamp}.json"
            filepath = self.recommendations_dir / filename
            
            with open(filepath, 'w') as f:
                json.dump(recommendation, f, indent=2, default=str)
            
            self.logger.info(f"Saved recommendation to {filepath}")
            
            # Append to history
            self._append_to_history(recommendation)
            
            return True
            
        except Exception as e:
            PortfolioLogger.log_error('OutputHandler.save_recommendation', e, {
                'ticker': recommendation.get('ticker')
            })
            return False
    
    def _append_to_history(self, recommendation: Dict[str, Any]):
        """Append recommendation to historical log"""
        try:
            ticker = recommendation.get('ticker', 'UNKNOWN')
            date = datetime.now().strftime('%Y%m%d')
            
            history_file = self.history_dir / f"{ticker}_{date}.jsonl"
            
            with open(history_file, 'a') as f:
                json.dump(recommendation, f, default=str)
                f.write('\n')
            
        except Exception as e:
            self.logger.error(f"Error appending to history: {e}")
    
    def print_recommendation(self, recommendation: Dict[str, Any]):
        """
        Print recommendation to console in a readable format
        
        Args:
            recommendation: Recommendation dictionary
        """
        try:
            print("\n" + "="*80)
            print(f"TRADING RECOMMENDATION - {recommendation.get('ticker', 'N/A')}")
            print("="*80)
            
            print(f"\n📊 Current Price: ${recommendation.get('current_price', 0):.2f}")
            print(f"⏰ Timestamp: {recommendation.get('timestamp', 'N/A')}")
            
            # Main recommendation
            rec = recommendation.get('recommendation', 'HOLD')
            confidence = recommendation.get('confidence_score', 0)
            
            emoji_map = {'BUY': '🟢', 'SELL': '🔴', 'HOLD': '🟡'}
            emoji = emoji_map.get(rec, '⚪')
            
            print(f"\n{emoji} RECOMMENDATION: {rec}")
            print(f"💪 Confidence Score: {confidence}%")
            
            # Reasoning
            reasoning = recommendation.get('reasoning', 'N/A')
            print(f"\n📝 Reasoning:\n{reasoning}")
            
            # Key factors
            key_factors = recommendation.get('key_factors', [])
            if key_factors:
                print(f"\n🔑 Key Factors:")
                for i, factor in enumerate(key_factors, 1):
                    print(f"   {i}. {factor}")
            
            # Risk management
            if 'risk_management' in recommendation:
                risk = recommendation['risk_management']
                print(f"\n⚠️  Risk Management:")
                print(f"   Stop Loss: ${risk.get('stop_loss', 0):.2f} ({risk.get('stop_loss_percent', 0):.2f}%)")
                print(f"   Take Profit 1: ${risk.get('take_profit_1', 0):.2f} ({risk.get('take_profit_1_percent', 0):.2f}%)")
                print(f"   Take Profit 2: ${risk.get('take_profit_2', 0):.2f} ({risk.get('take_profit_2_percent', 0):.2f}%)")
                print(f"   Risk/Reward: {risk.get('risk_reward_ratio_1', 0):.2f}")
            
            # Technical indicators
            if 'technical_data' in recommendation:
                tech = recommendation['technical_data']
                print(f"\n📈 Technical Indicators:")
                if 'rsi' in tech:
                    print(f"   RSI: {tech.get('rsi', 'N/A')} ({tech.get('rsi_signal', 'N/A')})")
                if 'macd_crossover' in tech:
                    print(f"   MACD: {tech.get('macd_crossover', 'N/A')}")
                if 'trend' in tech:
                    print(f"   Trend: {tech.get('trend', 'N/A')} ({tech.get('trend_strength', 'N/A')})")
            
            # Sentiment
            sentiment = recommendation.get('sentiment', 'neutral')
            sentiment_score = recommendation.get('sentiment_score', 0)
            print(f"\n💭 Sentiment: {sentiment.upper()} ({sentiment_score:.2f})")
            
            # Additional info
            timeframe = recommendation.get('timeframe', 'N/A')
            risk_level = recommendation.get('risk_level', 'N/A')
            print(f"\n⏱️  Timeframe: {timeframe}")
            print(f"🎯 Risk Level: {risk_level.upper()}")
            
            # Warnings
            warnings = recommendation.get('warnings', [])
            if warnings:
                print(f"\n⚠️  Warnings:")
                for warning in warnings:
                    print(f"   ⚠️  {warning}")
            
            # Disclaimer
            print("\n" + "-"*80)
            print("⚠️  DISCLAIMER: This is an AI-generated recommendation and does NOT")
            print("   constitute professional financial advice. Trade at your own risk.")
            print("="*80 + "\n")
            
        except Exception as e:
            PortfolioLogger.log_error('OutputHandler.print_recommendation', e, {
                'ticker': recommendation.get('ticker')
            })
    
    def get_latest_recommendation(self, ticker: str) -> Dict[str, Any]:
        """
        Get the latest recommendation for a ticker
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Latest recommendation or empty dict
        """
        try:
            # Find all recommendation files for this ticker
            files = sorted(self.recommendations_dir.glob(f"{ticker}_*.json"), reverse=True)
            
            if not files:
                return {}
            
            # Read the most recent file
            with open(files[0], 'r') as f:
                return json.load(f)
                
        except Exception as e:
            self.logger.error(f"Error getting latest recommendation: {e}")
            return {}
    
    def get_recommendation_history(self, ticker: str, days: int = 7) -> List[Dict[str, Any]]:
        """
        Get recommendation history for a ticker
        
        Args:
            ticker: Stock ticker symbol
            days: Number of days to look back
            
        Returns:
            List of recommendations
        """
        try:
            recommendations = []
            
            # Check history files for the specified period
            for i in range(days):
                date = (datetime.now() - timedelta(days=i)).strftime('%Y%m%d')
                history_file = self.history_dir / f"{ticker}_{date}.jsonl"
                
                if history_file.exists():
                    with open(history_file, 'r') as f:
                        for line in f:
                            try:
                                recommendations.append(json.loads(line))
                            except json.JSONDecodeError:
                                continue
            
            return sorted(recommendations, key=lambda x: x.get('timestamp', ''), reverse=True)
            
        except Exception as e:
            self.logger.error(f"Error getting recommendation history: {e}")
            return []
    
    def create_summary_report(self, recommendations: List[Dict[str, Any]]) -> str:
        """
        Create a summary report of multiple recommendations
        
        Args:
            recommendations: List of recommendations
            
        Returns:
            Formatted summary report
        """
        try:
            report = "\n" + "="*80 + "\n"
            report += "PORTFOLIO SUMMARY REPORT\n"
            report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            report += "="*80 + "\n\n"
            
            buy_count = sum(1 for r in recommendations if r.get('recommendation') == 'BUY')
            sell_count = sum(1 for r in recommendations if r.get('recommendation') == 'SELL')
            hold_count = sum(1 for r in recommendations if r.get('recommendation') == 'HOLD')
            
            report += f"Total Stocks Analyzed: {len(recommendations)}\n"
            report += f"🟢 BUY Signals: {buy_count}\n"
            report += f"🔴 SELL Signals: {sell_count}\n"
            report += f"🟡 HOLD Signals: {hold_count}\n\n"
            
            # List by recommendation type
            for rec_type in ['BUY', 'SELL', 'HOLD']:
                stocks = [r for r in recommendations if r.get('recommendation') == rec_type]
                if stocks:
                    report += f"\n{rec_type} Recommendations:\n"
                    report += "-" * 40 + "\n"
                    for stock in sorted(stocks, key=lambda x: x.get('confidence_score', 0), reverse=True):
                        ticker = stock.get('ticker', 'N/A')
                        price = stock.get('current_price', 0)
                        confidence = stock.get('confidence_score', 0)
                        report += f"  {ticker}: ${price:.2f} (Confidence: {confidence}%)\n"
            
            report += "\n" + "="*80 + "\n"
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error creating summary report: {e}")
            return "Error generating report"


from datetime import timedelta
