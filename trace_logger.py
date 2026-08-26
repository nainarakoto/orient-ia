"""
Trace logger — ORIENT'IA (§15, §20 du plan)

Enregistre chaque requête traitée par l'agent : question, profil, passages
récupérés, outils appelés, réponse finale, latence, erreurs/refus.

MVP : écriture JSON-lines sur disque (facile à afficher en démo, cf. §20 :
"afficher en direct la trace d'une requête pendant la démo"). À remplacer /
compléter par un vrai backend d'observabilité si le temps le permet (P2/P3).
"""
from __future__ import annotations
import json
import threading
from pathlib import Path

from schemas import Trace

LOG_PATH = Path(__file__).parent / "observability" / "traces.jsonl"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

_lock = threading.Lock()


def log_trace(trace: Trace) -> None:
    """Ajoute une trace au fichier de logs (append-only, thread-safe)."""
    line = trace.model_dump_json()
    with _lock:
        with LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(line + "\n")


def read_traces(limit: int = 50) -> list[dict]:
    """Relit les N dernières traces — utile pour un endpoint /traces de démo."""
    if not LOG_PATH.exists():
        return []
    with _lock:
        lines = LOG_PATH.read_text(encoding="utf-8").strip().splitlines()
    return [json.loads(line) for line in lines[-limit:]]
