import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import pandas as pd
from app.services.dataset import Dataset

class Visualizer:
    """
    Class responsible for generating visualizations.
    """
    def __init__(self, dataset: Dataset):
        self.df = dataset.df

    def generate_histogram(self, column: str) -> str:
        """Generates a histogram for a numeric column and returns base64 string."""
        if column not in self.df.columns:
            raise ValueError(f"Column {column} not found")
        
        plt.figure(figsize=(10, 6))
        sns.histplot(self.df[column], kde=True)
        plt.title(f"Histogram of {column}")
        return self._to_base64()

    def generate_bar_chart(self, column: str) -> str:
        """Generates a bar chart for a categorical column and returns base64 string."""
        if column not in self.df.columns:
            raise ValueError(f"Column {column} not found")
        
        plt.figure(figsize=(10, 6))
        self.df[column].value_counts().plot(kind='bar')
        plt.title(f"Bar Chart of {column}")
        plt.xlabel(column)
        plt.ylabel("Count")
        return self._to_base64()

    def generate_correlation_heatmap(self) -> str:
        """Generates a correlation heatmap for numeric columns and returns base64 string."""
        numeric_df = self.df.select_dtypes(include=['number'])
        if numeric_df.empty:
            raise ValueError("No numeric columns for correlation heatmap")

        plt.figure(figsize=(10, 8))
        sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
        plt.title("Correlation Heatmap")
        return self._to_base64()

    def _to_base64(self) -> str:
        """Converts the current plot to a base64 string."""
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        plt.close()
        
        graphic = base64.b64encode(image_png)
        return graphic.decode('utf-8')
