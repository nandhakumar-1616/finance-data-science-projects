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

class exploratory_data_analysis:
    def __init__(self, filename):
        self.filename = filename

    def load_data(self):
        data = []
        if not os.path.isfile(self.filename):
            print("File does not exist.")
            return data


        with open(self.filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data

    def load_data_pandas(self):
        if not os.path.isfile(self.filename):
            print("File does not exist.")
            return None
        self.df = pd.read_csv(self.filename)
        return self.df

    def summarize_data(self):
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
        data = self.load_data()
        if not data:
            print("No data to analyze.")
            return

        column_values = [row[column_name] for row in data if column_name in row]
        unique_values = set(column_values)

        print(f"Column: {column_name}")
        print(f"Unique Values ({len(unique_values)}): {unique_values}")

    def download_stock_data(self, ticker='^GSPC', start='2020-01-01', end='2023-01-01'):
        self.df = yfinance.download(ticker, start=start, end=end)
        return self.df

    def clean_data(self):
        self.df = self.df.dropna()
        self.df.index = pd.to_datetime(self.df.index)

    def summary_stats(self):
        print(self.df.describe())

    def plot_time_series(self):
        plt.figure(figsize=(10, 5))
        plt.plot(self.df['Close'])
        plt.title('Stock Price Over Time')
        plt.xlabel('Date')
        plt.ylabel('Close Price')
        plt.show()

    def plot_histogram(self):
        plt.figure()
        sns.histplot(self.df['Close'], kde=True)
        plt.title('Distribution of Closing Prices')
        plt.show()

    def calculate_returns(self):
        self.df['Returns'] = self.df['Close'].pct_change()
        self.df = self.df.dropna()
    
    def plot_returns_histogram(self):
        plt.figure()
        sns.histplot(self.df['Returns'], kde=True)
        plt.title('Distribution of Daily Returns')
        plt.show()


    def correlation_matrix(self):
        corr = self.df.corr()
        plt.figure()
        sns.heatmap(corr, annot=True, cmap='coolwarm')
        plt.title('Correlation Matrix')
        plt.show()


    def rolling_volatility(self):
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

    def check_data_quality(self):
        if not hasattr(self, 'df') or self.df is None:
            print("Data not loaded. Please load data first.")
            return
        print("Data Shape:", self.df.shape)
        print("\nData Types:")
        print(self.df.dtypes)
        print("\nMissing Values per Column:")
        print(self.df.isnull().sum())
        print(f"\nTotal Duplicates: {self.df.duplicated().sum()}")

    def detect_outliers(self, column_name):
        if not hasattr(self, 'df') or self.df is None:
            print("Data not loaded.")
            return None
        if column_name not in self.df.columns:
            print(f"Column '{column_name}' not found.")
            return None
        if not pd.api.types.is_numeric_dtype(self.df[column_name]):
            print(f"Column '{column_name}' is not numeric.")
            return None
        Q1 = self.df[column_name].quantile(0.25)
        Q3 = self.df[column_name].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = self.df[(self.df[column_name] < lower_bound) | (self.df[column_name] > upper_bound)]
        print(f"Outliers in '{column_name}': {len(outliers)} rows")
        print(f"Lower bound: {lower_bound}, Upper bound: {upper_bound}")
        return outliers

    def plot_trends(self, date_column, value_column):
        if not hasattr(self, 'df') or self.df is None:
            print("Data not loaded.")
            return
        if date_column not in self.df.columns or value_column not in self.df.columns:
            print("Specified columns not found.")
            return
        temp_df = self.df.copy()
        temp_df[date_column] = pd.to_datetime(temp_df[date_column], errors='coerce')
        temp_df = temp_df.dropna(subset=[date_column])
        plt.figure(figsize=(12, 6))
        plt.plot(temp_df[date_column], temp_df[value_column])
        plt.title(f'Trend of {value_column} over {date_column}')
        plt.xlabel(date_column)
        plt.ylabel(value_column)
        plt.xticks(rotation=45)
        plt.show()

    def analyze_relationships(self):
        if not hasattr(self, 'df') or self.df is None:
            print("Data not loaded.")
            return
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) < 2:
            print("Not enough numeric columns for correlation analysis.")
            return
        corr_matrix = self.df[numeric_cols].corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
        plt.title('Correlation Matrix')
        plt.show()