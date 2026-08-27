import asyncio
from ml.service import recommander_parcours_ml, obtenir_liste_metiers_connus
from rag.rag_service import rechercher_formation
from knowledge.service import verifier_prerequis_graphe

_METIERS_CONNUS = obtenir_liste_metiers_connus()
_METIERS_TEXTE = ", ".join(_METIERS_CONNUS)


async def tool_analyser_profil_ml(
    age: int,
    sexe: str,
    serie: str,
    moyenne_generale: float,
    preferences_env: str,
    objectif_professionnel: str,
    matieres_fortes: list,
    matieres_faibles: list,
    centres_interet: list,
    competences: list,
) -> str:
    """Analyse le profil complet d'un candidat (âge, sexe, série du bac, moyenne générale, préférence d'environnement de travail, objectif professionnel, matières fortes, matières faibles, centres d'intérêt, compétences) grâce au modèle ML d'orientation, et renvoie le classement des filières les plus adaptées avec leurs scores."""
    res = await asyncio.to_thread(
        recommander_parcours_ml,
        age, sexe, serie, moyenne_generale, preferences_env, objectif_professionnel,
        matieres_fortes, matieres_faibles, centres_interet, competences,
    )
    return str(res)


# La docstring est complétée dynamiquement après la définition, car une
# f-string ne peut pas servir directement de docstring en Python (elle
# n'est pas reconnue comme une chaîne littérale constante par l'interpréteur).
tool_analyser_profil_ml.__doc__ += (
    "\n\nIMPORTANT pour le paramètre objectif_professionnel : reformule toujours "
    "l'objectif exprimé librement par l'utilisateur vers le métier le plus proche "
    f"dans cette liste connue du modèle : {_METIERS_TEXTE}. "
    "Si l'utilisateur est vague (ex: \"travailler dans la tech\"), choisis le métier "
    "de cette liste qui correspond le mieux à son intention."
)


async def tool_rechercher_doc_rag(requete: str) -> str:
    """Recherche des informations officielles sur les formations, prérequis, matières et débouchés de l'ISPM dans la base documentaire."""
    res = await asyncio.to_thread(rechercher_formation, requete)
    return str(res)


def tool_verifier_prerequis(parcours: str, matieres: list) -> str:
    """Vérifie dans le graphe de connaissances si le profil valide les prérequis académiques d'un parcours."""
    res = verifier_prerequis_graphe(parcours, matieres)
    return str(res)