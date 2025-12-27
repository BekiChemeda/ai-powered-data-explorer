from pydantic import BaseModel
from typing import Dict, Any, List, Optional

class ProfileResponse(BaseModel):
    columns: List[str]
    missing_values: Dict[str, int]
    column_types: Dict[str, str]
    unique_counts: Dict[str, int]
    shape: tuple
    basic_stats: Dict[str, Dict[str, Optional[float]]]

class SummaryResponse(BaseModel):
    summary: str

class InfoResponse(BaseModel):
    head: List[Dict[str, Any]]
    describe: Dict[str, Dict[str, Dict[str, Any]]]
    info: Dict[str, Any]
    
class VisualizationRequest(BaseModel):
    column: str
    chart_type: str # histogram, bar

class VisualizationResponse(BaseModel):
    image_base64: str
