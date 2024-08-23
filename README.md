# Time Series Labeler

A Python library for interactive labeling of time series data with advanced features.

## Installation

```bash
pip install time_series_labeler
```

## Features

- Support for both univariate and multivariate time series data
- Interactive plotting using Plotly
- User-friendly labeling interface
- Color-coded labels for easy visualization
- Ability to edit or delete existing labels
- Zoom and pan functionality
- Export and import label data
- Automatic label suggestions based on K-means clustering
- Output as a labeled time series dataframe

## Usage

```python
import pandas as pd
import numpy as np
from time_series_labeler import TimeSeriesLabeler

# Create a sample time series dataframe
df = pd.DataFrame({
    'timestamp': pd.date_range(start='2023-01-01', periods=100, freq='H'),
    'value1': np.random.randn(100),
    'value2': np.random.randn(100)
})
df.set_index('timestamp', inplace=True)

# Create a TimeSeriesLabeler instance
labeler = TimeSeriesLabeler(df)

# Start the interactive labeling process
labeled_df = labeler.label()

# The resulting labeled_df will contain the original data with an additional 'label' column
print(labeled_df)
```

## Interactive Labeling Process

1. Enter a label in the "Label" text box.
2. Click "Start" to begin labeling a region.
3. Click "End" to finish labeling the region.
4. Click "Apply Label" to add the label to the selected region.
5. Use "Delete Label" to remove the most recently added label.
6. "Export Labels" saves the current labels to a JSON file.
7. "Import Labels" loads previously saved labels from a JSON file.
8. "Suggest Labels" uses K-means clustering to automatically suggest labels.

## Requirements

- pandas
- numpy
- plotly
- ipywidgets
- scikit-learn

## License

This project is licensed under the MIT License.