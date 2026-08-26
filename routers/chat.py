from fastapi import APIRouter

from schemas import ChatRequest, ChatResponse, Profile
from data_store import get_profile
import agent_orchestrator

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    """
    Interaction libre (§9 "Capacités conversationnelles"). MVP : on route la
    question vers le même orchestrateur que /recommend, avec un profil vide
    si aucun profile_id n'est fourni (l'agent demandera alors une
    clarification, cf. §10 étape 3). À enrichir par M4 pour gérer un vrai
    fil de discussion multi-tours si le temps le permet.
    """
    profile = get_profile(req.profile_id) if req.profile_id else None
    profile = profile or Profile()

    result = agent_orchestrator.run_recommendation(profile, req.message)
    outils = [t for t in ["rechercher_formation", "calculer_score_adequation"]]

    return ChatResponse(
        trace_id=result.trace_id,
        reponse=result.explication.texte_genere,
        outils_appeles=outils,
        refus=result.refus,
    )
