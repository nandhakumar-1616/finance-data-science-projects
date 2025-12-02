# finance-data-science-projects

Simple Stock Price Tracker — a minimal script that fetches stock quotes using `yfinance`, calculates additional metrics with `pandas`, and plots closing prices with moving averages.

## Requirements
- Python 3
- pandas
- numpy
- matplotlib
- yfinance

## Usage
```bash
python3 "Simple Stock Price Tracker" [TICKER] [--period PERIOD]
```
Examples:
```bash
python3 "Simple Stock Price Tracker" AAPL --period 1y
python3 "Simple Stock Price Tracker" MSFT --period 6mo
```

## Metrics shown
- Latest Close
- Total return for the period
- Mean daily return
- Daily volatility (std)
- Annualised return and volatility (assuming ~252 trading days)
- Sharpe Ratio (risk-free rate assumed to be 0)
- Maximum drawdown
- Recent rows with key computed columns: closing price, returns, cumulative returns, 50/200-day SMA, rolling volatility, drawdown

Plots include:
- Closing price history
- 50-day and 200-day simple moving averages (if present)

Note: This script prints a short table of recent data and computes the above metrics using `pandas`.