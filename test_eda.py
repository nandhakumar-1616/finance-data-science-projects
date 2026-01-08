import sys
import os
sys.path.append('/workspaces/finance-data-science-projects/Python Projects')

from exploratory_data_analysis import exploratory_data_analysis
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Test CSV methods with suicide rates
eda = exploratory_data_analysis('/workspaces/finance-data-science-projects/world_suicide_rates.csv')

print("--- Testing CSV Methods ---")
print("1. load_data")
data = eda.load_data()
print(f"   Loaded {len(data)} rows")

print("2. summarize_data")
eda.summarize_data()

print("3. analyze_column('Country Name')")
eda.analyze_column('Country Name')

print("4. analyze_column('Year')")
eda.analyze_column('Year')

print("5. analyze_column('Suicide Rate')")
eda.analyze_column('Suicide Rate')

# Test stock methods
print("\n--- Testing Stock Methods ---")
print("6. download_stock_data")
df = eda.download_stock_data()
print(f"   Downloaded data shape: {df.shape}")

print("7. clean_data")
eda.clean_data()
print(f"   After cleaning shape: {eda.df.shape}")

print("8. summary_stats")
eda.summary_stats()

print("9. plot_time_series")
eda.plot_time_series()
plt.savefig('time_series_plot.png')
print("   Plot saved as time_series_plot.png")

print("10. plot_histogram")
eda.plot_histogram()
plt.savefig('histogram_plot.png')
print("    Plot saved as histogram_plot.png")

print("11. calculate_returns")
eda.calculate_returns()
print("    Returns calculated")

print("12. plot_returns_histogram")
eda.plot_returns_histogram()
plt.savefig('returns_histogram_plot.png')
print("    Plot saved as returns_histogram_plot.png")

print("13. correlation_matrix")
eda.correlation_matrix()
plt.savefig('correlation_matrix_plot.png')
print("    Plot saved as correlation_matrix_plot.png")

print("14. rolling_volatility")
eda.rolling_volatility()
plt.savefig('rolling_volatility_plot.png')
print("    Plot saved as rolling_volatility_plot.png")

print("15. decompose_time_series")
eda.decompose_time_series()
plt.savefig('decompose_time_series_plot.png')
print("    Plot saved as decompose_time_series_plot.png")

print("\nAll methods executed successfully")