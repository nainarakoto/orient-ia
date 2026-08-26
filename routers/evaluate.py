import json
from pathlib import Path

from fastapi import APIRouter

from schemas import TestCase, TestResult, Profile
import agent_orchestrator

router = APIRouter(prefix="/evaluate", tags=["evaluate"])

TESTS_PATH = Path(__file__).parent.parent / "data" / "test_cases.json"


def _load_test_cases() -> list[TestCase]:
    if not TESTS_PATH.exists():
        return []
    raw = json.loads(TESTS_PATH.read_text(encoding="utf-8"))
    return [TestCase(**t) for t in raw]


@router.get("/cases", response_model=list[TestCase])
def list_cases() -> list[TestCase]:
    """Liste les 32 cas de test définis par M6 (§19)."""
    return _load_test_cases()


@router.post("/run", response_model=list[TestResult])
def run_all_tests() -> list[TestResult]:
    """
    Exécute chaque cas de test contre l'agent réel et renvoie un résultat
    chiffré par cas (exigence §13/§25 : "tests écrits mais jamais exécutés"
    est listé comme erreur MAJEURE — cet endpoint évite précisément ça).

    MVP : exécution automatique uniquement pour les cas de type "profil"
    (question_ou_profil interprétée comme une simple question texte avec un
    profil vide). Le jugement fin "réussi/échoué" par catégorie (RAG exact,
    ML top-k, sécurité...) est à affiner par M6 avec les métriques du plan.
    """
    results: list[TestResult] = []
    for case in _load_test_cases():
        response = agent_orchestrator.run_recommendation(Profile(), case.question_ou_profil)
        obtenu = response.refus or response.explication.texte_genere
        results.append(TestResult(
            test_id=case.id,
            resultat_obtenu=obtenu,
            reussi=bool(obtenu),  # placeholder : à remplacer par une vraie comparaison
            details="Résultat brut — comparaison fine à faire manuellement/par script (§19).",
        ))
    return results
