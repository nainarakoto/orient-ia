from fastapi import APIRouter

from trace_logger import read_traces

router = APIRouter(prefix="/traces", tags=["traces"])


@router.get("")
def get_traces(limit: int = 20) -> list[dict]:
    """
    Endpoint bonus mais très utile en démo (§20/§23) : affiche les dernières
    traces pour prouver en direct que ML/RAG/outils sont réellement appelés.
    """
    return read_traces(limit=limit)
