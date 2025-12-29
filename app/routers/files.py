from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.file_service import FileService

router = APIRouter()

@router.get("/files/list")
async def list_files(db: Session = Depends(get_db)):
    service = FileService(db)
    files = service.get_all_files()
    return [{
        "session_id": f.session_id,
        "name": f.session_name,
        "filename": f.filename,
        "date": f.upload_time.isoformat()
    } for f in files]
