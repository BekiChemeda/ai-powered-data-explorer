from pydantic import BaseModel
from typing import Dict, List, Optional, Any

class DatasetInfoResponse(BaseModel):
    filename: str
    rows: int
    columns: int
    column_names: List[str]
    dtypes: Dict[str, str]

class AnalysisResponse(BaseModel):
    head: List[Dict[str, Any]]
    description: Dict[str, Any]
    missing_values: Dict[str, Any]
    correlations: Dict[str, Any]

class AIRequest(BaseModel):
    api_key: Optional[str] = None # Optional now
    provider: str = "gemini"
    prompt_type: str = "overview"  # overview, stats, missing, visualization
    context_data: Dict[str, Any]

class AIResponse(BaseModel):
    summary: str
