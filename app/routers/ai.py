from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.key_manager import KeyManager
from app.schemas.models import AIRequest, AIResponse
from app.services.ai_service import AIService

router = APIRouter()

@router.post("/ai/summarize", response_model=AIResponse)
async def generate_summary(request: AIRequest, db: Session = Depends(get_db)):
    api_key = request.api_key
    
    # Fallback to stored key if not provided
    if not api_key:
        manager = KeyManager(db)
        api_key = manager.get_decrypted_key(request.provider)
        
    if not api_key:
        raise HTTPException(status_code=400, detail="API Key is required within request or stored settings.")
    
    service = AIService(api_key=api_key)
    # Using the new method name generate_insight
    summary = service.generate_insight(request.context_data, request.prompt_type)
    
    return {"summary": summary}
