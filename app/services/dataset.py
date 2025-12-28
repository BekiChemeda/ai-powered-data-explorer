import pandas as pd
import io

class Dataset:
    """
    Responsible for loading and basic inspection of tabular datasets.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df: pd.DataFrame | None = None


    def load(self) -> pd.DataFrame:
        """
        Loads the dataset into memory based on file extension.
        """
        try:
            if self.file_path.endswith(".csv"):
                self.df = pd.read_csv(self.file_path)

            elif self.file_path.endswith(".tsv"):
                self.df = pd.read_csv(self.file_path, sep="\t")

            elif self.file_path.endswith(".xlsx") or self.file_path.endswith(".xls"):
                self.df = pd.read_excel(self.file_path)

            else:
                raise ValueError("Unsupported file type")

            return self.df

        except Exception as e:
            raise RuntimeError(f"Failed to load dataset: {e}")


    def head(self, n: int = 5) -> list[dict]:
        """
        Returns the first n rows as JSON-serializable records.
        """
        if self.df is None:
            raise RuntimeError("Dataset not loaded")

        return (
            self.df
            .head(n)
            .where(pd.notnull(self.df), None)
            .to_dict(orient="records")
        )

    def describe(self) -> dict:
        """
        Returns descriptive statistics for all columns, handling numeric and non-numeric types.
        """
        numeric = self.df.describe()
        categorical = self.df.describe(include=['object', 'category'])
        return {
            "numeric": numeric.where(pd.notnull(numeric), None).to_dict(),
            "categorical": categorical.where(pd.notnull(categorical), None).to_dict()
        }

    def shape(self):
        """
        Returns shape of the dataset 
        """ 
        if self.df is None:
            raise RuntimeError("Dataset Not loaded")
        return (
            self.df.shape
        )
    def columns(self) -> list[str]:
        """
        Returns list of column names.
        """
        if self.df is None:
            raise RuntimeError("Dataset not loaded")

        return self.df.columns.tolist()
    def info(self) -> str:
        """
        Returns a summary of the DataFrame.
        """
        if self.df is None:
            raise RuntimeError("Dataset not loaded")

        buffer = io.StringIO()
        self.df.info(buf=buffer)
        return buffer.getvalue()