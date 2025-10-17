"""
Recommendation Engine
Synthesizes technical and sentiment data using Gemini API to generate trading recommendations
"""

import google.generativeai as genai
from typing import Dict, Any, Optional
import json
from datetime import datetime
from src.config import Config
from src.utils.logger import PortfolioLogger


class RecommendationEngine:
    """Generates trading recommendations using Gemini API"""
    
    def __init__(self):
        self.logger = PortfolioLogger.get_logger('recommendation_engine')
        
        # Configure Gemini with safety settings
        genai.configure(api_key=Config.GEMINI_API_KEY)
        
        # Set safety settings to allow financial analysis
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
        
        self.model = genai.GenerativeModel(
            Config.GEMINI_MODEL,
            safety_settings=safety_settings
        )
        
        self.logger.info("RecommendationEngine initialized with Gemini API")
    
    def generate_recommendation(
        self,
        ticker: str,
        current_price: float,
        technical_data: Dict[str, Any],
        sentiment_data: Dict[str, Any],
        risk_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Generate trading recommendation by synthesizing all data via Gemini
        
        Args:
            ticker: Stock ticker symbol
            current_price: Current stock price
            technical_data: Technical analysis results
            sentiment_data: Sentiment analysis results
            risk_data: Risk management calculations
            
        Returns:
            Dictionary with recommendation or None if failed
        """
        try:
            # Create comprehensive synthesis prompt
            prompt = self._create_recommendation_prompt(
                ticker,
                current_price,
                technical_data,
                sentiment_data,
                risk_data
            )
            
            self.logger.info(f"Generating recommendation for {ticker} via Gemini")
            
            # Get recommendation from Gemini
            response = self.model.generate_content(prompt)
            
            # Parse response
            recommendation = self._parse_recommendation_response(response.text)
            
            if recommendation:
                # Add metadata
                recommendation['ticker'] = ticker
                recommendation['current_price'] = current_price
                recommendation['timestamp'] = datetime.now().isoformat()
                
                # Add risk management data
                recommendation['risk_management'] = {
                    'stop_loss': risk_data.get('stop_loss'),
                    'take_profit_1': risk_data.get('take_profit_1'),
                    'take_profit_2': risk_data.get('take_profit_2'),
                    'stop_loss_percent': risk_data.get('stop_loss_percent'),
                    'take_profit_1_percent': risk_data.get('take_profit_1_percent'),
                    'take_profit_2_percent': risk_data.get('take_profit_2_percent'),
                    'risk_reward_ratio_1': risk_data.get('risk_reward_ratio_1'),
                    'risk_reward_ratio_2': risk_data.get('risk_reward_ratio_2')
                }
                
                # Add technical indicators summary
                recommendation['technical_data'] = self._extract_technical_summary(technical_data)
                
                # Add sentiment score
                recommendation['sentiment_score'] = sentiment_data.get('sentiment_score', 0.0)
                recommendation['sentiment'] = sentiment_data.get('overall_sentiment', 'neutral')
                
                self.logger.info(
                    f"Generated {recommendation['recommendation']} recommendation for {ticker} "
                    f"with {recommendation['confidence_score']}% confidence"
                )
                
                PortfolioLogger.log_recommendation(ticker, recommendation)
                PortfolioLogger.log_api_call('gemini', 'recommendation_generation', True)
                
                return recommendation
            else:
                self.logger.warning(f"Failed to parse recommendation for {ticker}")
                return None
                
        except Exception as e:
            PortfolioLogger.log_error('RecommendationEngine.generate_recommendation', e, {'ticker': ticker})
            return None
    
    def _create_recommendation_prompt(
        self,
        ticker: str,
        current_price: float,
        technical_data: Dict[str, Any],
        sentiment_data: Dict[str, Any],
        risk_data: Dict[str, Any]
    ) -> str:
        """Create comprehensive prompt for Gemini recommendation"""
        
        prompt = f"""You are an expert financial analyst and portfolio manager. Analyze the following comprehensive data for {ticker} and provide a clear trading recommendation.

**DISCLAIMER**: This is an AI-generated recommendation and does not constitute professional financial advice.

**Current Market Data:**
- Ticker: {ticker}
- Current Price: ${current_price:.2f}
- Timestamp: {datetime.now().isoformat()}

**Technical Analysis:**
{json.dumps(technical_data, indent=2)}

**Sentiment Analysis:**
{json.dumps(sentiment_data, indent=2)}

**Risk Management:**
- Stop Loss: ${risk_data.get('stop_loss', 0):.2f} ({risk_data.get('stop_loss_percent', 0):.2f}%)
- Take Profit 1: ${risk_data.get('take_profit_1', 0):.2f} ({risk_data.get('take_profit_1_percent', 0):.2f}%)
- Take Profit 2: ${risk_data.get('take_profit_2', 0):.2f} ({risk_data.get('take_profit_2_percent', 0):.2f}%)
- Risk/Reward Ratio: {risk_data.get('risk_reward_ratio_1', 0):.2f}
- Volatility: {risk_data.get('volatility', 0):.2f}%

**Analysis Instructions:**

1. **Synthesize All Data**: Consider technical indicators, news sentiment, and risk metrics together
2. **Generate Clear Signal**: Determine if this is a BUY, SELL, or HOLD opportunity
3. **Assess Confidence**: Provide a confidence score (0-100%) based on:
   - Alignment of technical indicators
   - Strength of sentiment
   - Quality of risk/reward ratio
   - Overall market conditions
4. **Provide Reasoning**: Explain your decision clearly and concisely

**Decision Criteria:**
- BUY: Strong bullish signals from technical AND sentiment, good risk/reward (>1.5)
- SELL: Strong bearish signals, negative sentiment, or poor risk/reward
- HOLD: Mixed signals, neutral sentiment, or unclear trend

**Output Format (JSON only):**
```json
{{
  "recommendation": "BUY|SELL|HOLD",
  "confidence_score": <0-100>,
  "reasoning": "<detailed explanation combining technical, sentiment, and risk factors>",
  "key_factors": [
    "<factor 1: e.g., 'Bullish MACD crossover'>",
    "<factor 2: e.g., 'Positive earnings news sentiment'>",
    "<factor 3: e.g., 'Favorable risk/reward ratio of 2.5'>"
  ],
  "timeframe": "short_term|medium_term|long_term",
  "risk_level": "low|medium|high",
  "entry_strategy": "<when/how to enter this position>",
  "exit_strategy": "<when/how to exit this position>",
  "warnings": ["<any risks or concerns to note>"],
  "conviction_level": "high|medium|low"
}}
```

**Critical Requirements:**
- Your confidence score must be data-driven and realistic
- If signals are mixed or unclear, recommend HOLD
- Always prioritize risk management
- Be specific in your reasoning
- Target minimum 70% confidence for BUY/SELL recommendations

Provide ONLY the JSON response, no additional commentary."""

        return prompt
    
    def _parse_recommendation_response(self, response_text: str) -> Optional[Dict[str, Any]]:
        """Parse Gemini's recommendation response"""
        try:
            # Clean response
            response_text = response_text.strip()
            
            # Remove markdown
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            
            # Parse JSON
            data = json.loads(response_text)
            
            # Validate required fields
            required = ['recommendation', 'confidence_score', 'reasoning']
            if not all(field in data for field in required):
                self.logger.error("Missing required fields in recommendation")
                return None
            
            # Validate recommendation value
            valid_recommendations = ['BUY', 'SELL', 'HOLD']
            if data['recommendation'].upper() not in valid_recommendations:
                self.logger.error(f"Invalid recommendation: {data['recommendation']}")
                return None
            
            data['recommendation'] = data['recommendation'].upper()
            
            # Ensure confidence is in valid range
            data['confidence_score'] = max(0, min(100, data['confidence_score']))
            
            return data
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse recommendation as JSON: {e}")
            self.logger.debug(f"Response: {response_text[:500]}")
            return None
        except Exception as e:
            self.logger.error(f"Error parsing recommendation: {e}")
            return None
    
    def _extract_technical_summary(self, technical_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract key technical indicators for output"""
        try:
            summary = {}
            
            if 'rsi' in technical_data:
                summary['rsi'] = technical_data['rsi'].get('value')
                summary['rsi_signal'] = technical_data['rsi'].get('signal')
            
            if 'macd' in technical_data:
                summary['macd'] = technical_data['macd'].get('macd_line')
                summary['macd_signal'] = technical_data['macd'].get('signal_line')
                summary['macd_crossover'] = technical_data['macd'].get('crossover')
            
            if 'trend' in technical_data:
                summary['trend'] = technical_data['trend'].get('direction')
                summary['trend_strength'] = technical_data['trend'].get('strength')
            
            if 'overall_signal' in technical_data:
                summary['overall_technical_signal'] = technical_data['overall_signal']
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Error extracting technical summary: {e}")
            return {}
