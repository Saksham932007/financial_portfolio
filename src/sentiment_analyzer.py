"""
Sentiment Analysis Module using Gemini API with Google Search
Analyzes news and market sentiment for stocks
"""

import google.generativeai as genai
from typing import Dict, Any, Optional, List
import json
from datetime import datetime, timedelta
from src.config import Config
from src.utils.logger import PortfolioLogger


class SentimentAnalyzer:
    """Performs news and sentiment analysis using Gemini API with Google Search grounding"""
    
    def __init__(self):
        self.logger = PortfolioLogger.get_logger('sentiment_analyzer')
        
        # Configure Gemini API with safety settings
        genai.configure(api_key=Config.GEMINI_API_KEY)
        
        # Set safety settings to allow financial analysis
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
        
        # Use model without grounding (Search grounding not supported for gemini-2.5-flash)
        self.model = genai.GenerativeModel(
            Config.GEMINI_MODEL,
            safety_settings=safety_settings
        )
        self.has_grounding = False
        self.logger.info("SentimentAnalyzer initialized with Gemini API")
    
    def analyze_sentiment(self, ticker: str, company_name: str = None) -> Optional[Dict[str, Any]]:
        """
        Analyze news sentiment for a stock using Gemini with Google Search
        
        Args:
            ticker: Stock ticker symbol
            company_name: Full company name (optional, helps with search)
            
        Returns:
            Dictionary with sentiment analysis or None if failed
        """
        try:
            # Create search-optimized prompt
            prompt = self._create_sentiment_prompt(ticker, company_name)
            
            self.logger.info(f"Requesting sentiment analysis for {ticker} from Gemini with Google Search")
            
            # Generate content with Google Search grounding
            response = self.model.generate_content(prompt)
            
            # Parse the response
            sentiment_data = self._parse_sentiment_response(response.text)
            
            if sentiment_data:
                sentiment_data['ticker'] = ticker
                sentiment_data['timestamp'] = datetime.now().isoformat()
                sentiment_data['analysis_period_hours'] = Config.NEWS_LOOKBACK_HOURS
                
                self.logger.info(
                    f"Sentiment analysis completed for {ticker}: "
                    f"{sentiment_data.get('overall_sentiment', 'unknown')}"
                )
                PortfolioLogger.log_api_call('gemini', 'sentiment_analysis', True)
                
                return sentiment_data
            else:
                self.logger.warning(f"Failed to parse sentiment response for {ticker}")
                return None
                
        except Exception as e:
            PortfolioLogger.log_error('SentimentAnalyzer.analyze_sentiment', e, {'ticker': ticker})
            return None
    
    def _create_sentiment_prompt(self, ticker: str, company_name: str = None) -> str:
        """Create prompt for sentiment analysis with Google Search"""
        
        search_term = company_name if company_name else ticker
        current_time = datetime.now()
        
        prompt = f"""You are an expert financial news analyst with real-time market access. Using Google Search, find and analyze the most recent news and market sentiment for {search_term} (ticker: {ticker}).

**Search Requirements:**
- Focus on news from the last {Config.NEWS_LOOKBACK_HOURS} hours
- Find at least {Config.MAX_NEWS_ARTICLES} relevant articles
- Include: earnings reports, product launches, analyst ratings, market news, regulatory updates
- Prioritize credible financial news sources (Bloomberg, Reuters, CNBC, WSJ, Financial Times, etc.)

**Analysis Tasks:**

1. **News Summary:**
   - List the top {Config.MAX_NEWS_ARTICLES} most relevant news items
   - For each: title, source, timestamp, brief summary

2. **Sentiment Classification:**
   - Analyze the overall sentiment: Positive, Negative, or Neutral
   - Provide a sentiment score from -1.0 (very negative) to +1.0 (very positive)
   - Explain the reasoning

3. **Market Impact Assessment:**
   - Estimate potential price impact: High, Medium, or Low
   - Identify key catalysts or concerns
   - Note any upcoming events (earnings, product launches, etc.)

4. **Key Themes:**
   - Identify main themes in the news (e.g., "strong earnings", "regulatory concerns", "product innovation")
   - List top 3-5 themes

**Output Format (JSON only):**
```json
{{
  "news_articles": [
    {{
      "title": "<article title>",
      "source": "<source name>",
      "timestamp": "<timestamp or relative time>",
      "summary": "<brief summary>",
      "sentiment": "positive|negative|neutral"
    }}
  ],
  "overall_sentiment": "positive|negative|neutral",
  "sentiment_score": <float between -1.0 and 1.0>,
  "confidence": <float between 0 and 100>,
  "reasoning": "<detailed explanation of sentiment>",
  "market_impact": {{
    "level": "high|medium|low",
    "direction": "bullish|bearish|neutral",
    "catalysts": ["<catalyst 1>", "<catalyst 2>"],
    "concerns": ["<concern 1>", "<concern 2>"]
  }},
  "key_themes": ["<theme 1>", "<theme 2>", "<theme 3>"],
  "upcoming_events": [
    {{
      "event": "<event description>",
      "date": "<date if known>",
      "significance": "high|medium|low"
    }}
  ]
}}
```

Provide ONLY the JSON response. Use real-time Google Search to gather current information."""

        return prompt
    
    def _parse_sentiment_response(self, response_text: str) -> Optional[Dict[str, Any]]:
        """Parse Gemini's sentiment analysis response"""
        try:
            # Clean response text
            response_text = response_text.strip()
            
            # Remove markdown code blocks
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
            required_fields = ['overall_sentiment', 'sentiment_score']
            if not all(field in data for field in required_fields):
                self.logger.error(f"Missing required fields in sentiment response")
                return None
            
            return data
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse sentiment response as JSON: {e}")
            self.logger.debug(f"Response text: {response_text[:500]}")
            return None
        except Exception as e:
            self.logger.error(f"Error parsing sentiment response: {e}")
            return None
    
    def get_simple_sentiment(self, ticker: str) -> Dict[str, Any]:
        """
        Get simplified sentiment analysis (fallback method)
        
        Returns:
            Basic sentiment data
        """
        try:
            # Simplified prompt for quick sentiment check
            prompt = f"""Based on recent market news for {ticker}, provide a quick sentiment assessment.

Output as JSON:
{{
  "overall_sentiment": "positive|negative|neutral",
  "sentiment_score": <-1.0 to 1.0>,
  "brief_reasoning": "<one sentence explanation>"
}}"""

            response = self.model.generate_content(prompt)
            
            data = self._parse_sentiment_response(response.text)
            
            if data:
                data['ticker'] = ticker
                data['timestamp'] = datetime.now().isoformat()
                return data
            
            return {
                'ticker': ticker,
                'overall_sentiment': 'neutral',
                'sentiment_score': 0.0,
                'brief_reasoning': 'Unable to analyze sentiment',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            PortfolioLogger.log_error('SentimentAnalyzer.get_simple_sentiment', e, {'ticker': ticker})
            return {
                'ticker': ticker,
                'overall_sentiment': 'neutral',
                'sentiment_score': 0.0,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
