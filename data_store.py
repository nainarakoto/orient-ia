"""
Data store — MVP en mémoire (chargé depuis data/formations.json au démarrage).

À remplacer par une vraie base (Postgres/SQLite) si le temps le permet — le
plan (§16) prévoit `data/formations/` comme dossier du corpus structuré.
L'important pour la démo est que ces fonctions retournent des données réelles
et traçables (source_id, statut, etc.), pas que le stockage soit sophistiqué.
"""
from __future__ import annotations
import json
from pathlib import Path
from schemas import Formation, Source, Profile

DATA_DIR = Path(__file__).parent / "data"

_formations: dict[str, Formation] = {}
_sources: dict[str, Source] = {}
_profiles: dict[str, Profile] = {}


def load_formations(path: Path | None = None) -> None:
    global _formations, _sources
    path = path or DATA_DIR / "formations.json"
    if not path.exists():
        return
    raw = json.loads(path.read_text(encoding="utf-8"))
    for s in raw.get("sources", []):
        src = Source(**s)
        _sources[src.id] = src
    for f in raw.get("formations", []):
        form = Formation(**f)
        _formations[form.id] = form


def list_formations() -> list[Formation]:
    return list(_formations.values())


def get_formation(formation_id: str) -> Formation | None:
    return _formations.get(formation_id)


def get_source(source_id: str) -> Source | None:
    return _sources.get(source_id)


def save_profile(profile: Profile) -> Profile:
    _profiles[profile.id] = profile
    return profile


def get_profile(profile_id: str) -> Profile | None:
    return _profiles.get(profile_id)
