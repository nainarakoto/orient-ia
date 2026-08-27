import os
import pandas as pd
import numpy as np
import joblib
from rag.embeddings import embed_texte  # réutilise le même modèle d'embeddings que le RAG

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(PROJECT_ROOT, "ml", "models", "best_model.joblib")
FORMATIONS_PATH = os.path.join(PROJECT_ROOT, "data", "synthetic", "formations_etablissement.csv")

_model = None
_formations = None
_metiers_connus = None
_metiers_embeddings = None


def _charger_modele():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model


def _charger_formations():
    global _formations
    if _formations is None:
        df = pd.read_csv(FORMATIONS_PATH)
        df.columns = df.columns.str.strip()
        _formations = df
    return _formations


def obtenir_liste_metiers_connus() -> list:
    """Retourne la liste triée des métiers connus du modèle (utilisée pour guider Gemini dans le choix d'objectif_professionnel)."""
    formations = _charger_formations()
    tous_metiers = set()
    for valeur in formations["metiers_accessibles"].dropna():
        for metier in valeur.split(";"):
            metier = metier.strip()
            if metier:
                tous_metiers.add(metier)
    return sorted(tous_metiers)


def obtenir_schema_ml() -> dict:
    """
    Retourne les catégories exactes attendues par le pipeline scikit-learn
    pour les champs catégoriels du profil utilisateur (série du bac,
    préférence d'environnement de travail, objectifs professionnels connus).

    Extraites directement depuis le OneHotEncoder entraîné (et depuis les
    formations connues pour les métiers), afin que le frontend construise
    ses menus déroulants toujours parfaitement synchronisés avec le modèle,
    même si celui-ci est ré-entraîné avec des catégories différentes plus tard.
    """
    model = _charger_modele()
    preprocessing = model.named_steps["preprocessing"]

    series = []
    preferences_env = []
    for nom_transformer, transfo, colonnes in preprocessing.transformers_:
        if nom_transformer != "categorical":
            continue
        encoder = transfo.named_steps["encoder"]
        colonnes = list(colonnes)
        if "serie" in colonnes:
            series = list(encoder.categories_[colonnes.index("serie")])
        if "preferences_env" in colonnes:
            preferences_env = list(encoder.categories_[colonnes.index("preferences_env")])

    return {
        "series": series,
        "preferences_env": preferences_env,
        "objectifs_professionnels": obtenir_liste_metiers_connus(),
    }


def _charger_metiers_connus():
    """
    Précalcule les embeddings des métiers connus, une seule fois (mis en
    cache en mémoire). Utilisé uniquement comme filet de sécurité quand
    Gemini n'a pas choisi une valeur exacte de la liste.
    """
    global _metiers_connus, _metiers_embeddings
    if _metiers_connus is None:
        _metiers_connus = obtenir_liste_metiers_connus()
        _metiers_embeddings = np.array([embed_texte(m) for m in _metiers_connus])
    return _metiers_connus, _metiers_embeddings


def _cosine_similarite(vecteur: np.ndarray, matrice: np.ndarray) -> np.ndarray:
    vecteur_norm = vecteur / (np.linalg.norm(vecteur) + 1e-10)
    matrice_norm = matrice / (np.linalg.norm(matrice, axis=1, keepdims=True) + 1e-10)
    return matrice_norm @ vecteur_norm


def normaliser_objectif_professionnel(objectif: str) -> str:
    """
    Si Gemini a déjà fourni un métier exact de la liste connue, on le garde
    tel quel (cas normal attendu). Sinon, filet de sécurité par similarité
    d'embeddings (cas limite, moins fiable).
    """
    metiers_connus, embeddings_connus = _charger_metiers_connus()

    if objectif in metiers_connus:
        return objectif

    vecteur_objectif = embed_texte(objectif)
    similarites = _cosine_similarite(vecteur_objectif, embeddings_connus)
    index_meilleur = int(np.argmax(similarites))
    return metiers_connus[index_meilleur]


def recommander_parcours_ml(
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
    top_k: int = 5,
) -> list:
    model = _charger_modele()
    formations = _charger_formations()

    objectif_normalise = normaliser_objectif_professionnel(objectif_professionnel)

    nombre_competences = len(competences)
    nombre_matieres_fortes = len(matieres_fortes)
    nombre_matieres_faibles = len(matieres_faibles)
    nombre_centres_interet = len(centres_interet)

    lignes = []
    for _, filiere in formations.iterrows():
        lignes.append({
            "parcours_id": filiere["parcours_id"],
            "age": age,
            "sexe": sexe,
            "serie": serie,
            "moyenne_generale": moyenne_generale,
            "preferences_env": preferences_env,
            "objectif_professionnel": objectif_normalise,
            "filiere_nom": filiere["nom_complet"],
            "filiere_parcours_id": filiere["parcours_id"],
            "filiere_parcours_nom": filiere["parcours_nom"],
            "filiere_secteur": filiere["secteur_professionnel"],
            "nombre_competences": nombre_competences,
            "nombre_matieres_fortes": nombre_matieres_fortes,
            "nombre_matieres_faibles": nombre_matieres_faibles,
            "nombre_centres_interet": nombre_centres_interet,
            "_filiere_code": filiere["code_filiere"],
        })

    df_candidats = pd.DataFrame(lignes)

    if hasattr(model, "feature_names_in_"):
        features_attendues = list(model.feature_names_in_)
    else:
        features_attendues = [c for c in df_candidats.columns if not c.startswith("_")]

    X = df_candidats[features_attendues]
    probabilites = model.predict_proba(X)[:, 1]

    df_candidats["score_recommandation"] = probabilites
    df_candidats = df_candidats.sort_values("score_recommandation", ascending=False)

    resultats = []
    for _, row in df_candidats.head(top_k).iterrows():
        resultats.append({
            "filiere_code": row["_filiere_code"],
            "filiere_nom": row["filiere_nom"],
            "score": round(float(row["score_recommandation"]), 4),
        })
    return resultats