"""
Real-time Market Data Fetcher
Fetches live stock prices and forex data using yfinance and other APIs
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import time
from src.config import Config
from src.utils.logger import PortfolioLogger


class MarketDataFetcher:
    """Fetches real-time market data for stocks and forex"""
    
    def __init__(self):
        self.logger = PortfolioLogger.get_logger('market_data_fetcher')
        self.cache = {}
        self.cache_duration = 60  # Cache data for 60 seconds
    
    def get_live_price(self, ticker: str) -> Optional[Dict[str, Any]]:
        """
        Get current live price and basic info for a ticker
        
        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL', 'EURUSD=X')
            
        Returns:
            Dictionary with current price data or None if failed
        """
        try:
            start_time = time.time()
            
            # Check cache first
            cache_key = f"{ticker}_live"
            if cache_key in self.cache:
                cached_data, cached_time = self.cache[cache_key]
                if time.time() - cached_time < self.cache_duration:
                    self.logger.info(f"Using cached data for {ticker}")
                    return cached_data
            
            # Fetch from yfinance
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Get current price data
            hist = stock.history(period='1d', interval='1m')
            
            if hist.empty:
                self.logger.warning(f"No recent data available for {ticker}")
                return None
            
            latest = hist.iloc[-1]
            
            price_data = {
                'ticker': ticker,
                'timestamp': datetime.now().isoformat(),
                'current_price': float(latest['Close']),
                'open': float(latest['Open']),
                'high': float(latest['High']),
                'low': float(latest['Low']),
                'volume': int(latest['Volume']) if not pd.isna(latest['Volume']) else 0,
                'previous_close': float(info.get('previousClose', latest['Close'])),
                'day_high': float(hist['High'].max()),
                'day_low': float(hist['Low'].min()),
                'change': 0.0,
                'change_percent': 0.0
            }
            
            # Calculate change
            if price_data['previous_close'] > 0:
                price_data['change'] = price_data['current_price'] - price_data['previous_close']
                price_data['change_percent'] = (price_data['change'] / price_data['previous_close']) * 100
            
            # Cache the data
            self.cache[cache_key] = (price_data, time.time())
            
            response_time = time.time() - start_time
            PortfolioLogger.log_api_call('yfinance', f'live_price/{ticker}', True, response_time)
            PortfolioLogger.log_market_data(ticker, price_data)
            
            return price_data
            
        except Exception as e:
            PortfolioLogger.log_error('MarketDataFetcher.get_live_price', e, {'ticker': ticker})
            return None
    
    def get_historical_data(self, ticker: str, period: str = '1y', interval: str = '1d') -> Optional[pd.DataFrame]:
        """
        Get historical price data for technical analysis
        
        Args:
            ticker: Stock ticker symbol
            period: Data period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            interval: Data interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
            
        Returns:
            DataFrame with historical OHLCV data or None if failed
        """
        try:
            start_time = time.time()
            
            # Check cache
            cache_key = f"{ticker}_hist_{period}_{interval}"
            if cache_key in self.cache:
                cached_data, cached_time = self.cache[cache_key]
                if time.time() - cached_time < self.cache_duration:
                    self.logger.info(f"Using cached historical data for {ticker}")
                    return cached_data
            
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period, interval=interval)
            
            if hist.empty:
                self.logger.warning(f"No historical data available for {ticker}")
                return None
            
            # Clean the data
            hist = hist.dropna()
            
            # Cache the data
            self.cache[cache_key] = (hist, time.time())
            
            response_time = time.time() - start_time
            PortfolioLogger.log_api_call('yfinance', f'historical/{ticker}', True, response_time)
            
            self.logger.info(f"Fetched {len(hist)} historical data points for {ticker}")
            
            return hist
            
        except Exception as e:
            PortfolioLogger.log_error('MarketDataFetcher.get_historical_data', e, {
                'ticker': ticker,
                'period': period,
                'interval': interval
            })
            return None
    
    def get_multiple_tickers(self, tickers: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Get live price data for multiple tickers
        
        Args:
            tickers: List of ticker symbols
            
        Returns:
            Dictionary mapping ticker to price data
        """
        results = {}
        
        for ticker in tickers:
            price_data = self.get_live_price(ticker)
            if price_data:
                results[ticker] = price_data
            else:
                self.logger.warning(f"Failed to fetch data for {ticker}")
        
        return results
    
    def get_intraday_data(self, ticker: str, days: int = 5) -> Optional[pd.DataFrame]:
        """
        Get detailed intraday data for recent analysis
        
        Args:
            ticker: Stock ticker symbol
            days: Number of days to fetch (max 7 for minute data)
            
        Returns:
            DataFrame with minute-level data
        """
        try:
            period_map = {1: '1d', 2: '2d', 5: '5d', 7: '7d'}
            period = period_map.get(days, '5d')
            
            return self.get_historical_data(ticker, period=period, interval='1m')
            
        except Exception as e:
            PortfolioLogger.log_error('MarketDataFetcher.get_intraday_data', e, {
                'ticker': ticker,
                'days': days
            })
            return None
    
    def clear_cache(self):
        """Clear all cached data"""
        self.cache.clear()
        self.logger.info("Market data cache cleared")
