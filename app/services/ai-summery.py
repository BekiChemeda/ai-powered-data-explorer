import pandas as pd
from typing import Dict, Any
from app.services.dataset import Dataset

class Profiler:
    """
    Profiles a Dataset object and generates JSON-ready statistics.
    """

    def __init__(self, dataset: Dataset):
        if dataset.df is None:
            raise RuntimeError("Dataset must be loaded before profiling")
        self.df = dataset.df

    def profile(self) -> Dict[str, Any]:
        profile_data = {}
        for col in self.df.columns:
            col_data = self.df[col]
            col_profile = {
                "dtype": str(col_data.dtype),
                "missing_count": int(col_data.isna().sum()),
                "missing_percent": float(col_data.isna().mean() * 100),
                "unique_count": int(col_data.nunique())
            }

            if pd.api.types.is_numeric_dtype(col_data):
                col_profile.update({
                    "mean": float(col_data.mean()) if not col_data.empty else None,
                    "std": float(col_data.std()) if not col_data.empty else None,
                    "min": float(col_data.min()) if not col_data.empty else None,
                    "25%": float(col_data.quantile(0.25)) if not col_data.empty else None,
                    "50%": float(col_data.median()) if not col_data.empty else None,
                    "75%": float(col_data.quantile(0.75)) if not col_data.empty else None,
                    "max": float(col_data.max()) if not col_data.empty else None
                })
            else:
                col_profile.update({
                    "top": col_data.mode().iloc[0] if not col_data.mode().empty else None,
                    "freq": int(col_data.value_counts().iloc[0]) if not col_data.value_counts().empty else None
                })

            profile_data[col] = col_profile

        numeric_cols = self.df.select_dtypes(include=['int64', 'float64']).columns
        if len(numeric_cols) > 1:
            profile_data["correlations"] = self.df[numeric_cols].corr().where(pd.notnull(self.df[numeric_cols].corr()), None).to_dict()

        return profile_data
