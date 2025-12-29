from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class FileRecord(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True)
    session_name = Column(String)
    filename = Column(String)
    filepath = Column(String)
    upload_time = Column(DateTime, default=datetime.utcnow)
    file_type = Column(String)

class AppSetting(Base):
    __tablename__ = "settings"

    key = Column(String, primary_key=True, index=True)
    value = Column(String) # Encrypted value
