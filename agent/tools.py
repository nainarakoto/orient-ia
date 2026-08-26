from ml.service import recommander_parcours_ml
from rag.service import rechercher_documents_rag
from knowledge.service import verifier_prerequis_graphe

def tool_analyser_profil_ml(matieres: list, interets: list) -> str:
    """Analyse le profil d'un candidat grâce au modèle ML d'orientation et renvoie un score d'adéquation."""
    res = recommander_parcours_ml(matieres, interets)
    return str(res)

def tool_rechercher_doc_rag(requete: str) -> str:
    """Recherche des informations officielles sur les formations, prérequis, matières et débouchés de l'ISPM dans la base documentaire."""
    res = rechercher_documents_rag(requete)
    return str(res)

def tool_verifier_prerequis(parcours: str, matieres: list) -> str:
    """Vérifie dans le graphe de connaissances si le profil valide les prérequis académiques d'un parcours."""
    res = verifier_prerequis_graphe(parcours, matieres)
    return str(res)