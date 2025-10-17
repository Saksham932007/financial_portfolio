# API Documentation

## Overview

The AI Financial Portfolio Manager exposes its functionality through well-defined Python modules. While there's no REST API (yet), you can integrate the components into your own applications.

## Core Modules

### 1. MarketDataFetcher

**Location**: `src/data_fetcher.py`

Fetches real-time and historical market data.

#### Methods

```python
from src.data_fetcher import MarketDataFetcher

fetcher = MarketDataFetcher()

# Get live price data
price_data = fetcher.get_live_price('AAPL')
# Returns: {
#   'ticker': 'AAPL',
#   'current_price': 170.50,
#   'volume': 52000000,
#   'day_high': 172.00,
#   'day_low': 169.50,
#   ...
# }

# Get historical data
historical = fetcher.get_historical_data('AAPL', period='1y', interval='1d')
# Returns: pandas DataFrame with OHLCV data

# Get multiple tickers
data = fetcher.get_multiple_tickers(['AAPL', 'MSFT', 'GOOGL'])
# Returns: dict mapping ticker to price data
```

### 2. TechnicalAnalyzer

**Location**: `src/technical_analyzer.py`

Performs technical analysis using Gemini API.

#### Methods

```python
from src.technical_analyzer import TechnicalAnalyzer

analyzer = TechnicalAnalyzer()

# Analyze stock
technical_data = analyzer.analyze('AAPL', price_dataframe)
# Returns: {
#   'rsi': {'value': 60.1, 'signal': 'neutral'},
#   'macd': {'macd_line': 1.25, 'crossover': 'bullish'},
#   'bollinger_bands': {'upper': 175.0, 'middle': 170.0, 'lower': 165.0},
#   'trend': {'direction': 'uptrend', 'strength': 'strong'},
#   ...
# }

# Quick indicators (fallback)
quick = analyzer.get_quick_indicators('AAPL', price_dataframe)
```

### 3. SentimentAnalyzer

**Location**: `src/sentiment_analyzer.py`

Analyzes news sentiment using Gemini API with Google Search.

#### Methods

```python
from src.sentiment_analyzer import SentimentAnalyzer

analyzer = SentimentAnalyzer()

# Analyze sentiment
sentiment = analyzer.analyze_sentiment('AAPL', 'Apple Inc.')
# Returns: {
#   'overall_sentiment': 'positive',
#   'sentiment_score': 0.75,
#   'news_articles': [...],
#   'market_impact': {'level': 'high', 'direction': 'bullish'},
#   ...
# }

# Simple sentiment
simple = analyzer.get_simple_sentiment('AAPL')
```

### 4. RiskManager

**Location**: `src/risk_manager.py`

Calculates risk management levels.

#### Methods

```python
from src.risk_manager import RiskManager

risk_mgr = RiskManager()

# Calculate risk levels
risk_data = risk_mgr.calculate_risk_levels(
    ticker='AAPL',
    current_price=170.50,
    price_data=historical_df,
    technical_data=technical_dict
)
# Returns: {
#   'stop_loss': 165.75,
#   'take_profit_1': 175.00,
#   'take_profit_2': 180.25,
#   'risk_reward_ratio_1': 2.5,
#   ...
# }

# Validate risk-reward
is_valid = risk_mgr.validate_risk_reward(risk_data, min_ratio=1.5)
```

### 5. RecommendationEngine

**Location**: `src/recommendation_engine.py`

Generates trading recommendations using Gemini.

#### Methods

```python
from src.recommendation_engine import RecommendationEngine

engine = RecommendationEngine()

# Generate recommendation
rec = engine.generate_recommendation(
    ticker='AAPL',
    current_price=170.50,
    technical_data=technical_dict,
    sentiment_data=sentiment_dict,
    risk_data=risk_dict
)
# Returns: {
#   'recommendation': 'BUY',
#   'confidence_score': 85,
#   'reasoning': '...',
#   'risk_management': {...},
#   ...
# }
```

### 6. OutputHandler

**Location**: `src/output_handler.py`

Handles output formatting and storage.

#### Methods

```python
from src.output_handler import OutputHandler

output = OutputHandler(output_dir='output')

# Save recommendation
output.save_recommendation(recommendation_dict)

# Print to console
output.print_recommendation(recommendation_dict)

# Get latest
latest = output.get_latest_recommendation('AAPL')

# Get history
history = output.get_recommendation_history('AAPL', days=7)

# Create summary
summary = output.create_summary_report([rec1, rec2, rec3])
```

## Integration Example

### Basic Integration

```python
from src.data_fetcher import MarketDataFetcher
from src.technical_analyzer import TechnicalAnalyzer
from src.sentiment_analyzer import SentimentAnalyzer
from src.recommendation_engine import RecommendationEngine
from src.risk_manager import RiskManager

# Initialize modules
data_fetcher = MarketDataFetcher()
tech_analyzer = TechnicalAnalyzer()
sent_analyzer = SentimentAnalyzer()
risk_manager = RiskManager()
rec_engine = RecommendationEngine()

# Analyze a stock
ticker = 'AAPL'

# 1. Fetch data
price_data = data_fetcher.get_live_price(ticker)
historical = data_fetcher.get_historical_data(ticker)

# 2. Technical analysis
technical = tech_analyzer.analyze(ticker, historical)

# 3. Sentiment analysis
sentiment = sent_analyzer.analyze_sentiment(ticker, 'Apple Inc.')

# 4. Risk management
risk = risk_manager.calculate_risk_levels(
    ticker,
    price_data['current_price'],
    historical,
    technical
)

# 5. Generate recommendation
recommendation = rec_engine.generate_recommendation(
    ticker,
    price_data['current_price'],
    technical,
    sentiment,
    risk
)

print(recommendation)
```

### Custom Analysis

```python
# Use only specific modules
from src.data_fetcher import MarketDataFetcher
from src.technical_analyzer import TechnicalAnalyzer

fetcher = MarketDataFetcher()
analyzer = TechnicalAnalyzer()

# Quick technical check
historical = fetcher.get_historical_data('AAPL', period='6mo')
technical = analyzer.get_quick_indicators('AAPL', historical)

if technical['above_sma_50']:
    print("Price above 50-day MA - potential uptrend")
```

## Configuration

### Environment Variables

```python
from src.config import Config

# Access configuration
Config.GEMINI_API_KEY
Config.UPDATE_INTERVAL_SECONDS
Config.CONFIDENCE_THRESHOLD
Config.RSI_PERIOD
Config.MACD_FAST_PERIOD
# etc.

# Validate config
Config.validate()

# Get config dict
config_dict = Config.get_config_dict()
```

### Logger

```python
from src.utils.logger import PortfolioLogger

# Get logger
logger = PortfolioLogger.get_logger('my_module')

# Log messages
logger.info("Information message")
logger.warning("Warning message")
logger.error("Error message")

# Specialized logging
PortfolioLogger.log_market_data('AAPL', price_data)
PortfolioLogger.log_recommendation('AAPL', recommendation)
PortfolioLogger.log_api_call('gemini', 'analysis', True, 1.5)
PortfolioLogger.log_error('ComponentName', exception, context_dict)
```

## Data Structures

### Price Data Structure

```python
{
    'ticker': 'AAPL',
    'timestamp': '2023-10-27T14:35:00Z',
    'current_price': 170.50,
    'open': 169.00,
    'high': 171.25,
    'low': 168.75,
    'volume': 52000000,
    'previous_close': 169.50,
    'day_high': 171.25,
    'day_low': 168.75,
    'change': 1.00,
    'change_percent': 0.59
}
```

### Technical Data Structure

```python
{
    'ticker': 'AAPL',
    'timestamp': '2023-10-27T14:35:00Z',
    'rsi': {
        'value': 60.1,
        'signal': 'neutral',
        'interpretation': '...'
    },
    'macd': {
        'macd_line': 1.25,
        'signal_line': 0.95,
        'histogram': 0.30,
        'crossover': 'bullish',
        'interpretation': '...'
    },
    'bollinger_bands': {
        'upper': 175.00,
        'middle': 170.00,
        'lower': 165.00,
        'price_position': 'within_bands',
        'interpretation': '...'
    },
    'moving_averages': {
        'sma_50': 168.00,
        'sma_100': 165.00,
        'sma_200': 160.00,
        'ema_50': 168.50,
        'ema_100': 165.50,
        'ema_200': 160.50,
        'golden_cross': False,
        'death_cross': False
    },
    'support_resistance': {
        'support_levels': [165.00, 162.50],
        'resistance_levels': [172.00, 175.00]
    },
    'trend': {
        'direction': 'uptrend',
        'strength': 'strong',
        'interpretation': '...'
    },
    'overall_signal': 'bullish'
}
```

### Sentiment Data Structure

```python
{
    'ticker': 'AAPL',
    'timestamp': '2023-10-27T14:35:00Z',
    'overall_sentiment': 'positive',
    'sentiment_score': 0.75,
    'confidence': 85,
    'reasoning': '...',
    'news_articles': [
        {
            'title': '...',
            'source': 'Bloomberg',
            'timestamp': '...',
            'summary': '...',
            'sentiment': 'positive'
        }
    ],
    'market_impact': {
        'level': 'high',
        'direction': 'bullish',
        'catalysts': ['...'],
        'concerns': ['...']
    },
    'key_themes': ['...'],
    'upcoming_events': [...]
}
```

### Recommendation Structure

```python
{
    'ticker': 'AAPL',
    'timestamp': '2023-10-27T14:35:00Z',
    'current_price': 170.50,
    'recommendation': 'BUY',
    'confidence_score': 85,
    'reasoning': '...',
    'key_factors': ['...', '...', '...'],
    'timeframe': 'medium_term',
    'risk_level': 'medium',
    'entry_strategy': '...',
    'exit_strategy': '...',
    'warnings': ['...'],
    'conviction_level': 'high',
    'risk_management': {
        'stop_loss': 165.75,
        'take_profit_1': 175.00,
        'take_profit_2': 180.25,
        'stop_loss_percent': -2.79,
        'take_profit_1_percent': 2.64,
        'take_profit_2_percent': 5.72,
        'risk_reward_ratio_1': 2.5,
        'risk_reward_ratio_2': 5.0
    },
    'technical_data': {...},
    'sentiment_score': 0.75,
    'sentiment': 'positive'
}
```

## Error Handling

All modules use try-except blocks and return `None` on errors. Check return values:

```python
data = fetcher.get_live_price('INVALID')
if data is None:
    print("Failed to fetch data")
else:
    print(f"Price: {data['current_price']}")
```

## Rate Limiting

- Built-in caching (60 seconds default)
- Configurable update intervals
- Sleep between multiple requests
- Graceful handling of API limits

## Future API Endpoints

Planned for future releases:

- REST API server
- WebSocket streaming
- GraphQL interface
- Webhook notifications

---

For more details, see the source code and inline documentation.
