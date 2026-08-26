"""
Tool registry — ORIENT'IA (§11 du plan)

Chaque fonction ici est un OUTIL RÉEL au sens du sujet : une opération
technique identifiable, appelée avec une entrée précise et retournant une
sortie structurée — pas une simple instruction glissée dans un prompt.

Outils implémentés (minimum imposé : 3) :
  1. rechercher_formation      -> RAG
  2. verifier_prerequis        -> règles
  3. comparer_parcours         -> règles + RAG
  4. calculer_score_adequation -> ML
  5. identifier_debouches      -> lecture structurée
  6. expliquer_recommandation  -> assemblage final

Chaque appel est journalisé par l'appelant (agent_orchestrator) sous forme
de ToolCallTrace pour l'observabilité (§20).
"""
from __future__ import annotations
from schemas import Profile, Formation, ScoreParcours, CitedPassage
from data_store import list_formations, get_formation
import ml_service
import rag_engine


def rechercher_formation(query: str) -> list[CitedPassage]:
    """Outil RAG : recherche des passages pertinents dans le corpus (§9)."""
    return rag_engine.search(query, list_formations())


def verifier_prerequis(profile: Profile, parcours_id: str) -> dict:
    """Outil règles : vérifie si un profil remplit les prérequis d'un parcours."""
    formation = get_formation(parcours_id)
    if formation is None:
        return {"trouve": False, "ok": False, "manquants": []}
    manquants = [
        p for p in formation.prerequis
        if p.lower() not in {c.lower() for c in profile.competences_declarees}
    ]
    return {"trouve": True, "ok": len(manquants) == 0, "manquants": manquants}


def comparer_parcours(parcours_id_1: str, parcours_id_2: str) -> dict:
    """Outil : compare deux parcours sur matières/compétences/débouchés, avec sources."""
    f1, f2 = get_formation(parcours_id_1), get_formation(parcours_id_2)
    if f1 is None or f2 is None:
        return {"erreur": "Un ou plusieurs parcours introuvables dans le corpus."}
    return {
        "parcours_1": {
            "id": f1.id, "mention": f1.mention, "parcours": f1.parcours,
            "matieres": f1.matieres, "competences": f1.competences,
            "debouches": f1.debouches, "source_ids": f1.source_ids,
        },
        "parcours_2": {
            "id": f2.id, "mention": f2.mention, "parcours": f2.parcours,
            "matieres": f2.matieres, "competences": f2.competences,
            "debouches": f2.debouches, "source_ids": f2.source_ids,
        },
    }


def calculer_score_adequation(profile: Profile) -> list[ScoreParcours]:
    """Outil ML : score d'adéquation profil <-> chaque parcours (§7)."""
    return ml_service.score_parcours(profile, list_formations())


def identifier_debouches(parcours_id: str) -> dict:
    """Outil : renvoie les débouchés d'un parcours et sa/ses source(s)."""
    formation = get_formation(parcours_id)
    if formation is None:
        return {"trouve": False, "debouches": [], "source_ids": []}
    return {"trouve": True, "debouches": formation.debouches, "source_ids": formation.source_ids}


def expliquer_recommandation(
    scores: list[ScoreParcours],
    passages: list[CitedPassage],
    regles_appliquees: list[str],
) -> str:
    """
    Outil d'assemblage final : construit un texte distinguant explicitement
    ce qui vient du ML, des documents et des règles (exigence §8/§12).
    """
    lignes = []
    if scores:
        top = scores[0]
        lignes.append(
            f"D'après le modèle d'adéquation (ML), le parcours '{top.parcours_id}' "
            f"obtient le score le plus élevé ({top.score_ml})."
        )
        if not top.prerequis_ok:
            lignes.append(
                f"Cependant, les prérequis suivants ne sont pas remplis d'après nos règles : "
                f"{', '.join(top.prerequis_manquants)}."
            )
    if passages:
        lignes.append(
            "Éléments issus des documents de l'ISPM : "
            + " | ".join(f"[{p.source_id}] {p.extrait[:120]}" for p in passages)
        )
    if regles_appliquees:
        lignes.append("Règles appliquées : " + "; ".join(regles_appliquees))
    if not lignes:
        lignes.append(
            "Je n'ai pas assez d'informations vérifiées pour formuler une "
            "recommandation fiable. Pouvez-vous préciser vos matières préférées "
            "ou vos résultats scolaires ?"
        )
    return " ".join(lignes)
