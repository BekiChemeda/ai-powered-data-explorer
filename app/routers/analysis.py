from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.file_service import FileService
from app.services.dataset import Dataset
from app.services.profiler import Profiler
import os

router = APIRouter()

def get_analysis_context(session_id: str, db: Session):
    file_service = FileService(db)
    record = file_service.get_file_record(session_id)
    if not record:
        raise HTTPException(status_code=404, detail="Session not found")
    
    try:
        # Check if file exists on disk
        if not os.path.exists(record.filepath):
            raise HTTPException(status_code=404, detail=f"File missing from storage: {record.filepath}")

        # Load file
        with open(record.filepath, "rb") as f:
            content = f.read()
        
        dataset = Dataset(content, record.filename)
        profiler = Profiler(dataset.get_dataframe())
        
        return dataset, profiler
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc() # Print to server console
        raise HTTPException(status_code=500, detail=f"Analysis Error: {str(e)}")

@router.get("/analysis/{session_id}/overview")
async def get_overview(session_id: str, db: Session = Depends(get_db)):
    dataset, _ = get_analysis_context(session_id, db)
    return {
        "info": dataset.get_info(),
        "head": dataset.get_head(),
        "shape": dataset.get_shape()
    }

@router.get("/analysis/{session_id}/stats")
async def get_stats(session_id: str, db: Session = Depends(get_db)):
    _, profiler = get_analysis_context(session_id, db)
    return {
        "description": profiler.get_description(),
        "missing_values": profiler.get_missing_values(),
        "correlations": profiler.get_correlations()
    }

@router.get("/analysis/{session_id}/visualizations")
async def get_visualizations(session_id: str, db: Session = Depends(get_db)):
    _, profiler = get_analysis_context(session_id, db)
    return profiler.generate_visualizations()
