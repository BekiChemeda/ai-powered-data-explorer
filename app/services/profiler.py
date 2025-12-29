import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from app.utils_json import clean_for_json

class Profiler:
    """
    Computes statistics and generates visualizations for a pandas DataFrame.
    """
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def get_description(self) -> dict:
        """
        Returns descriptive statistics including numeric and categorical data.
        """
        # include='all' gets both numeric and categorical summaries
        desc = self.df.describe(include='all').to_dict()
        return clean_for_json(desc)

    def get_missing_values(self) -> dict:
        """Returns count and percentage of missing values per column."""
        missing = self.df.isnull().sum()
        percent = (missing / len(self.df)) * 100
        
        data = {
            "count": missing.to_dict(),
            "percentage": percent.to_dict()
        }
        return clean_for_json(data)

    def get_correlations(self) -> dict:
        """Returns correlation matrix for numeric columns."""
        numeric_df = self.df.select_dtypes(include=[np.number])
        if numeric_df.empty:
            return {}
        corr = numeric_df.corr().to_dict()
        return clean_for_json(corr)

    def generate_visualizations(self) -> dict:
        """
        Generates base64 encoded strings for various plots.
        """
        plots = {}
        
        # Ensure we use a non-GUI backend
        plt.switch_backend('Agg')
        
        numeric_columns = self.df.select_dtypes(include=[np.number]).columns.tolist()
        # Limit to top 5 numeric columns to avoid overwhelming the UI/Backend
        target_numeric = numeric_columns[:5] 
        
        # 1. Histogram (Distribution of numeric cols)
        for col in target_numeric:
            plt.figure(figsize=(6, 4))
            sns.histplot(self.df[col].dropna(), kde=True)
            plt.title(f'Distribution of {col}')
            plots[f'hist_{col}'] = self._plot_to_base64()
            plt.close()

        # 2. Correlation Heatmap
        if len(numeric_columns) > 1:
            plt.figure(figsize=(8, 6))
            corr = self.df[numeric_columns].corr()
            sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
            plt.title('Correlation Heatmap')
            plots['correlation_heatmap'] = self._plot_to_base64()
            plt.close()

        # 3. Bar Chart for Categorical Data (Top 1 categorical col)
        cat_columns = self.df.select_dtypes(include=['object', 'category']).columns.tolist()
        if cat_columns:
            col = cat_columns[0]
            top_counts = self.df[col].value_counts().head(10)
            plt.figure(figsize=(8, 5))
            sns.barplot(x=top_counts.values, y=top_counts.index)
            plt.title(f'Top Categories in {col}')
            plots[f'bar_{col}'] = self._plot_to_base64()
            plt.close()

        return plots

    def _plot_to_base64(self) -> str:
        """Helper to convert current matplotlib plot to base64 string."""
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        return f"data:image/png;base64,{img_str}"
