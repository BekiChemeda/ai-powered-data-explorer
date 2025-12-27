import pandas as pd
import io

class Dataset:
    """
    Class responsible for loading and managing the dataset.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = None

    def load(self) -> pd.DataFrame:
        """
        Loads the dataset from the file path based on extension.
        """
        try:
            if self.file_path.endswith(".csv"):
                self.df = pd.read_csv(self.file_path)
            elif self.file_path.endswith(".tsv"):
                self.df = pd.read_csv(self.file_path, sep="\t")
            elif self.file_path.endswith(".xlsx") or self.file_path.endswith(".xls"):
                self.df = pd.read_excel(self.file_path)
            else:
                raise ValueError("Unsupported file type. Please upload CSV, TSV, or Excel.")
            return self.df
        except Exception as e:
            raise RuntimeError(f"Failed to load dataset: {e}")
    
    def head(self, n=5) -> dict:
        """Returns the first n rows as a dictionary."""
        if self.df is not None:
            # Replace NaN with None for JSON compatibility
            return self.df.head(n).where(pd.notnull(self.df), None).to_dict(orient='records')
        return {}
    
    def describe(self) -> dict:
        """Returns descriptive statistics."""
        if self.df is not None:
            return self.df.describe(include='all').where(pd.notnull(self.df), None).to_dict()
        return {}
    
    def info(self) -> str:
        """Returns the info summary as a string."""
        if self.df is not None:
            buffer = io.StringIO()
            self.df.info(buf=buffer)
            return buffer.getvalue()
        return ""
