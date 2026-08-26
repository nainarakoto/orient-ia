from fastapi import APIRouter
from backend.models.chat import ChatRequest, ChatResponse
from agent.orchestrator import agent_orchestrator
import uuid

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("", response_model=ChatResponse)
def chat_endpoint(payload: ChatRequest):
    req_id = str(uuid.uuid4())
    profil_dict = payload.profil.model_dump() if payload.profil else {}
    
    res = agent_orchestrator.execute(
        message=payload.message,
        profil=profil_dict,
        request_id=req_id
    )
    
    return ChatResponse(
        reponse=res["reponse"],
        sources=res["sources"],
        outils_appeles=res["outils_appeles"],
        avertissements=res.get("avertissements", []),
        request_id=req_id
    )