"""
Logging utility for AI Financial Portfolio Manager
Provides structured logging for all agent operations
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from pythonjsonlogger import jsonlogger
from src.config import Config


class PortfolioLogger:
    """Custom logger for the portfolio manager agent"""
    
    _loggers = {}
    
    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """Get or create a logger instance"""
        
        if name in cls._loggers:
            return cls._loggers[name]
        
        # Create logger
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, Config.LOG_LEVEL))
        
        # Create logs directory if it doesn't exist
        log_dir = Path(Config.LOG_FILE).parent
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # File handler with JSON formatting
        file_handler = logging.FileHandler(Config.LOG_FILE)
        json_formatter = jsonlogger.JsonFormatter(
            '%(timestamp)s %(name)s %(levelname)s %(message)s',
            timestamp=True
        )
        file_handler.setFormatter(json_formatter)
        
        # Console handler with standard formatting
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        
        # Add handlers
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        # Store logger
        cls._loggers[name] = logger
        
        return logger
    
    @classmethod
    def log_market_data(cls, ticker: str, data: dict):
        """Log market data fetch"""
        logger = cls.get_logger('market_data')
        logger.info(f"Fetched market data for {ticker}", extra={'ticker': ticker, 'data': data})
    
    @classmethod
    def log_recommendation(cls, ticker: str, recommendation: dict):
        """Log trading recommendation"""
        logger = cls.get_logger('recommendations')
        logger.info(
            f"Generated {recommendation.get('recommendation', 'UNKNOWN')} recommendation for {ticker}",
            extra={'ticker': ticker, 'recommendation': recommendation}
        )
    
    @classmethod
    def log_api_call(cls, api_name: str, endpoint: str, success: bool, response_time: float = None):
        """Log API calls"""
        logger = cls.get_logger('api_calls')
        logger.info(
            f"API call to {api_name}",
            extra={
                'api': api_name,
                'endpoint': endpoint,
                'success': success,
                'response_time': response_time
            }
        )
    
    @classmethod
    def log_error(cls, component: str, error: Exception, context: dict = None):
        """Log errors with context"""
        logger = cls.get_logger('errors')
        logger.error(
            f"Error in {component}: {str(error)}",
            extra={
                'component': component,
                'error_type': type(error).__name__,
                'error_message': str(error),
                'context': context or {}
            },
            exc_info=True
        )
