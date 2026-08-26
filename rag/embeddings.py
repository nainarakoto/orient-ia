"""
embeddings.py
-------------
Isole tout ce qui concerne le modèle d'embeddings.
Si on doit changer de modèle plus tard (lenteur, quota, etc.),
c'est le SEUL fichier à modifier — rien d'autre dans le pipeline ne bouge.

Modèle choisi : sentence-transformers, modèle multilingue léger.
- Tourne en local (pas d'appel API externe, pas de quota, pas de coût).
- Gère bien le français.
"""

from sentence_transformers import SentenceTransformer

_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
_model = None  # chargé une seule fois (lazy loading)


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        print(f"[embeddings] Chargement du modèle '{_MODEL_NAME}' (premier appel, peut prendre du temps)...")
        _model = SentenceTransformer(_MODEL_NAME)
    return _model


def embed_texte(texte: str) -> list[float]:
    """Retourne le vecteur d'embedding d'un seul texte."""
    model = _get_model()
    vecteur = model.encode(texte, normalize_embeddings=True)
    return vecteur.tolist()


def embed_batch(textes: list[str]) -> list[list[float]]:
    """Version batch : plus rapide pour indexer plusieurs chunks d'un coup."""
    model = _get_model()
    vecteurs = model.encode(textes, normalize_embeddings=True, show_progress_bar=True)
    return vecteurs.tolist()


if __name__ == "__main__":
    # Test rapide : lance `python embeddings.py` pour vérifier que ça marche
    texte_test = "Formation en informatique orientée data et intelligence artificielle"
    vecteur = embed_texte(texte_test)
    print(f"Texte testé : {texte_test}")
    print(f"Taille du vecteur obtenu : {len(vecteur)}")
    print(f"5 premières valeurs : {vecteur[:5]}")
    print("OK — le module embeddings fonctionne.")