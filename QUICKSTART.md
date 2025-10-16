# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Install Dependencies

```bash
chmod +x setup.sh
./setup.sh
```

Or manually:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Get Your Gemini API Key

1. Go to https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key

### 3. Configure Environment

```bash
cp .env.example .env
nano .env  # Add your GEMINI_API_KEY
```

### 4. Set Up Your Portfolio

Edit `portfolio.json`:
```json
{
  "portfolio": [
    {"ticker": "AAPL", "name": "Apple Inc.", "market": "NASDAQ"},
    {"ticker": "MSFT", "name": "Microsoft", "market": "NASDAQ"}
  ]
}
```

### 5. Run the Agent

```bash
python main.py
```

## 📊 Example Commands

### Analyze Everything Once
```bash
python main.py --single
```

### Analyze One Stock
```bash
python main.py --ticker AAPL
```

### Continuous Monitoring
```bash
python main.py
```

## 🎯 What to Expect

The agent will:
1. ✅ Fetch live prices
2. ✅ Analyze technical indicators (RSI, MACD, etc.)
3. ✅ Check latest news and sentiment
4. ✅ Calculate risk levels
5. ✅ Generate BUY/SELL/HOLD recommendation

Output location:
- Console: Real-time display
- Files: `output/recommendations/`
- Logs: `logs/portfolio_agent.log`

## ⚠️ Important Notes

- **Free API**: Gemini has a generous free tier
- **Rate Limits**: Default 60s between cycles to avoid limits
- **Market Hours**: Best results during trading hours
- **Disclaimer**: This is NOT financial advice!

## 🐛 Troubleshooting

**Missing API Key?**
```bash
export GEMINI_API_KEY="your-key-here"
```

**Module not found?**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

**No data for ticker?**
- Check ticker symbol is correct
- Try during market hours
- Verify internet connection

## 📚 Learn More

See `README.md` for complete documentation.
