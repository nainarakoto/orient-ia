"""
RAG engine — interface entre le backend/agent et le pipeline RAG de M3.

MVP : recherche lexicale naïve (mots-clés) sur les champs texte des
formations chargées en mémoire, pour permettre à l'agent de citer une source
dès aujourd'hui. À REMPLACER par le vrai pipeline (embeddings + vector DB,
§9) en gardant la même signature `search`.
"""
from __future__ import annotations
from schemas import Formation, CitedPassage
from data_store import get_source


def search(query: str, formations: list[Formation], top_k: int = 3) -> list[CitedPassage]:
    """
    Recherche naïve : score = nombre de mots de la requête trouvés dans la
    description/matières/compétences/débouchés de la formation.

    TODO (M3): remplacer par retrieval vectoriel (+ éventuel reranking),
    en conservant la sortie `list[CitedPassage]` (source_id + extrait + score).
    """
    if not query:
        return []
    q_words = {w.lower() for w in query.split() if len(w) > 2}
    scored: list[tuple[float, Formation]] = []

    for f in formations:
        haystack = " ".join(
            [f.description or "", " ".join(f.matieres), " ".join(f.competences), " ".join(f.debouches)]
        ).lower()
        hits = sum(1 for w in q_words if w in haystack)
        if hits > 0:
            scored.append((hits / max(len(q_words), 1), f))

    scored.sort(key=lambda t: t[0], reverse=True)

    passages: list[CitedPassage] = []
    for score, f in scored[:top_k]:
        source_id = f.source_ids[0] if f.source_ids else "inconnue"
        extrait = (f.description or f"{f.mention} — {f.parcours}")[:280]
        passages.append(CitedPassage(source_id=source_id, extrait=extrait, score_recherche=round(score, 3)))
    return passages
