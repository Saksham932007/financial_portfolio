# Example Portfolios

This directory contains sample portfolio configurations to help you get started.

## Available Examples

### 1. Tech Stocks (`portfolio_tech_stocks.json`)

Major technology companies:

- AAPL (Apple)
- MSFT (Microsoft)
- GOOGL (Google/Alphabet)
- AMZN (Amazon)
- NVDA (NVIDIA)
- TSLA (Tesla)
- META (Meta/Facebook)

**Usage:**

```bash
python main.py --portfolio examples/portfolio_tech_stocks.json
```

### 2. ETFs (`portfolio_etfs.json`)

Popular index and sector ETFs:

- SPY (S&P 500)
- QQQ (NASDAQ-100)
- DIA (Dow Jones)
- IWM (Russell 2000)
- VTI (Total Stock Market)

**Usage:**

```bash
python main.py --portfolio examples/portfolio_etfs.json
```

### 3. Forex & Crypto (`portfolio_forex.json`)

Major forex pairs and cryptocurrencies:

- EUR/USD
- GBP/USD
- USD/JPY
- AUD/USD
- BTC-USD (Bitcoin)
- ETH-USD (Ethereum)

**Usage:**

```bash
python main.py --portfolio examples/portfolio_forex.json
```

## Creating Your Own Portfolio

Create a JSON file with this structure:

```json
{
  "portfolio": [
    {
      "ticker": "SYMBOL",
      "name": "Company Name",
      "market": "NASDAQ|NYSE|FOREX|CRYPTO"
    }
  ],
  "watchlist": [
    {
      "ticker": "SYMBOL",
      "name": "Company Name",
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

### Ticker Symbol Formats

- **Stocks**: Use standard ticker (e.g., `AAPL`, `MSFT`)
- **Forex**: Add `=X` suffix (e.g., `EURUSD=X`, `GBPUSD=X`)
- **Crypto**: Use `-USD` suffix (e.g., `BTC-USD`, `ETH-USD`)
- **Indices**: Use `^` prefix (e.g., `^GSPC` for S&P 500)

### Tips

1. **Start Small**: Begin with 3-5 tickers to test
2. **Mix Assets**: Combine stocks, ETFs, and forex for diversification
3. **Update Regularly**: Keep your portfolio file current
4. **Test First**: Use `--single` flag to test before continuous monitoring

```bash
python main.py --portfolio myportfolio.json --single
```
