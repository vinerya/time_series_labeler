import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import ipywidgets as widgets
from IPython.display import display
import json
from sklearn.cluster import KMeans

class TimeSeriesLabeler:
    def __init__(self, df):
        self.df = df
        self.fig = None
        self.current_label = None
        self.labels = []
        self.label_start = None
        self.label_end = None
        self.colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
        self.label_colors = {}
        self.label_shapes = []

    def plot(self):
        columns = self.df.columns
        num_cols = len(columns)
        
        self.fig = make_subplots(rows=num_cols, cols=1, shared_xaxes=True, vertical_spacing=0.02)
        
        for i, col in enumerate(columns, start=1):
            self.fig.add_trace(go.Scatter(x=self.df.index, y=self.df[col], name=col), row=i, col=1)
        
        self.fig.update_layout(height=200*num_cols, title_text="Time Series Data", showlegend=True)
        self.fig.update_xaxes(rangeslider_visible=True)
        self.fig.show()

    def create_label_widgets(self):
        self.label_input = widgets.Text(description="Label:")
        start_button = widgets.Button(description="Start")
        end_button = widgets.Button(description="End")
        apply_button = widgets.Button(description="Apply Label")
        delete_button = widgets.Button(description="Delete Label")
        export_button = widgets.Button(description="Export Labels")
        import_button = widgets.Button(description="Import Labels")
        suggest_button = widgets.Button(description="Suggest Labels")
        
        start_button.on_click(self.on_start_click)
        end_button.on_click(self.on_end_click)
        apply_button.on_click(self.on_apply_click)
        delete_button.on_click(self.on_delete_click)
        export_button.on_click(self.on_export_click)
        import_button.on_click(self.on_import_click)
        suggest_button.on_click(self.on_suggest_click)
        
        display(widgets.VBox([
            widgets.HBox([self.label_input, start_button, end_button, apply_button]),
            widgets.HBox([delete_button, export_button, import_button, suggest_button])
        ]))

    def on_start_click(self, b):
        self.label_start = self.fig.layout.xaxis.range[0]
        self.current_label = self.label_input.value

    def on_end_click(self, b):
        self.label_end = self.fig.layout.xaxis.range[1]

    def on_apply_click(self, b):
        if self.label_start and self.label_end and self.current_label:
            if self.current_label not in self.label_colors:
                self.label_colors[self.current_label] = self.colors[len(self.label_colors) % len(self.colors)]
            
            self.labels.append((self.label_start, self.label_end, self.current_label))
            self.add_label_shape(self.label_start, self.label_end, self.current_label)
            
            self.label_start = None
            self.label_end = None
            self.current_label = None
            self.label_input.value = ""
            self.update_plot()

    def add_label_shape(self, start, end, label):
        color = self.label_colors[label]
        shape = dict(
            type="rect",
            xref="x",
            yref="paper",
            x0=start,
            y0=0,
            x1=end,
            y1=1,
            fillcolor=color,
            opacity=0.3,
            layer="below",
            line_width=0,
        )
        self.label_shapes.append(shape)

    def update_plot(self):
        self.fig.update_layout(shapes=self.label_shapes)
        self.fig.show()

    def on_delete_click(self, b):
        self.labels = self.labels[:-1]
        self.label_shapes = self.label_shapes[:-1]
        self.update_plot()

    def on_export_click(self, b):
        with open('labels.json', 'w') as f:
            json.dump(self.labels, f)
        print("Labels exported to labels.json")

    def on_import_click(self, b):
        try:
            with open('labels.json', 'r') as f:
                self.labels = json.load(f)
            self.label_shapes = []
            for start, end, label in self.labels:
                self.add_label_shape(start, end, label)
            self.update_plot()
            print("Labels imported from labels.json")
        except FileNotFoundError:
            print("No labels.json file found")

    def on_suggest_click(self, b):
        # Simple suggestion based on K-means clustering
        data = self.df.values
        n_clusters = min(5, len(data) // 10)  # Adjust the number of clusters as needed
        kmeans = KMeans(n_clusters=n_clusters)
        labels = kmeans.fit_predict(data)
        
        for i in range(n_clusters):
            cluster_points = data[labels == i]
            start = self.df.index[labels == i][0]
            end = self.df.index[labels == i][-1]
            suggested_label = f"Cluster_{i+1}"
            self.labels.append((start, end, suggested_label))
            self.add_label_shape(start, end, suggested_label)
        
        self.update_plot()
        print(f"Added {n_clusters} suggested labels based on K-means clustering")

    def label(self):
        self.plot()
        self.create_label_widgets()
        
        # Wait for user to finish labeling (you may want to implement a "Finish" button)
        # For simplicity, we'll use a dummy wait here
        input("Press Enter when you're done labeling...")
        
        return self.apply_labels()

    def apply_labels(self):
        self.df['label'] = ''
        for start, end, label in self.labels:
            mask = (self.df.index >= start) & (self.df.index <= end)
            self.df.loc[mask, 'label'] = label
        return self.df