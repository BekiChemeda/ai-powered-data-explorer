import pandas as pd
import io


class Dataset:
    """
    Supports CSV, TSV, and Excel files.
    """

    def __init__(self, filename: str, file_bytes: bytes):
        self.filename = filename
        self.file_bytes = file_bytes
        self.df: pd.DataFrame | None = None

    def _ensure_loaded(self):
        if self.df is None:
            raise RuntimeError("Dataset not loaded. Call load() first.")

    def load(self) -> pd.DataFrame:
        """
        Load dataset from in-memory bytes based on file extension.
        """
        try:
            buffer = io.BytesIO(self.file_bytes)

            if self.filename.endswith(".csv"):
                self.df = pd.read_csv(buffer)

            elif self.filename.endswith(".tsv"):
                self.df = pd.read_csv(buffer, sep="\t")

            elif self.filename.endswith((".xls", ".xlsx")):
                self.df = pd.read_excel(buffer)

            else:
                raise ValueError("Unsupported file type")

            return self.df

        except Exception as e:
            raise RuntimeError(f"Failed to load dataset: {e}")

    def head(self, n: int = 5) -> list[dict]:
        self._ensure_loaded()
        return (
            self.df.head(n)
            .where(pd.notnull(self.df), None)
            .to_dict(orient="records")
        )

    def describe(self) -> dict:
        self._ensure_loaded()

        numeric = self.df.select_dtypes(include="number").describe()
        categorical = self.df.select_dtypes(exclude="number").describe()

        return {
            "numeric": numeric.where(pd.notnull(numeric), None).to_dict(),
            "categorical": categorical.where(pd.notnull(categorical), None).to_dict()
        }

    def info(self) -> dict:
        self._ensure_loaded()

        return {
            "rows": int(self.df.shape[0]),
            "columns": int(self.df.shape[1]),
            "column_names": list(self.df.columns),
            "dtypes": self.df.dtypes.astype(str).to_dict(),
            "null_counts": self.df.isnull().sum().to_dict(),
            "memory_usage_bytes": int(
                self.df.memory_usage(deep=True).sum()
            ),
        }

    def summary(self, head_rows: int = 5) -> dict:
        return {
            "head": self.head(head_rows),
            "describe": self.describe(),
            "info": self.info()
        }
