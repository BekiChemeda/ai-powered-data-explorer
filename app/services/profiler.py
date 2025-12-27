import pandas as pd
import numpy as np
from pandas.api.types import is_numeric_dtype, is_datetime64_any_dtype
from app.services.dataset import Dataset

class Profiler:
    """
    Class responsible for profiling the dataset (missing values, types, stats).
    """
    def __init__(self, dataset: Dataset):
        self.df = dataset.df
    
    def get_profile(self) -> dict:
        """Aggregates all profiling information."""
        if self.df is None:
            return {}
        
        return {
            "columns": list(self.df.columns),
            "missing_values": self.missing_values(),
            "column_types": self.column_types(),
            "unique_counts": self.unique_counts(),
            "shape": self.df.shape,
            "basic_stats": self.basic_stats()
        }

    def missing_values(self) -> dict:
        """Computes missing values per column."""
        return self.df.isnull().sum().to_dict()
    
    def column_types(self) -> dict:
        """Determines the data type of each column."""
        types = {}
        for col in self.df.columns:
            if is_numeric_dtype(self.df[col]):
                types[col] = 'numeric'
            elif is_datetime64_any_dtype(self.df[col]):
                types[col] = 'datetime'
            else:
                types[col] = 'categorical'
        return types

    def unique_counts(self) -> dict:
        """Counts unique values for each column."""
        return self.df.nunique().to_dict()

    def basic_stats(self) -> dict:
        """Computes basic statistics for numeric columns."""
        stats = {}
        for col in self.df.columns:
            if is_numeric_dtype(self.df[col]):
                stats[col] = {
                    "mean": float(self.df[col].mean()) if not pd.isna(self.df[col].mean()) else None,
                    "median": float(self.df[col].median()) if not pd.isna(self.df[col].median()) else None,
                    "std": float(self.df[col].std()) if not pd.isna(self.df[col].std()) else None,
                    "min": float(self.df[col].min()) if not pd.isna(self.df[col].min()) else None,
                    "max": float(self.df[col].max()) if not pd.isna(self.df[col].max()) else None
                }
        return stats
