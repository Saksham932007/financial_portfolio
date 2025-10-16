"""
Technical Analysis Module using Gemini API
Performs technical indicator calculations via Gemini AI
"""

import google.generativeai as genai
import pandas as pd
from typing import Dict, Any, Optional
import json
from datetime import datetime
from src.config import Config
from src.utils.logger import PortfolioLogger


class TechnicalAnalyzer:
    """Performs technical analysis using Gemini API"""
    
    def __init__(self):
        self.logger = PortfolioLogger.get_logger('technical_analyzer')
        
        # Configure Gemini
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
        
        self.logger.info("TechnicalAnalyzer initialized with Gemini API")
    
    def analyze(self, ticker: str, price_data: pd.DataFrame) -> Optional[Dict[str, Any]]:
        """
        Perform comprehensive technical analysis using Gemini API
        
        Args:
            ticker: Stock ticker symbol
            price_data: DataFrame with OHLCV data
            
        Returns:
            Dictionary with technical indicators or None if failed
        """
        try:
            if price_data is None or price_data.empty:
                self.logger.warning(f"No price data available for {ticker}")
                return None
            
            # Prepare price data for Gemini
            price_list = price_data['Close'].tail(200).tolist()
            high_list = price_data['High'].tail(200).tolist()
            low_list = price_data['Low'].tail(200).tolist()
            volume_list = price_data['Volume'].tail(200).tolist()
            
            # Create comprehensive prompt for Gemini
            prompt = self._create_technical_analysis_prompt(
                ticker, price_list, high_list, low_list, volume_list
            )
            
            # Call Gemini API
            self.logger.info(f"Sending technical analysis request to Gemini for {ticker}")
            response = self.model.generate_content(prompt)
            
            # Parse response
            technical_data = self._parse_gemini_response(response.text)
            
            if technical_data:
                technical_data['ticker'] = ticker
                technical_data['timestamp'] = datetime.now().isoformat()
                technical_data['data_points'] = len(price_list)
                
                self.logger.info(f"Technical analysis completed for {ticker}")
                PortfolioLogger.log_api_call('gemini', 'technical_analysis', True)
                
                return technical_data
            else:
                self.logger.warning(f"Failed to parse Gemini response for {ticker}")
                return None
                
        except Exception as e:
            PortfolioLogger.log_error('TechnicalAnalyzer.analyze', e, {'ticker': ticker})
            return None
    
    def _create_technical_analysis_prompt(
        self, 
        ticker: str,
        prices: list,
        highs: list,
        lows: list,
        volumes: list
    ) -> str:
        """Create detailed prompt for Gemini technical analysis"""
        
        prompt = f"""You are an expert quantitative analyst. Analyze the following stock price data for {ticker} and calculate technical indicators.

**Price Data (Most Recent {len(prices)} periods):**
- Closing Prices: {prices[-50:]}  (showing last 50 of {len(prices)})
- High Prices: {highs[-50:]}
- Low Prices: {lows[-50:]}
- Volume: {volumes[-50:]}

**Required Calculations:**

1. **RSI (Relative Strength Index)**
   - Period: {Config.RSI_PERIOD}
   - Calculate current RSI value
   - Determine if overbought (>{Config.RSI_OVERBOUGHT}) or oversold (<{Config.RSI_OVERSOLD})

2. **MACD (Moving Average Convergence Divergence)**
   - Fast Period: {Config.MACD_FAST_PERIOD}
   - Slow Period: {Config.MACD_SLOW_PERIOD}
   - Signal Period: {Config.MACD_SIGNAL_PERIOD}
   - Calculate: MACD line, Signal line, Histogram
   - Determine bullish or bearish crossover

3. **Bollinger Bands**
   - Period: {Config.BOLLINGER_PERIOD}
   - Standard Deviation: {Config.BOLLINGER_STD_DEV}
   - Calculate: Upper Band, Middle Band (SMA), Lower Band
   - Current price position relative to bands

4. **Moving Averages**
   - Calculate SMA for periods: {Config.MA_PERIODS}
   - Calculate EMA for periods: {Config.MA_PERIODS}
   - Identify golden cross or death cross patterns

5. **Support and Resistance Levels**
   - Identify key support levels (at least 2)
   - Identify key resistance levels (at least 2)

6. **Trend Analysis**
   - Overall trend: Uptrend, Downtrend, or Sideways
   - Trend strength: Strong, Moderate, or Weak

**Output Format (JSON only, no additional text):**
```json
{{
  "rsi": {{
    "value": <float>,
    "signal": "overbought|neutral|oversold",
    "interpretation": "<brief explanation>"
  }},
  "macd": {{
    "macd_line": <float>,
    "signal_line": <float>,
    "histogram": <float>,
    "crossover": "bullish|bearish|none",
    "interpretation": "<brief explanation>"
  }},
  "bollinger_bands": {{
    "upper": <float>,
    "middle": <float>,
    "lower": <float>,
    "price_position": "above_upper|within_bands|below_lower",
    "interpretation": "<brief explanation>"
  }},
  "moving_averages": {{
    "sma_50": <float>,
    "sma_100": <float>,
    "sma_200": <float>,
    "ema_50": <float>,
    "ema_100": <float>,
    "ema_200": <float>,
    "golden_cross": <boolean>,
    "death_cross": <boolean>
  }},
  "support_resistance": {{
    "support_levels": [<float>, <float>],
    "resistance_levels": [<float>, <float>]
  }},
  "trend": {{
    "direction": "uptrend|downtrend|sideways",
    "strength": "strong|moderate|weak",
    "interpretation": "<brief explanation>"
  }},
  "overall_signal": "bullish|bearish|neutral"
}}
```

Provide ONLY the JSON response, no additional commentary."""

        return prompt
    
    def _parse_gemini_response(self, response_text: str) -> Optional[Dict[str, Any]]:
        """Parse Gemini's JSON response"""
        try:
            # Extract JSON from response
            response_text = response_text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            
            # Parse JSON
            data = json.loads(response_text)
            
            return data
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse Gemini response as JSON: {e}")
            self.logger.debug(f"Response text: {response_text[:500]}")
            return None
        except Exception as e:
            self.logger.error(f"Error parsing Gemini response: {e}")
            return None
    
    def get_quick_indicators(self, ticker: str, price_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Get simplified technical indicators for quick analysis
        (Uses local calculation as fallback)
        """
        try:
            if price_data is None or price_data.empty:
                return {}
            
            latest_price = float(price_data['Close'].iloc[-1])
            
            # Calculate simple moving averages locally as backup
            sma_50 = float(price_data['Close'].tail(50).mean())
            sma_200 = float(price_data['Close'].tail(200).mean()) if len(price_data) >= 200 else None
            
            return {
                'current_price': latest_price,
                'sma_50': sma_50,
                'sma_200': sma_200,
                'above_sma_50': latest_price > sma_50,
                'above_sma_200': latest_price > sma_200 if sma_200 else None,
            }
            
        except Exception as e:
            PortfolioLogger.log_error('TechnicalAnalyzer.get_quick_indicators', e, {'ticker': ticker})
            return {}
