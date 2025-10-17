"""
Configuration Management for AI Financial Portfolio Manager
Loads environment variables and manages agent settings
"""

import os
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables
load_dotenv()


class Config:
    """Central configuration class for the portfolio manager agent"""
    
    # API Keys
    GEMINI_API_KEY: str = os.getenv('GEMINI_API_KEY', '')
    ALPHA_VANTAGE_API_KEY: str = os.getenv('ALPHA_VANTAGE_API_KEY', '')
    
    # Agent Operational Settings
    UPDATE_INTERVAL_SECONDS: int = int(os.getenv('UPDATE_INTERVAL_SECONDS', '60'))
    CONFIDENCE_THRESHOLD: int = int(os.getenv('CONFIDENCE_THRESHOLD', '70'))
    MAX_CONCURRENT_STOCKS: int = int(os.getenv('MAX_CONCURRENT_STOCKS', '10'))
    
    # Risk Management Defaults
    DEFAULT_STOP_LOSS_PERCENTAGE: float = float(os.getenv('DEFAULT_STOP_LOSS_PERCENTAGE', '5.0'))
    DEFAULT_TAKE_PROFIT_1_PERCENTAGE: float = float(os.getenv('DEFAULT_TAKE_PROFIT_1_PERCENTAGE', '10.0'))
    DEFAULT_TAKE_PROFIT_2_PERCENTAGE: float = float(os.getenv('DEFAULT_TAKE_PROFIT_2_PERCENTAGE', '20.0'))
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE: str = os.getenv('LOG_FILE', 'logs/portfolio_agent.log')
    
    # Technical Analysis Parameters
    RSI_PERIOD: int = 14
    RSI_OVERBOUGHT: float = 70.0
    RSI_OVERSOLD: float = 30.0
    
    MACD_FAST_PERIOD: int = 12
    MACD_SLOW_PERIOD: int = 26
    MACD_SIGNAL_PERIOD: int = 9
    
    BOLLINGER_PERIOD: int = 20
    BOLLINGER_STD_DEV: float = 2.0
    
    MA_PERIODS: list = [50, 100, 200]
    
    # News & Sentiment Analysis
    NEWS_LOOKBACK_HOURS: int = 24
    MAX_NEWS_ARTICLES: int = 5
    
    # Gemini Model Configuration
    GEMINI_MODEL: str = "gemini-2.5-flash"
    GEMINI_TEMPERATURE: float = 0.7
    GEMINI_MAX_OUTPUT_TOKENS: int = 2048
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that all required configuration is present"""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required but not set in environment variables")
        return True
    
    @classmethod
    def get_config_dict(cls) -> Dict[str, Any]:
        """Return configuration as dictionary for logging purposes"""
        return {
            'update_interval': cls.UPDATE_INTERVAL_SECONDS,
            'confidence_threshold': cls.CONFIDENCE_THRESHOLD,
            'max_concurrent_stocks': cls.MAX_CONCURRENT_STOCKS,
            'rsi_period': cls.RSI_PERIOD,
            'macd_periods': f"{cls.MACD_FAST_PERIOD}/{cls.MACD_SLOW_PERIOD}/{cls.MACD_SIGNAL_PERIOD}",
            'bollinger_period': cls.BOLLINGER_PERIOD,
            'ma_periods': cls.MA_PERIODS,
        }


# Validate configuration on import
Config.validate()
