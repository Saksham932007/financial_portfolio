# Frequently Asked Questions (FAQ)

## General Questions

### What is this project?
The AI Financial Portfolio Manager is an autonomous trading recommendation system that uses Google's Gemini API to analyze stocks, forex, and other financial instruments in real-time, providing BUY/SELL/HOLD recommendations with confidence scores.

### Is this free to use?
Yes, the software is free and open-source (MIT License). However, you'll need a free Gemini API key from Google. Gemini offers a generous free tier that should be sufficient for most users.

### Can I use this for live trading?
The software generates recommendations only. It does NOT execute trades automatically. You must manually place trades through your broker. We recommend using these as one input among many in your trading decisions.

### Is this financial advice?
**NO.** This is an AI-generated analysis tool for informational purposes only. It does NOT constitute professional financial advice. Always consult with qualified financial advisors.

## Setup & Installation

### What do I need to get started?
- Python 3.8 or higher
- Internet connection
- Gemini API key (free from Google AI Studio)
- About 5 minutes for setup

### Where do I get a Gemini API key?
1. Visit https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key to your `.env` file

### The setup script fails on my system
Try manual installation:
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your API key
```

### I'm getting import errors
Make sure:
1. Virtual environment is activated
2. Dependencies are installed: `pip install -r requirements.txt`
3. You're in the project root directory

## Usage Questions

### How often should I run the agent?
- **Continuous mode** (default): Runs every 60 seconds
- **Single analysis**: Once on demand
- **Custom interval**: Adjust `UPDATE_INTERVAL_SECONDS` in `.env`

Recommendation: Start with single analysis mode to test, then use continuous mode.

### How many stocks can I monitor?
The default limit is 10 concurrent stocks (`MAX_CONCURRENT_STOCKS`). You can increase this, but be aware of:
- API rate limits
- Processing time
- Data costs

### Can I analyze stocks outside the US?
Yes! yfinance supports international markets. Use the appropriate ticker symbol:
- US stocks: `AAPL`
- London: `BP.L`
- Tokyo: `7203.T`
- etc.

### What markets are supported?
- **Stocks**: NYSE, NASDAQ, and international exchanges
- **Forex**: Major and minor currency pairs
- **Crypto**: Bitcoin, Ethereum, and other major cryptocurrencies
- **ETFs**: All major ETFs
- **Indices**: S&P 500, NASDAQ, Dow Jones, etc.

### The agent can't find data for my ticker
Check:
1. Ticker symbol is correct
2. Market is open (or use recent data)
3. Internet connection is working
4. Ticker exists on yfinance (test at https://finance.yahoo.com)

## Technical Questions

### How accurate are the recommendations?
The agent aims for 80%+ accuracy, but this depends on:
- Market conditions
- Data quality
- News availability
- Indicator alignment

**Important**: Always verify recommendations with your own research.

### What technical indicators are used?
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- Bollinger Bands
- Moving Averages (SMA/EMA for 50, 100, 200 days)
- Support/Resistance levels
- Trend analysis
- ATR (Average True Range)

### How does sentiment analysis work?
The agent uses Gemini API with Google Search grounding to:
1. Find recent news articles (last 24 hours)
2. Analyze sentiment from credible sources
3. Score sentiment from -1.0 (very negative) to +1.0 (very positive)
4. Assess market impact

### Can I customize the technical indicators?
Yes! Edit `src/config.py`:
```python
RSI_PERIOD = 14  # Change to your preference
MACD_FAST_PERIOD = 12
BOLLINGER_PERIOD = 20
# etc.
```

### How are stop-loss and take-profit levels calculated?
The risk manager uses:
- Historical volatility (standard deviation)
- ATR (Average True Range)
- Support/resistance levels from technical analysis
- Configurable percentages

Default: 5% stop-loss, 10% TP1, 20% TP2

## Performance & Optimization

### The agent is too slow
Try:
- Reduce number of tickers
- Increase `UPDATE_INTERVAL_SECONDS`
- Use faster internet connection
- Check API rate limits

### How do I reduce API calls?
- Increase update interval
- Use data caching (built-in, 60s default)
- Analyze fewer tickers
- Run in single analysis mode

### Can I run this on a server?
Yes! The agent runs well on:
- Cloud servers (AWS, GCP, Azure)
- VPS
- Raspberry Pi (for smaller portfolios)
- Docker containers (create your own Dockerfile)

### How much does it cost to run?
- **Software**: Free
- **Gemini API**: Free tier is generous, paid tiers available
- **Data**: yfinance is free
- **Infrastructure**: Depends on where you run it

## Troubleshooting

### "GEMINI_API_KEY is required"
Add your API key to `.env`:
```env
GEMINI_API_KEY=your_key_here
```

### "No recent data available for TICKER"
- Check ticker symbol
- Verify market hours
- Try a different ticker to test
- Check internet connection

### Recommendations seem off
Remember:
- AI is not perfect
- Market conditions change
- Always do your own research
- Consider multiple sources

### Agent keeps crashing
Check:
- Logs in `logs/portfolio_agent.log`
- Error messages in console
- API rate limits
- Internet stability

Run the test script:
```bash
python test_setup.py
```

## Best Practices

### How should I use these recommendations?
1. Use as one data point, not the only one
2. Verify with your own analysis
3. Consider your risk tolerance
4. Never invest more than you can afford to lose
5. Consult financial advisors for major decisions

### What confidence score should I trust?
- **80-100%**: Strong signal, but still verify
- **70-79%**: Good signal, use caution
- **Below 70%**: Weak signal, likely HOLD

Always consider the reasoning, not just the score.

### How often should I check the recommendations?
Depends on your trading style:
- **Day trading**: Every few minutes (but note API limits)
- **Swing trading**: Few times per day
- **Long-term**: Once per day or less

### Should I act on every BUY signal?
No! Consider:
- Your portfolio diversification
- Current positions
- Risk management
- Market conditions
- Your investment strategy

## Data & Privacy

### What data is collected?
The agent only:
- Fetches public market data
- Accesses public news
- Stores recommendations locally
- Logs operations to local files

No personal data is sent anywhere.

### Is my API key secure?
- Store in `.env` file (excluded from git)
- Never commit to version control
- Keep `.env` file private
- Rotate keys periodically

### Where are recommendations stored?
Locally in:
- `output/recommendations/` - Individual files
- `output/history/` - Historical logs
- `logs/` - Application logs

## Advanced Usage

### Can I integrate this with my trading platform?
The agent provides JSON output that you can parse and use with trading APIs. Integration would require:
1. Reading recommendation files
2. Implementing trading logic
3. Connecting to broker API
4. Adding extensive error handling

**Warning**: Automated trading is risky. Test extensively!

### Can I add custom indicators?
Yes! Extend the `TechnicalAnalyzer` class or create your own modules. Contributions welcome!

### How do I backtest strategies?
Backtesting framework is planned for future release. Currently, you can:
1. Collect historical recommendations
2. Compare against actual market performance
3. Analyze accuracy over time

## Getting Help

### Where can I get help?
1. Read this FAQ
2. Check the main README
3. Review CONTRIBUTING.md
4. Open an issue on GitHub
5. Check existing issues for solutions

### How do I report a bug?
Open a GitHub issue with:
- Clear description
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Relevant logs

### Can I request features?
Yes! Open an issue describing:
- The feature
- Why it would be useful
- How it might work

## Contributing

### Can I contribute?
Absolutely! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### What skills do I need?
- Python programming
- Understanding of financial markets
- Git/GitHub basics
- Willingness to learn

### How do I submit changes?
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Didn't find your answer?** Open an issue on GitHub!
