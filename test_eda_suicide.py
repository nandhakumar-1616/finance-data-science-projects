import sys
import os
sys.path.append('/workspaces/finance-data-science-projects/Python Projects')

from exploratory_data_analysis import exploratory_data_analysis
import matplotlib
matplotlib.use('Agg')

eda = exploratory_data_analysis('/workspaces/finance-data-science-projects/world_suicide_rates.csv')

# Test load_data
print("Testing load_data...")
try:
    data = eda.load_data()
    print(f"Success: Loaded {len(data)} rows")
except Exception as e:
    print(f"Error: {e}")

# Test load_data_pandas
print("\nTesting load_data_pandas...")
try:
    df = eda.load_data_pandas()
    print(f"Success: Loaded DataFrame with shape {df.shape}")
except Exception as e:
    print(f"Error: {e}")

# Test summarize_data
print("\nTesting summarize_data...")
try:
    eda.summarize_data()
    print("Success")
except Exception as e:
    print(f"Error: {e}")

# Test analyze_column
print("\nTesting analyze_column...")
try:
    eda.analyze_column('Country Name')
    print("Success")
except Exception as e:
    print(f"Error: {e}")

# Test check_data_quality
print("\nTesting check_data_quality...")
try:
    eda.check_data_quality()
    print("Success")
except Exception as e:
    print(f"Error: {e}")

# Test detect_outliers
print("\nTesting detect_outliers...")
try:
    outliers = eda.detect_outliers('Suicide Rate')
    print(f"Success: Found {len(outliers)} outliers")
except Exception as e:
    print(f"Error: {e}")

# Test plot_trends
print("\nTesting plot_trends...")
try:
    eda.plot_trends('Year', 'Suicide Rate')
    print("Success")
except Exception as e:
    print(f"Error: {e}")

# Test analyze_relationships
print("\nTesting analyze_relationships...")
try:
    eda.analyze_relationships()
    print("Success")
except Exception as e:
    print(f"Error: {e}")

# Test download_stock_data - this downloads stock data, not using CSV
print("\nTesting download_stock_data...")
try:
    stock_df = eda.download_stock_data()
    print(f"Success: Downloaded stock data with shape {stock_df.shape}")
except Exception as e:
    print(f"Error: {e}")

# Assuming stock data loaded, test clean_data
print("\nTesting clean_data...")
try:
    eda.clean_data()
    print("Success")
except Exception as e:
    print(f"Error: {e}")

# summary_stats
print("\nTesting summary_stats...")
try:
    eda.summary_stats()
    print("Success")
except Exception as e:
    print(f"Error: {e}")

# plot_time_series
print("\nTesting plot_time_series...")
try:
    eda.plot_time_series()
    print("Success")
except Exception as e:
    print(f"Error: {e}")

# plot_histogram
print("\nTesting plot_histogram...")
try:
    eda.plot_histogram()
    print("Success")
except Exception as e:
    print(f"Error: {e}")

# calculate_returns
print("\nTesting calculate_returns...")
try:
    eda.calculate_returns()
    print("Success")
except Exception as e:
    print(f"Error: {e}")

# plot_returns_histogram
print("\nTesting plot_returns_histogram...")
try:
    eda.plot_returns_histogram()
    print("Success")
except Exception as e:
    print(f"Error: {e}")

# correlation_matrix
print("\nTesting correlation_matrix...")
try:
    eda.correlation_matrix()
    print("Success")
except Exception as e:
    print(f"Error: {e}")

# rolling_volatility
print("\nTesting rolling_volatility...")
try:
    eda.rolling_volatility()
    print("Success")
except Exception as e:
    print(f"Error: {e}")

# decompose_time_series
print("\nTesting decompose_time_series...")
try:
    eda.decompose_time_series()
    print("Success")
except Exception as e:
    print(f"Error: {e}")

print("\nAll tests completed.")