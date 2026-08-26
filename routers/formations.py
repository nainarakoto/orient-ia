from fastapi import APIRouter, HTTPException

from schemas import Formation
from data_store import list_formations, get_formation

router = APIRouter(prefix="/formations", tags=["formations"])


@router.get("", response_model=list[Formation])
def get_all_formations() -> list[Formation]:
    return list_formations()


@router.get("/{formation_id}", response_model=Formation)
def get_one_formation(formation_id: str) -> Formation:
    formation = get_formation(formation_id)
    if formation is None:
        raise HTTPException(status_code=404, detail="Formation introuvable dans le corpus.")
    return formation
