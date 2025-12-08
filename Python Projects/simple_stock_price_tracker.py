import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
import argparse

def get_stock_data(ticker_symbol="AAPL", period="1y"):
    """
    Fetches real-time info and historical data for a given ticker symbol.
    """
    stock = yf.Ticker(ticker_symbol)

    # Fetch real-time info (current price, market cap, etc.)
    stock_info = stock.info
    
    # Fetch historical data for the last year
    historical_data = stock.history(period=period)

    if not historical_data.empty:
        # Get current price (last closing price from the historical data)
        current_price = historical_data['Close'].iloc[-1]

        # Get market cap (if available in info)
        market_cap = stock_info.get('marketCap', 'N/A')
        
        print(f"--- Stock Information for {ticker_symbol} ---")
        print(f"Current Price: ${current_price:.2f}")

        if market_cap != 'N/A':
            print(f"Market Cap: ${market_cap/1e12:.2f}T")
        else:
            print("Market Cap: N/A")
        
        historical_data = compute_metrics(historical_data)
        show_metrics(historical_data, stock_info, ticker_symbol)

        # Plot the closing prices with moving averages
        plot_stock_data(historical_data, ticker_symbol)
    else:
        print(f"No data available for ticker symbol: {ticker_symbol}")

def plot_stock_data(data, ticker_symbol):
    """
    Plots the closing price history using matplotlib.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(data['Close'], label='Closing Price', color='blue')
    # Plot moving averages if present
    if 'SMA_50' in data.columns:
        plt.plot(data['SMA_50'], label='50-day SMA', color='orange', linewidth=1.25)
    if 'SMA_200' in data.columns:
        plt.plot(data['SMA_200'], label='200-day SMA', color='green', linewidth=1.25)
    plt.title(f"{ticker_symbol} Stock Closing Prices (Last Year)")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.grid(True)
    plt.show()


def compute_metrics(data: pd.DataFrame) -> pd.DataFrame:
    """
    Adds common finance metrics to the historical price DataFrame:
      - Daily returns
      - Cumulative returns
      - 50/200 day simple moving averages
      - Rolling 30-day volatility
      - Drawdown
    Returns the DataFrame with new columns added.
    """
    data = data.copy()
    # Daily percent change
    data['Return'] = data['Close'].pct_change()

    # Cumulative returns
    data['Cumulative Return'] = (1 + data['Return']).cumprod() - 1

    # Simple Moving Averages
    data['SMA_50'] = data['Close'].rolling(window=50, min_periods=1).mean()
    data['SMA_200'] = data['Close'].rolling(window=200, min_periods=1).mean()

    # Rolling volatility (30-day)
    data['Rolling Volatility (30d)'] = data['Return'].rolling(window=30, min_periods=1).std()

    # Rolling maximum drawdown
    data['Cumulative Max'] = data['Close'].cummax()
    data['Drawdown'] = data['Close'] / data['Cumulative Max'] - 1

    return data


def show_metrics(data: pd.DataFrame, stock_info: dict, ticker_symbol: str, tail: int = 5) -> None:
    """
    Prints a summary of useful metrics calculated from the price data.
    """
    # Latest values
    latest = data.iloc[-1]
    first = data.iloc[0]

    last_price = latest['Close']
    total_return = last_price / first['Close'] - 1
    mean_daily_return = data['Return'].mean()
    std_daily_return = data['Return'].std()
    annualised_return = mean_daily_return * 252
    annualised_volatility = std_daily_return * np.sqrt(252)
    sharpe_ratio = (annualised_return / annualised_volatility) if annualised_volatility != 0 else np.nan
    max_drawdown = data['Drawdown'].min()

    market_cap = stock_info.get('marketCap', None)

    print('\n--- Additional Metrics (Pandas) ---')
    print(f"Last Close: ${last_price:.2f}")
    print(f"Total Return (period): {total_return*100:.2f}%")
    print(f"Mean Daily Return: {mean_daily_return*100:.4f}%")
    print(f"Daily Volatility (std): {std_daily_return*100:.4f}%")
    print(f"Annualised Return: {annualised_return*100:.2f}%")
    print(f"Annualised Volatility: {annualised_volatility*100:.2f}%")
    print(f"Sharpe Ratio (rf=0): {sharpe_ratio:.2f}")
    print(f"Max Drawdown: {max_drawdown*100:.2f}%")
    if market_cap:
        print(f"Market Cap: ${market_cap:,.0f}")

    #Table of recent data
    cols_to_show = ['Close', 'Return', 'Cumulative Return', 'SMA_50', 'SMA_200', 'Rolling Volatility (30d)', 'Drawdown']
    existing_cols = [c for c in cols_to_show if c in data.columns]
    print('\nRecent data:')
    print(data[existing_cols].tail(tail).to_string())

def main():
    parser = argparse.ArgumentParser(description="Simple Stock Price Tracker with pandas metrics")
    parser.add_argument('ticker', nargs='?', default='AAPL', help='Ticker symbol (default: AAPL)')
    parser.add_argument('--period', default='1y', help='History period for yfinance (default: 1y)')
    args = parser.parse_args()
    get_stock_data(args.ticker, period=args.period)

if __name__ == "__main__":
    main()