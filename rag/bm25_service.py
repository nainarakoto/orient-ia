"""
bm25_service.py (v2 — corpus réel ISPM)
-------------------------------------------
Recherche lexicale (mots-clés exacts) en complément de la recherche
vectorielle. Lit les mêmes chunks que ceux indexés dans ChromaDB par
build_index.py — reconstruit en mémoire à chaque lancement (rapide vu
la taille du corpus).
"""

import os
import re

from rank_bm25 import BM25Okapi

try:
    from .chunking import chunker_toutes_formations
except ImportError:
    from chunking import chunker_toutes_formations

FICHIER_CORPUS = os.path.join(os.path.dirname(__file__), "data", "corpus_ispm.md")

_bm25 = None
_chunks = None

# Mots vides français à ignorer : sans ce filtre, des mots très fréquents
# comme "pour", "en", "le" faussent BM25 sur des textes au vocabulaire
# répétitif, et peuvent faire remonter des chunks non pertinents pour
# une question hors sujet qui contient juste un mot-outil courant.
STOPWORDS_FR = {
    "le", "la", "les", "un", "une", "des", "de", "du", "d",
    "en", "et", "ou", "au", "aux", "pour", "par", "sur", "dans",
    "avec", "sans", "ce", "ces", "cette", "cet", "que", "qui",
    "quel", "quelle", "quels", "quelles", "est", "sont", "être",
    "à", "l", "se", "s", "y", "il", "elle", "ils", "elles", "on",
}


def _tokeniser(texte: str) -> list[str]:
    """Tokenisation : minuscules + découpage + suppression des mots vides."""
    texte = texte.lower()
    tokens = re.findall(r"\w+", texte)
    return [t for t in tokens if t not in STOPWORDS_FR]


def build_bm25_index():
    """Reconstruit l'index BM25 en mémoire à partir du corpus réel."""
    global _bm25, _chunks

    fiches = parser_corpus(FICHIER_CORPUS)
    _chunks = chunker_tout_le_corpus(fiches)

    corpus_tokenise = [_tokeniser(c["texte"]) for c in _chunks]
    _bm25 = BM25Okapi(corpus_tokenise)

    return _bm25, _chunks


def _get_bm25():
    global _bm25, _chunks
    if _bm25 is None:
        build_bm25_index()
    return _bm25, _chunks


def rechercher_bm25(query: str, top_k: int = 5) -> list[dict]:
    """
    Recherche lexicale pure. Retourne le même format que rechercher_formation
    (formation_id, extrait, source_id, score), mais le score ici est un
    score BM25 brut (pas borné entre 0 et 1, contrairement au vectoriel).
    """
    bm25, chunks = _get_bm25()

    tokens_query = _tokeniser(query)
    scores = bm25.get_scores(tokens_query)

    resultats = sorted(
        zip(chunks, scores), key=lambda x: x[1], reverse=True
    )[:top_k]

    sortie = []
    for chunk, score in resultats:
        if score <= 0:
            continue  # aucune correspondance lexicale, on ignore
        sortie.append({
            "formation_id": chunk["formation_id"],
            "extrait": chunk["texte"],
            "source_id": chunk["source_id"],
            "score": round(float(score), 3),
        })
    return sortie


if __name__ == "__main__":
    print("=== Test BM25 sur corpus réel : frais de scolarité ===")
    resultats = rechercher_bm25("Quels sont les frais de scolarité en licence 1 ?")
    for r in resultats:
        print(r)