from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.key_manager import KeyManager
from pydantic import BaseModel

router = APIRouter()

class KeyPayload(BaseModel):
    provider: str
    key: str

@router.post("/settings/key")
async def save_api_key(payload: KeyPayload, db: Session = Depends(get_db)):
    manager = KeyManager(db)
    try:
        manager.save_key(payload.provider, payload.key)
        return {"message": "API Key saved and validated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Error")

@router.get("/settings/has_key/{provider}")
async def check_key(provider: str, db: Session = Depends(get_db)):
    manager = KeyManager(db)
    key = manager.get_decrypted_key(provider)
    return {"exists": key is not None}
