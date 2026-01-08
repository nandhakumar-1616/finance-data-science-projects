import csv
import os
import yfinance
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
#learned about new library statsmodels for time series decomposition graph on 1/6
from statsmodels.tsa.seasonal import seasonal_decompose

#On Friday, write new methods that highlight key patterns in the chosen dataset; identify trends, seasonality, outliers, and relationships.

class exploratory_data_analysis:
    def __init__(self, filename):
        self.filename = filename

    def load_data(self):
        """Load data from CSV file"""
        data = []
        if not os.path.isfile(self.filename):
            print("File does not exist.")
            return data


        with open(self.filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data

    def summarize_data(self):
        """Provide summary statistics of the data"""
        data = self.load_data()
        if not data:
            print("No data to analyze.")
            return

        total_rows = len(data)
        print(f"Total Rows: {total_rows}")

        if total_rows > 0:
            sample_row = data[0]
            print("Sample Row:")
            for key, value in sample_row.items():
                print(f"  {key}: {value}")

    def analyze_column(self, column_name):
        """Analyze a specific column"""
        data = self.load_data()
        if not data:
            print("No data to analyze.")
            return

        column_values = [row[column_name] for row in data if column_name in row]
        unique_values = set(column_values)

        print(f"Column: {column_name}")
        print(f"Unique Values ({len(unique_values)}): {unique_values}")

    def download_stock_data(self, ticker='^GSPC', start='2020-01-01', end='2023-01-01'):
        """Download historical stock data using yfinance"""
        self.df = yfinance.download(ticker, start=start, end=end)
        return self.df

    def clean_data(self):
        """Clean the data"""
        self.df = self.df.dropna()
        self.df.index = pd.to_datetime(self.df.index)

    def summary_stats(self):
        """Print summary statistics"""
        print(self.df.describe())

    def plot_time_series(self):
        """Plot time series of closing prices"""
        plt.figure(figsize=(10, 5))
        plt.plot(self.df['Close'])
        plt.title('Stock Price Over Time')
        plt.xlabel('Date')
        plt.ylabel('Close Price')
        plt.show()

    def plot_histogram(self):
        """Plot histogram of closing prices"""
        plt.figure()
        sns.histplot(self.df['Close'], kde=True)
        plt.title('Distribution of Closing Prices')
        plt.show()

    def calculate_returns(self):
        """Calculate daily returns"""
        self.df['Returns'] = self.df['Close'].pct_change()
        self.df = self.df.dropna()
    
    def plot_returns_histogram(self):
        """Plot histogram of daily returns"""
        plt.figure()
        sns.histplot(self.df['Returns'], kde=True)
        plt.title('Distribution of Daily Returns')
        plt.show()


    def correlation_matrix(self):
        """Plot correlation matrix"""
        corr = self.df.corr()
        plt.figure()
        sns.heatmap(corr, annot=True, cmap='coolwarm')
        plt.title('Correlation Matrix')
        plt.show()


    def rolling_volatility(self):
        """Calculate and plot rolling volatility"""
        if 'Returns' not in self.df.columns:
            self.calculate_returns()
        self.df['Volatility'] = self.df['Returns'].rolling(window=30).std()
        plt.figure(figsize=(10, 5))
        plt.plot(self.df['Volatility'])
        plt.title('3 Year Rolling Volatility')
        plt.xlabel('Date')
        plt.ylabel('Volatility')
        plt.show()


    def decompose_time_series(self):
        """Decompose time series into trend, seasonal, residual"""
        decomposition = seasonal_decompose(self.df['Close'], model='additive', period=252)
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(10, 8))
        decomposition.observed.plot(ax=ax1)
        ax1.set_title('Observed')
        decomposition.trend.plot(ax=ax2)
        ax2.set_title('Trend')
        decomposition.seasonal.plot(ax=ax3)
        ax3.set_title('Seasonal')
        decomposition.resid.plot(ax=ax4)
        ax4.set_title('Residual')
        plt.tight_layout()
        plt.show()