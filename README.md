# 🤖 AI Financial Portfolio Manager Agent

An advanced AI-powered financial portfolio management system that provides real-time, data-driven trading recommendations using Google's Gemini API. This autonomous agent continuously monitors markets, performs technical and sentiment analysis, and generates actionable BUY/SELL/HOLD recommendations with an 80%+ accuracy target.

## ⚠️ IMPORTANT DISCLAIMER

**This is an AI-generated recommendation tool and does NOT constitute professional financial advice. The recommendations provided are for informational purposes only. Always conduct your own research and consult with a qualified financial advisor before making any investment decisions. Trading stocks and forex involves substantial risk of loss.**

## 🌟 Key Features

### Real-Time Market Analysis
- **Live Price Tracking**: Continuous monitoring of stock prices, volume, and market metrics
- **Multi-Market Support**: Handles stocks (NYSE, NASDAQ) and Forex markets
- **Intelligent Caching**: Optimized data fetching with smart caching mechanisms

### Advanced Technical Analysis (via Gemini API)
- **RSI (Relative Strength Index)**: Identifies overbought/oversold conditions
- **MACD (Moving Average Convergence Divergence)**: Tracks momentum and trend direction
- **Bollinger Bands**: Gauges market volatility and price action zones
- **Moving Averages**: SMA and EMA calculations for 50, 100, and 200-day periods
- **Support/Resistance Levels**: Automatic identification of key price levels
- **Trend Analysis**: Comprehensive trend direction and strength assessment

### Real-Time News & Sentiment Analysis
- **Google Search Grounding**: Gemini API with real-time Google Search integration
- **Multi-Source News**: Aggregates from Bloomberg, Reuters, CNBC, WSJ, and more
- **Sentiment Scoring**: Quantified sentiment from -1.0 (very negative) to +1.0 (very positive)
- **Impact Assessment**: Evaluates potential market impact of news events
- **Event Tracking**: Identifies upcoming events (earnings, product launches, etc.)

### Intelligent Recommendation Engine
- **Clear Signals**: BUY, SELL, or HOLD recommendations
- **Confidence Scores**: 0-100% confidence rating for each recommendation
- **Data Synthesis**: Combines technical indicators, sentiment, and risk metrics
- **Detailed Reasoning**: Comprehensive explanations for each decision
- **Risk Management**: Stop-loss and take-profit levels with every recommendation

### Risk Management
- **Volatility-Based Calculations**: Uses ATR (Average True Range) for dynamic risk levels
- **Support/Resistance Integration**: Incorporates technical levels into risk calculations
- **Dual Take-Profit Targets**: Conservative (TP1) and aggressive (TP2) exit points
- **Risk-Reward Ratios**: Ensures favorable risk-reward profiles (minimum 1.5:1)

### Comprehensive Logging & Output
- **JSON Logging**: Structured logs for all operations and decisions
- **Historical Tracking**: Maintains history of all recommendations
- **Console Display**: Beautiful, readable terminal output
- **File Storage**: Saves all recommendations for later review

## 📋 Requirements

- Python 3.8 or higher
- Gemini API Key (from Google AI Studio)
- Internet connection for real-time data

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd financial_portfolio
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional (for additional data sources)
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here

# Agent Configuration (optional - defaults provided)
UPDATE_INTERVAL_SECONDS=60
CONFIDENCE_THRESHOLD=70
MAX_CONCURRENT_STOCKS=10
```

#### Getting API Keys

**Gemini API Key** (Required):
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key to your `.env` file

**Alpha Vantage API Key** (Optional):
1. Visit [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
2. Enter your email to get a free API key
3. Copy to `.env` file (optional - used as backup data source)

### 5. Configure Your Portfolio

Edit `portfolio.json` to add your stocks:

```json
{
  "portfolio": [
    {
      "ticker": "AAPL",
      "name": "Apple Inc.",
      "market": "NASDAQ"
    },
    {
      "ticker": "GOOGL",
      "name": "Alphabet Inc.",
      "market": "NASDAQ"
    }
  ],
  "watchlist": [
    {
      "ticker": "NVDA",
      "name": "NVIDIA Corporation",
      "market": "NASDAQ"
    }
  ],
  "forex": [
    {
      "ticker": "EURUSD=X",
      "name": "EUR/USD",
      "market": "FOREX"
    }
  ]
}
```

## 💻 Usage

### Continuous Monitoring (Recommended)

Run the agent in continuous mode to monitor your portfolio 24/7:

```bash
python main.py
```

This will:
- Analyze all tickers in your portfolio
- Generate recommendations every 60 seconds (configurable)
- Save all recommendations to `output/` directory
- Display real-time updates in the console

### Single Analysis Cycle

Run one complete analysis cycle and exit:

```bash
python main.py --single
```

### Analyze Specific Stock

Analyze a single stock symbol:

```bash
python main.py --ticker AAPL
```

### Custom Portfolio File

Use a different portfolio configuration:

```bash
python main.py --portfolio my_custom_portfolio.json
```

### All Command-Line Options

```bash
python main.py --help
```

## 📊 Output Format

### Console Output

The agent displays recommendations in a beautiful, readable format:

```
================================================================================
TRADING RECOMMENDATION - AAPL
================================================================================

📊 Current Price: $170.50
⏰ Timestamp: 2023-10-27T14:35:00Z

🟢 RECOMMENDATION: BUY
💪 Confidence Score: 85%

📝 Reasoning:
Strong bullish momentum indicated by MACD crossover above the signal line...

🔑 Key Factors:
   1. Bullish MACD crossover
   2. Positive earnings news sentiment
   3. Favorable risk/reward ratio of 2.5

⚠️  Risk Management:
   Stop Loss: $165.75 (-2.79%)
   Take Profit 1: $175.00 (+2.64%)
   Take Profit 2: $180.25 (+5.72%)
   Risk/Reward: 2.50

📈 Technical Indicators:
   RSI: 60.1 (neutral)
   MACD: bullish
   Trend: uptrend (strong)

💭 Sentiment: POSITIVE (0.80)

⏱️  Timeframe: medium_term
🎯 Risk Level: MEDIUM
================================================================================
```

### JSON Output

All recommendations are saved as JSON files in `output/recommendations/`:

```json
{
  "ticker": "AAPL",
  "timestamp": "2023-10-27T14:35:00Z",
  "current_price": 170.50,
  "recommendation": "BUY",
  "confidence_score": 85,
  "reasoning": "Strong bullish momentum...",
  "risk_management": {
    "stop_loss": 165.75,
    "take_profit_1": 175.00,
    "take_profit_2": 180.25,
    "risk_reward_ratio_1": 2.5
  },
  "technical_data": {
    "rsi": 60.1,
    "macd": 1.25,
    "trend": "uptrend"
  },
  "sentiment_score": 0.80
}
```

## 🏗️ Architecture

### Project Structure

```
financial_portfolio/
├── main.py                      # Main entry point
├── portfolio.json               # Your portfolio configuration
├── requirements.txt             # Python dependencies
├── .env                        # Environment variables (create from .env.example)
├── .env.example                # Environment template
├── README.md                   # This file
│
├── src/                        # Source code
│   ├── __init__.py
│   ├── config.py               # Configuration management
│   ├── data_fetcher.py         # Market data fetching
│   ├── technical_analyzer.py   # Technical analysis (Gemini)
│   ├── sentiment_analyzer.py   # Sentiment analysis (Gemini + Google Search)
│   ├── recommendation_engine.py # Recommendation generation (Gemini)
│   ├── risk_manager.py         # Risk management calculations
│   ├── output_handler.py       # Output formatting and storage
│   │
│   └── utils/                  # Utilities
│       ├── __init__.py
│       └── logger.py           # Logging system
│
├── output/                     # Generated outputs (created automatically)
│   ├── recommendations/        # Individual recommendation files
│   └── history/               # Historical logs
│
└── logs/                      # Application logs (created automatically)
    └── portfolio_agent.log    # Main log file
```

### Agent Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    MAIN ORCHESTRATOR                         │
│                   (PortfolioManagerAgent)                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────┐
        │  For Each Stock in Portfolio:       │
        └─────────────────────────────────────┘
                              │
        ┌─────────────────────┴─────────────────────┐
        │                                           │
        ▼                                           ▼
┌──────────────────┐                    ┌──────────────────────┐
│  STEP 1: Fetch   │                    │  STEP 2: Technical   │
│  Market Data     │ ──────────────────▶│  Analysis (Gemini)   │
│  (yfinance)      │                    │  - RSI, MACD, BB     │
└──────────────────┘                    │  - Moving Averages   │
                                        │  - Support/Resistance│
                                        └──────────────────────┘
                                                    │
                                                    ▼
                                        ┌──────────────────────┐
                                        │  STEP 3: Sentiment   │
                                        │  Analysis (Gemini)   │
                                        │  - Google Search     │
                                        │  - News Aggregation  │
                                        └──────────────────────┘
                                                    │
                                                    ▼
                                        ┌──────────────────────┐
                                        │  STEP 4: Risk        │
                                        │  Management          │
                                        │  - Stop Loss         │
                                        │  - Take Profits      │
                                        └──────────────────────┘
                                                    │
                                                    ▼
                                        ┌──────────────────────┐
                                        │  STEP 5: Generate    │
                                        │  Recommendation      │
                                        │  (Gemini Synthesis)  │
                                        └──────────────────────┘
                                                    │
                                                    ▼
                                        ┌──────────────────────┐
                                        │  Output & Storage    │
                                        │  - JSON Files        │
                                        │  - Console Display   │
                                        │  - Logging           │
                                        └──────────────────────┘
```

## ⚙️ Configuration

### Agent Settings (.env)

| Variable | Default | Description |
|----------|---------|-------------|
| `UPDATE_INTERVAL_SECONDS` | 60 | Seconds between analysis cycles |
| `CONFIDENCE_THRESHOLD` | 70 | Minimum confidence for recommendations |
| `MAX_CONCURRENT_STOCKS` | 10 | Maximum stocks to analyze concurrently |
| `DEFAULT_STOP_LOSS_PERCENTAGE` | 5.0 | Default stop loss % |
| `DEFAULT_TAKE_PROFIT_1_PERCENTAGE` | 10.0 | Default first take profit % |
| `DEFAULT_TAKE_PROFIT_2_PERCENTAGE` | 20.0 | Default second take profit % |
| `LOG_LEVEL` | INFO | Logging level (DEBUG, INFO, WARNING, ERROR) |

### Technical Indicators (config.py)

```python
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70.0
RSI_OVERSOLD = 30.0

MACD_FAST_PERIOD = 12
MACD_SLOW_PERIOD = 26
MACD_SIGNAL_PERIOD = 9

BOLLINGER_PERIOD = 20
BOLLINGER_STD_DEV = 2.0

MA_PERIODS = [50, 100, 200]
```

## 📈 Understanding Recommendations

### Recommendation Types

- **BUY**: Strong bullish signals from technical AND sentiment analysis with favorable risk/reward (>1.5)
- **SELL**: Strong bearish signals, negative sentiment, or poor risk/reward ratio
- **HOLD**: Mixed signals, neutral sentiment, or unclear trend direction

### Confidence Score Interpretation

- **80-100%**: Very High Confidence - Strong alignment across all indicators
- **70-79%**: High Confidence - Good alignment with minor discrepancies
- **60-69%**: Medium Confidence - Moderate signals, some conflicting data
- **50-59%**: Low Confidence - Weak or highly mixed signals
- **<50%**: Very Low Confidence - Should typically result in HOLD

### Risk Management Guidelines

1. **Always use stop-loss orders** to limit downside risk
2. **Take partial profits at TP1** to secure gains
3. **Let winners run to TP2** for maximum potential
4. **Never risk more than 2-3%** of your portfolio on a single trade
5. **Respect the risk-reward ratio** - look for minimum 1.5:1

## 🔧 Troubleshooting

### Common Issues

**1. API Key Errors**
```
Error: GEMINI_API_KEY is required but not set
```
Solution: Ensure your `.env` file contains a valid Gemini API key

**2. No Data Retrieved**
```
Warning: No recent data available for TICKER
```
Solution: Check ticker symbol is correct, try during market hours, verify internet connection

**3. Import Errors**
```
ModuleNotFoundError: No module named 'google.generativeai'
```
Solution: Run `pip install -r requirements.txt` in your virtual environment

**4. Rate Limiting**
```
Error: API rate limit exceeded
```
Solution: Increase `UPDATE_INTERVAL_SECONDS` in `.env`, reduce number of tickers

### Debug Mode

Enable debug logging:

```env
LOG_LEVEL=DEBUG
```

Check logs:
```bash
tail -f logs/portfolio_agent.log
```

## 🤝 Contributing

This project was created as a comprehensive AI trading agent. Contributions are welcome!

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit with clear messages (`git commit -m 'feat: Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📝 License

This project is provided as-is for educational and informational purposes.

## 🙏 Acknowledgments

- **Google Gemini API** for powerful AI analysis capabilities
- **yfinance** for reliable market data
- **The open-source community** for excellent Python libraries

## 📧 Support

For issues, questions, or suggestions:
1. Check existing documentation
2. Review troubleshooting section
3. Open an issue on GitHub

## 🔮 Future Enhancements

- [ ] Backtesting framework
- [ ] Performance tracking and analytics
- [ ] Multi-timeframe analysis
- [ ] Portfolio optimization suggestions
- [ ] Integration with trading platforms
- [ ] Machine learning model for pattern recognition
- [ ] Web dashboard interface
- [ ] Mobile notifications
- [ ] Paper trading mode
- [ ] Advanced order types (trailing stops, etc.)

---

**Remember**: Always trade responsibly and never invest more than you can afford to lose. This tool is an aid to decision-making, not a replacement for human judgment and professional financial advice.