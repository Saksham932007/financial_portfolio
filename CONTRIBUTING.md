# Contributing to AI Financial Portfolio Manager

Thank you for your interest in contributing to this project! This document provides guidelines for contributing.

## 🎯 How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:

- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (Python version, OS, etc.)
- Relevant logs or error messages

### Suggesting Enhancements

For feature requests:

- Describe the feature and its benefits
- Explain how it would work
- Consider edge cases and potential issues

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**

   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed

4. **Test your changes**

   ```bash
   python test_setup.py
   ```

5. **Commit with clear messages**

   ```bash
   git commit -m "feat: Add new feature"
   ```

   Use conventional commit format:

   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation changes
   - `test:` - Test additions or changes
   - `refactor:` - Code refactoring
   - `style:` - Code style changes
   - `chore:` - Maintenance tasks

6. **Push to your fork**

   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Describe your changes clearly
   - Reference any related issues
   - Wait for review

## 📝 Code Style

### Python Style Guide

- Follow PEP 8
- Use type hints where appropriate
- Add docstrings to functions and classes
- Keep functions focused and small
- Use meaningful variable names

Example:

```python
def calculate_risk_level(
    current_price: float,
    historical_data: pd.DataFrame
) -> Dict[str, Any]:
    """
    Calculate risk management levels.

    Args:
        current_price: Current stock price
        historical_data: Historical OHLCV data

    Returns:
        Dictionary with stop-loss and take-profit levels
    """
    # Implementation
    pass
```

### Documentation

- Update README.md for new features
- Add examples where helpful
- Keep documentation clear and concise
- Include code examples

### Testing

- Test your code before submitting
- Ensure existing tests still pass
- Add new tests for new features
- Test edge cases

## 🏗️ Development Setup

1. Clone your fork:

   ```bash
   git clone https://github.com/YOUR_USERNAME/financial_portfolio.git
   cd financial_portfolio
   ```

2. Create virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create .env:

   ```bash
   cp .env.example .env
   # Add your API keys
   ```

5. Test the setup:
   ```bash
   python test_setup.py
   ```

## 🎨 Areas for Contribution

### High Priority

- [ ] Backtesting framework
- [ ] Performance analytics
- [ ] Unit tests for all modules
- [ ] Error handling improvements
- [ ] Rate limiting optimization

### Medium Priority

- [ ] Web dashboard
- [ ] Additional data sources
- [ ] More technical indicators
- [ ] Portfolio optimization
- [ ] Multi-timeframe analysis

### Documentation

- [ ] Video tutorials
- [ ] More examples
- [ ] FAQ section
- [ ] Troubleshooting guide

### Code Quality

- [ ] Type hint coverage
- [ ] Docstring completeness
- [ ] Code refactoring
- [ ] Performance optimization

## 📊 Project Structure

Understanding the codebase:

```
financial_portfolio/
├── main.py                    # Entry point
├── src/
│   ├── config.py             # Configuration
│   ├── data_fetcher.py       # Market data
│   ├── technical_analyzer.py # Technical analysis
│   ├── sentiment_analyzer.py # Sentiment analysis
│   ├── recommendation_engine.py # Recommendations
│   ├── risk_manager.py       # Risk management
│   ├── output_handler.py     # Output formatting
│   └── utils/
│       └── logger.py         # Logging
└── examples/                  # Example configs
```

## 🤝 Code of Conduct

- Be respectful and constructive
- Welcome newcomers
- Focus on the code, not the person
- Give and receive feedback gracefully

## ❓ Questions?

- Check existing issues and pull requests
- Read the documentation thoroughly
- Ask in issue comments if unclear

## 🙏 Recognition

Contributors will be recognized in the project README!

---

Thank you for contributing to make this project better! 🚀
