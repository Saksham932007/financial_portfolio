# Performance Tips & Optimization Guide

## Overview

This guide helps you optimize the AI Financial Portfolio Manager for better performance and efficiency.

## Quick Wins

### 1. Reduce Update Interval

For long-term investing:

```env
UPDATE_INTERVAL_SECONDS=300  # 5 minutes instead of 60 seconds
```

For day trading (careful with rate limits):

```env
UPDATE_INTERVAL_SECONDS=30  # 30 seconds
```

### 2. Limit Portfolio Size

Start with 3-5 stocks and gradually increase:

```json
{
  "portfolio": [
    { "ticker": "AAPL", "name": "Apple", "market": "NASDAQ" },
    { "ticker": "MSFT", "name": "Microsoft", "market": "NASDAQ" },
    { "ticker": "GOOGL", "name": "Google", "market": "NASDAQ" }
  ]
}
```

### 3. Use Caching Effectively

Built-in caching is 60 seconds. Data is automatically reused within this window.

## API Optimization

### Gemini API

**Rate Limits** (Free tier):

- 60 requests per minute
- 1,500 requests per day

**Tips**:

1. Increase update interval
2. Reduce number of stocks
3. Use single analysis mode for testing
4. Consider upgrading to paid tier for production

### yfinance Data

**Best Practices**:

- Data is free and unlimited
- But respect their servers
- Cache is built-in (60s)
- Fetch historical data only when needed

## Memory Optimization

### For Large Portfolios

```python
# Limit historical data period
historical = fetcher.get_historical_data('AAPL', period='6mo')  # vs '5y'
```

### For Raspberry Pi or Low-Memory Systems

```env
MAX_CONCURRENT_STOCKS=5  # Instead of 10
```

Monitor memory:

```bash
docker stats portfolio-agent  # If using Docker
```

## Speed Improvements

### 1. Parallel Processing (Future Enhancement)

Currently processes sequentially. Future versions may support:

- Concurrent API calls
- Parallel technical analysis
- Async operations

### 2. Database Integration (Future)

For faster historical data access:

- Store recommendations in SQLite
- Cache technical indicators
- Reduce redundant calculations

### 3. Skip Steps for Quick Analysis

Modify `main.py` to skip sentiment for quick technical-only analysis.

## Network Optimization

### Use Fast Internet

- Stable connection is crucial
- VPN may add latency
- Cloud deployments: choose region near APIs

### Reduce Data Transfer

```python
# Fetch only needed data
historical = fetcher.get_historical_data('AAPL', period='1mo')  # Minimal for quick RSI
```

## Configuration Tuning

### For Swing Trading

```env
UPDATE_INTERVAL_SECONDS=1800  # 30 minutes
RSI_PERIOD=14
MACD_FAST_PERIOD=12
MACD_SLOW_PERIOD=26
```

### For Day Trading

```env
UPDATE_INTERVAL_SECONDS=60  # 1 minute
RSI_PERIOD=9  # Faster response
MACD_FAST_PERIOD=8
MACD_SLOW_PERIOD=17
```

### For Long-Term Investing

```env
UPDATE_INTERVAL_SECONDS=3600  # 1 hour
MA_PERIODS=[100, 200, 300]  # Longer periods
```

## Logging Optimization

### Reduce Log Verbosity

```env
LOG_LEVEL=WARNING  # Instead of DEBUG or INFO
```

### Log Rotation

Add to your deployment:

```bash
# Linux logrotate
/path/to/logs/*.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
}
```

## Docker Optimization

### Multi-Stage Build

```dockerfile
# Future optimization: Multi-stage build
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.11-slim
COPY --from=builder /root/.local /root/.local
COPY . /app
WORKDIR /app
CMD ["python", "main.py"]
```

### Resource Limits

```yaml
# docker-compose.yml
services:
  portfolio-agent:
    mem_limit: 512m
    cpus: 1.0
```

## Monitoring & Profiling

### Check Performance

```python
import time

start = time.time()
# Your code
print(f"Execution time: {time.time() - start:.2f}s")
```

### Monitor API Calls

Check logs for:

- API response times
- Failed requests
- Rate limit warnings

```bash
grep "API call" logs/portfolio_agent.log
```

### Track Recommendations

```python
# Count recommendations per day
import json
import glob

files = glob.glob('output/history/*.jsonl')
for file in files:
    with open(file) as f:
        count = sum(1 for _ in f)
    print(f"{file}: {count} recommendations")
```

## Cost Optimization

### Gemini API Costs

Free tier limits:

- 60 RPM (requests per minute)
- 1,500 RPD (requests per day)

With 10 stocks and 60s interval:

- 10 stocks × 3 API calls each = 30 calls per cycle
- 1 cycle per minute = 30-40 calls per minute
- **You'll hit rate limits!**

**Solutions**:

1. Reduce stocks to 5
2. Increase interval to 120s
3. Upgrade to paid tier

### Paid Tier (if needed)

- Pay-as-you-go pricing
- Higher rate limits
- For serious production use

## Benchmarks

### Typical Performance

Single stock analysis:

- Data fetch: 1-2s
- Technical analysis: 2-3s
- Sentiment analysis: 3-5s
- Recommendation: 2-3s
- **Total: ~10-15s per stock**

10 stocks:

- Sequential: ~2-3 minutes
- With optimizations: ~1-2 minutes

### Hardware Requirements

**Minimum**:

- 1 CPU core
- 512MB RAM
- Stable internet

**Recommended**:

- 2+ CPU cores
- 1GB+ RAM
- Fast internet (10+ Mbps)

**Optimal**:

- 4+ CPU cores
- 2GB+ RAM
- Cloud deployment (low latency)

## Future Optimizations

Planned improvements:

- [ ] Async API calls
- [ ] Parallel processing
- [ ] Database caching
- [ ] WebSocket streaming
- [ ] Intelligent throttling
- [ ] Smart cache invalidation
- [ ] Historical data persistence

## Troubleshooting Slow Performance

### Symptom: Each stock takes >30s

**Check**:

1. Internet speed
2. API response times in logs
3. Gemini API key validity

### Symptom: Memory growing

**Fix**:

1. Reduce portfolio size
2. Clear cache periodically
3. Restart agent daily

### Symptom: Rate limit errors

**Fix**:

1. Increase UPDATE_INTERVAL_SECONDS
2. Reduce number of stocks
3. Check API quotas

## Best Practices Summary

1. ✅ Start small (3-5 stocks)
2. ✅ Use appropriate update intervals
3. ✅ Monitor API usage
4. ✅ Log at WARNING level in production
5. ✅ Use Docker for consistent performance
6. ✅ Deploy on cloud for 24/7 operation
7. ✅ Regular monitoring and maintenance
8. ✅ Respect API rate limits

---

For more help, see [FAQ.md](FAQ.md) or open an issue on GitHub.
