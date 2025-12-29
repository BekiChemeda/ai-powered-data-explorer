import os
import shutil
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.models import FileRecord
import uuid

STORAGE_DIR = "storage"
os.makedirs(STORAGE_DIR, exist_ok=True)

class FileService:
    def __init__(self, db: Session):
        self.db = db

    def save_file(self, file: UploadFile, session_name: str) -> str:
        """Saves file to disk and creates DB record. Returns session_id."""
        session_id = str(uuid.uuid4())
        file_ext = os.path.splitext(file.filename)[1]
        stored_filename = f"{session_id}{file_ext}"
        filepath = os.path.join(STORAGE_DIR, stored_filename)

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        record = FileRecord(
            session_id=session_id,
            session_name=session_name,
            filename=file.filename,
            filepath=filepath,
            file_type=file_ext
        )
        self.db.add(record)
        self.db.commit()
        return session_id

    def get_file_record(self, session_id: str) -> FileRecord:
        return self.db.query(FileRecord).filter(FileRecord.session_id == session_id).first()

    def get_all_files(self):
        return self.db.query(FileRecord).order_by(FileRecord.upload_time.desc()).all()
