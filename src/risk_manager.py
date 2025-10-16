"""
Risk Management Module
Calculates stop-loss and take-profit levels based on volatility and technical analysis
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, Tuple
from datetime import datetime
from src.config import Config
from src.utils.logger import PortfolioLogger


class RiskManager:
    """Manages risk calculations for trading recommendations"""
    
    def __init__(self):
        self.logger = PortfolioLogger.get_logger('risk_manager')
        self.logger.info("RiskManager initialized")
    
    def calculate_risk_levels(
        self,
        ticker: str,
        current_price: float,
        price_data: pd.DataFrame,
        technical_data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Calculate stop-loss and take-profit levels
        
        Args:
            ticker: Stock ticker symbol
            current_price: Current stock price
            price_data: Historical price data
            technical_data: Technical analysis results (optional)
            
        Returns:
            Dictionary with risk management levels
        """
        try:
            if price_data is None or price_data.empty:
                self.logger.warning(f"No price data for risk calculation: {ticker}")
                return self._get_default_risk_levels(current_price)
            
            # Calculate volatility-based levels
            volatility = self._calculate_volatility(price_data)
            atr = self._calculate_atr(price_data)
            
            # Get support/resistance from technical data if available
            support_levels = []
            resistance_levels = []
            
            if technical_data and 'support_resistance' in technical_data:
                support_levels = technical_data['support_resistance'].get('support_levels', [])
                resistance_levels = technical_data['support_resistance'].get('resistance_levels', [])
            
            # Calculate stop-loss
            stop_loss = self._calculate_stop_loss(
                current_price,
                volatility,
                atr,
                support_levels
            )
            
            # Calculate take-profit levels
            tp1, tp2 = self._calculate_take_profit_levels(
                current_price,
                volatility,
                atr,
                resistance_levels
            )
            
            # Calculate risk-reward ratio
            risk = abs(current_price - stop_loss)
            reward1 = abs(tp1 - current_price)
            reward2 = abs(tp2 - current_price)
            
            risk_reward_1 = reward1 / risk if risk > 0 else 0
            risk_reward_2 = reward2 / risk if risk > 0 else 0
            
            risk_data = {
                'ticker': ticker,
                'current_price': round(current_price, 2),
                'stop_loss': round(stop_loss, 2),
                'take_profit_1': round(tp1, 2),
                'take_profit_2': round(tp2, 2),
                'stop_loss_percent': round(((stop_loss - current_price) / current_price) * 100, 2),
                'take_profit_1_percent': round(((tp1 - current_price) / current_price) * 100, 2),
                'take_profit_2_percent': round(((tp2 - current_price) / current_price) * 100, 2),
                'risk_reward_ratio_1': round(risk_reward_1, 2),
                'risk_reward_ratio_2': round(risk_reward_2, 2),
                'volatility': round(volatility * 100, 2),
                'atr': round(atr, 2),
                'timestamp': datetime.now().isoformat()
            }
            
            self.logger.info(
                f"Risk levels calculated for {ticker}: "
                f"SL={risk_data['stop_loss']}, TP1={risk_data['take_profit_1']}, TP2={risk_data['take_profit_2']}"
            )
            
            return risk_data
            
        except Exception as e:
            PortfolioLogger.log_error('RiskManager.calculate_risk_levels', e, {'ticker': ticker})
            return self._get_default_risk_levels(current_price)
    
    def _calculate_volatility(self, price_data: pd.DataFrame, period: int = 20) -> float:
        """Calculate historical volatility (standard deviation of returns)"""
        try:
            returns = price_data['Close'].pct_change().dropna()
            volatility = returns.tail(period).std()
            return volatility
        except Exception:
            return 0.02  # Default 2% volatility
    
    def _calculate_atr(self, price_data: pd.DataFrame, period: int = 14) -> float:
        """Calculate Average True Range (ATR) for volatility measurement"""
        try:
            high = price_data['High']
            low = price_data['Low']
            close = price_data['Close']
            
            # True Range calculation
            tr1 = high - low
            tr2 = abs(high - close.shift())
            tr3 = abs(low - close.shift())
            
            tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            atr = tr.tail(period).mean()
            
            return atr
            
        except Exception:
            # Fallback: use simple high-low range
            try:
                return (price_data['High'] - price_data['Low']).tail(14).mean()
            except Exception:
                return 0.0
    
    def _calculate_stop_loss(
        self,
        current_price: float,
        volatility: float,
        atr: float,
        support_levels: list
    ) -> float:
        """Calculate optimal stop-loss level"""
        
        # Method 1: Volatility-based (2 * ATR below current price)
        sl_atr = current_price - (2 * atr)
        
        # Method 2: Percentage-based
        sl_percent = current_price * (1 - Config.DEFAULT_STOP_LOSS_PERCENTAGE / 100)
        
        # Method 3: Support-based (nearest support level minus small buffer)
        sl_support = current_price * 0.95  # Default 5% below
        if support_levels:
            nearest_support = max([s for s in support_levels if s < current_price], default=None)
            if nearest_support:
                sl_support = nearest_support * 0.99  # 1% below support
        
        # Use the most conservative (highest) stop-loss
        stop_loss = max(sl_atr, sl_percent, sl_support)
        
        # Ensure stop-loss is below current price
        if stop_loss >= current_price:
            stop_loss = current_price * 0.95
        
        return stop_loss
    
    def _calculate_take_profit_levels(
        self,
        current_price: float,
        volatility: float,
        atr: float,
        resistance_levels: list
    ) -> Tuple[float, float]:
        """Calculate two take-profit levels"""
        
        # TP1: Conservative target (1.5x risk or nearest resistance)
        tp1_atr = current_price + (3 * atr)
        tp1_percent = current_price * (1 + Config.DEFAULT_TAKE_PROFIT_1_PERCENTAGE / 100)
        
        tp1_resistance = current_price * 1.10  # Default 10% above
        if resistance_levels:
            nearest_resistance = min([r for r in resistance_levels if r > current_price], default=None)
            if nearest_resistance:
                tp1_resistance = nearest_resistance * 0.99  # Just below resistance
        
        tp1 = min(tp1_atr, tp1_percent, tp1_resistance)
        if tp1 <= current_price:
            tp1 = current_price * 1.10
        
        # TP2: Aggressive target (3x risk or next resistance)
        tp2_atr = current_price + (5 * atr)
        tp2_percent = current_price * (1 + Config.DEFAULT_TAKE_PROFIT_2_PERCENTAGE / 100)
        
        tp2_resistance = current_price * 1.20  # Default 20% above
        if resistance_levels and len(resistance_levels) > 1:
            next_resistance = sorted([r for r in resistance_levels if r > tp1])
            if next_resistance:
                tp2_resistance = next_resistance[0] * 0.99
        
        tp2 = min(tp2_atr, tp2_percent, tp2_resistance)
        if tp2 <= tp1:
            tp2 = tp1 * 1.15
        
        return tp1, tp2
    
    def _get_default_risk_levels(self, current_price: float) -> Dict[str, Any]:
        """Return default risk levels when calculation fails"""
        
        stop_loss = current_price * (1 - Config.DEFAULT_STOP_LOSS_PERCENTAGE / 100)
        tp1 = current_price * (1 + Config.DEFAULT_TAKE_PROFIT_1_PERCENTAGE / 100)
        tp2 = current_price * (1 + Config.DEFAULT_TAKE_PROFIT_2_PERCENTAGE / 100)
        
        return {
            'current_price': round(current_price, 2),
            'stop_loss': round(stop_loss, 2),
            'take_profit_1': round(tp1, 2),
            'take_profit_2': round(tp2, 2),
            'stop_loss_percent': -Config.DEFAULT_STOP_LOSS_PERCENTAGE,
            'take_profit_1_percent': Config.DEFAULT_TAKE_PROFIT_1_PERCENTAGE,
            'take_profit_2_percent': Config.DEFAULT_TAKE_PROFIT_2_PERCENTAGE,
            'risk_reward_ratio_1': 2.0,
            'risk_reward_ratio_2': 4.0,
            'volatility': 0.0,
            'atr': 0.0,
            'default': True,
            'timestamp': datetime.now().isoformat()
        }
    
    def validate_risk_reward(self, risk_data: Dict[str, Any], min_ratio: float = 1.5) -> bool:
        """
        Validate if risk-reward ratio meets minimum threshold
        
        Args:
            risk_data: Risk calculation results
            min_ratio: Minimum acceptable risk-reward ratio
            
        Returns:
            True if risk-reward is acceptable
        """
        rr1 = risk_data.get('risk_reward_ratio_1', 0)
        return rr1 >= min_ratio
