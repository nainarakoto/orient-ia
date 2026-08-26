from fastapi import APIRouter
import uuid

from schemas import Profile, ProfileUpdateRequest
from data_store import save_profile, get_profile

router = APIRouter(prefix="/profile", tags=["profile"])


@router.post("", response_model=Profile)
def create_or_update_profile(req: ProfileUpdateRequest) -> Profile:
    """Crée un profil (si profile_id absent) ou met à jour un profil existant."""
    existing = get_profile(req.profile_id) if req.profile_id else None
    profile = existing or Profile(id=req.profile_id or str(uuid.uuid4()))

    for field in (
        "matieres_preferees", "resultats", "competences_declarees",
        "interets", "projets", "preferences_professionnelles",
        "environnement_travail_recherche",
    ):
        value = getattr(req, field)
        if value is not None:
            setattr(profile, field, value)

    return save_profile(profile)


@router.get("/{profile_id}", response_model=Profile | None)
def read_profile(profile_id: str) -> Profile | None:
    return get_profile(profile_id)
