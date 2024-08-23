import pandas as pd
import numpy as np
from time_series_labeler import TimeSeriesLabeler

# Create a sample time series dataframe
dates = pd.date_range(start='2023-01-01', periods=1000, freq='h')
df = pd.DataFrame({
    'timestamp': dates,
    'temperature': np.sin(np.arange(1000) * 2 * np.pi / 24) + np.random.normal(0, 0.2, 1000) + 20,
    'humidity': np.cos(np.arange(1000) * 2 * np.pi / 24) + np.random.normal(0, 0.1, 1000) + 50
})
df.set_index('timestamp', inplace=True)

# Create a TimeSeriesLabeler instance
labeler = TimeSeriesLabeler(df)

# Plot the data and save it as an HTML file
labeler.plot()
labeler.fig.write_html("time_series_plot.html")

print("Time series plot saved as 'time_series_plot.html'")

# Simulate labeling some data
df['label'] = ''
df.loc['2023-01-01':'2023-01-02', 'label'] = 'Cold'
df.loc['2023-01-03':'2023-01-04', 'label'] = 'Warm'
df.loc['2023-01-05':'2023-01-06', 'label'] = 'Hot'

print("\nSimulated label statistics:")
print(df['label'].value_counts())

print("\nFirst few rows of the labeled dataframe:")
print(df.head())