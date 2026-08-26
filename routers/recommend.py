from fastapi import APIRouter

from schemas import RecommendRequest, RecommendResponse
import agent_orchestrator

router = APIRouter(prefix="/recommend", tags=["recommend"])


@router.post("", response_model=RecommendResponse)
def recommend(req: RecommendRequest) -> RecommendResponse:
    """
    Endpoint principal (§17) : profil -> ML -> RAG -> règles -> réponse.
    C'est CET endpoint qui doit être appelé en direct pendant la démo pour
    prouver que le ML et le RAG tournent réellement (cf. §20, question jury #9).
    """
    return agent_orchestrator.run_recommendation(req.profile, req.question)
