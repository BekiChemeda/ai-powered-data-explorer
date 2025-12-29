from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.file_service import FileService

router = APIRouter()

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    session_name: str = Form(...),
    db: Session = Depends(get_db)
):
    if not file.filename.lower().endswith(('.csv', '.tsv', '.xls', '.xlsx')):
        raise HTTPException(status_code=400, detail="Unsupported file format")
    
    try:
        service = FileService(db)
        session_id = service.save_file(file, session_name)
        
        return {
            "session_id": session_id,
            "filename": file.filename,
            "message": "File uploaded successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
