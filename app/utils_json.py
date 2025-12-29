import pandas as pd
import numpy as np

def clean_for_json(obj):
    """
    Recursively converts numpy types to native Python types 
    and replaces NaNs with None for JSON serialization.
    """
    if isinstance(obj, dict):
        return {k: clean_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_for_json(v) for v in obj]
    elif isinstance(obj, (np.integer, int)):
        return int(obj)
    elif isinstance(obj, (np.floating, float)):
        return None if pd.isna(obj) else float(obj)
    elif isinstance(obj, pd.Timestamp):
        return obj.isoformat() if not pd.isna(obj) else None
    elif pd.isna(obj): # Catch-all for other NaNs/NaTs
        return None
    elif isinstance(obj, np.ndarray):
        return clean_for_json(obj.tolist())
    else:
        return obj
