import pandas as pd
import io
import os
from app.utils_json import clean_for_json

class Dataset:
    """
    Handles loading and basic operations on datasets.
    Supports CSV, TSV, Excel.
    """
    def __init__(self, file_content: bytes, filename: str):
        self.filename = filename
        self.df = self._load_data(file_content, filename)

    def _load_data(self, content: bytes, filename: str) -> pd.DataFrame:
        """Loads data into a pandas DataFrame based on file extension."""
        filename = filename.lower()
        try:
            if filename.endswith('.csv'):
                return pd.read_csv(io.BytesIO(content))
            elif filename.endswith('.tsv'):
                return pd.read_csv(io.BytesIO(content), sep='\t')
            elif filename.endswith(('.xls', '.xlsx')):
                return pd.read_excel(io.BytesIO(content))
            # Basic basic SQL support if uploaded as .db (sqlite)
            # This is risky/complex for web upload generally without a specialized UI, 
            # so we'll stick to file-based formats for this implementation as per standard user flows.
            else:
                raise ValueError(f"Unsupported file format: {filename}")
        except Exception as e:
            raise ValueError(f"Error loading file: {str(e)}")

    def get_head(self, n: int = 5) -> list[dict]:
        """Returns the first n rows as a list of dictionaries (JSON-ready)."""
        data = self.df.head(n).to_dict(orient='records')
        return clean_for_json(data)

    def get_info(self) -> dict:
        """Returns dataset metadata."""
        buffer = io.StringIO()
        self.df.info(buf=buffer)
        info_str = buffer.getvalue()
        
        info_data = {
            "rows": self.df.shape[0],
            "columns": self.df.shape[1],
            "column_names": self.df.columns.tolist(),
            "memory_usage": self.df.memory_usage(deep=True).sum(),
            "dtypes": self.df.dtypes.astype(str).to_dict(),
            "raw_info": info_str # For display if needed
        }
        return clean_for_json(info_data)

    def get_columns(self) -> list:
        return self.df.columns.tolist()
        
    def get_shape(self) -> tuple:
        return self.df.shape

    def get_dataframe(self) -> pd.DataFrame:
        return self.df