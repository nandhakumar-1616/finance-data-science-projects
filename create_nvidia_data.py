#created data here because for some reason yfinance did not work 2/17

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests

end_date = datetime.now()
start_date = datetime(2019, 1, 1)

dates = pd.date_range(start=start_date, end=end_date, freq='W')

np.random.seed(42)
n_weeks = len(dates)

base_price = 20
trend = np.linspace(base_price, 140, n_weeks)
noise = np.random.normal(0, 5, n_weeks)
prices = trend + noise
prices = np.maximum(prices, base_price / 2)

volume = np.random.randint(40000000, 100000000, n_weeks)

data = {
    'Date': dates,
    'Open': prices + np.random.normal(0, 2, n_weeks),
    'High': prices + np.abs(np.random.normal(3, 1, n_weeks)),
    'Low': prices - np.abs(np.random.normal(3, 1, n_weeks)),
    'Close': prices,
    'Adj Close': prices,
    'Volume': volume
}

df = pd.DataFrame(data)

df['Open'] = np.maximum(df['Open'], 0.1)
df['High'] = np.maximum(df['High'], df[['Open', 'Close']].max(axis=1))
df['Low'] = np.minimum(df['Low'], df[['Open', 'Close']].min(axis=1))

for col in ['Open', 'High', 'Low', 'Close', 'Adj Close']:
    df[col] = df[col].round(2)

df.to_csv('nvidia_stock_weekly.csv', index=False)
print(f"Created nvidia_stock_weekly.csv with {len(df)} weekly records from {df['Date'].min().date()} to {df['Date'].max().date()}")
print(f"\nFirst few rows:")
print(df.head())
print(f"\nLast few rows:")
print(df.tail())
print(f"\nPrice range: ${df['Close'].min():.2f} - ${df['Close'].max():.2f}")
