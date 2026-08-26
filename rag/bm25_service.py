"""
bm25_service.py
-----------------
Recherche lexicale (mots-clés exacts) en complément de la recherche
vectorielle. Utile pour les cas où le vectoriel rate un mot clé précis
(ex: "matières", un sigle, un nom exact de parcours) noyé dans des
chunks très similaires entre eux.

Principe : BM25 est un algorithme classique de recherche par mots-clés
(comme un moteur de recherche à l'ancienne), qui score les documents
selon la fréquence des mots de la requête qu'ils contiennent.

Ce module lit les MÊMES chunks que ceux indexés par build_index.py,
donc il doit être reconstruit (build_bm25_index) chaque fois que
build_index.py est relancé, pour rester synchronisé.
"""

import json
import os

from rank_bm25 import BM25Okapi

from chunking import chunker_toutes_formations

DOSSIER_FORMATIONS = os.path.join(os.path.dirname(__file__), "data", "formations")
FICHIER_CHUNKS_CACHE = os.path.join(os.path.dirname(__file__), "chunks", "chunks.jsonl")

_bm25 = None
_chunks = None

# Mots vides français à ignorer : sans ce filtre, des mots très fréquents
# comme "pour", "en", "le" faussent BM25 sur des chunks au vocabulaire
# répétitif (ex: "Prérequis POUR intégrer...", "Débouchés POUR..."),
# et peuvent faire remonter des chunks non pertinents pour une question
# totalement hors sujet qui contient juste "pour" ou "en".
STOPWORDS_FR = {
    "le", "la", "les", "un", "une", "des", "de", "du", "d",
    "en", "et", "ou", "au", "aux", "pour", "par", "sur", "dans",
    "avec", "sans", "ce", "ces", "cette", "cet", "que", "qui",
    "quel", "quelle", "quels", "quelles", "est", "sont", "être",
    "à", "l", "se", "s", "y", "il", "elle", "ils", "elles", "on",
}


def _tokeniser(texte: str) -> list[str]:
    """Tokenisation : minuscules + découpage + suppression des mots vides."""
    import re
    texte = texte.lower()
    tokens = re.findall(r"\w+", texte)
    return [t for t in tokens if t not in STOPWORDS_FR]


def charger_formations_locales() -> list[dict]:
    formations = []
    for fichier in os.listdir(DOSSIER_FORMATIONS):
        if fichier.endswith(".json"):
            with open(os.path.join(DOSSIER_FORMATIONS, fichier), "r", encoding="utf-8") as f:
                formations.append(json.load(f))
    return formations


def build_bm25_index():
    """
    Reconstruit l'index BM25 en mémoire à partir des chunks générés par
    chunking.py (les mêmes que ceux indexés dans ChromaDB par build_index.py).
    Sauvegarde aussi les chunks dans un fichier .jsonl pour inspection/debug.
    """
    global _bm25, _chunks

    formations = charger_formations_locales()
    _chunks = chunker_toutes_formations(formations)

    corpus_tokenise = [_tokeniser(c["texte"]) for c in _chunks]
    _bm25 = BM25Okapi(corpus_tokenise)

    # Sauvegarde optionnelle pour inspection
    os.makedirs(os.path.dirname(FICHIER_CHUNKS_CACHE), exist_ok=True)
    with open(FICHIER_CHUNKS_CACHE, "w", encoding="utf-8") as f:
        for c in _chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

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
    print("=== Test BM25 : question sur les matières ===")
    resultats = rechercher_bm25("Quelles matières en licence informatique ?")
    for r in resultats:
        print(r)
    print("\nOK si le chunk 'Matières enseignées en Licence Informatique...' apparaît en premier.")