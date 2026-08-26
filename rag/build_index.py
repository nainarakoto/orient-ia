"""
build_index.py
---------------
Script à RELANCER À LA MAIN chaque fois que M1 met à jour le corpus
(nouvelles fiches formation, corrections, etc.) :

    python build_index.py

Ce script :
1. charge toutes les fiches formation depuis data/formations/
2. les découpe en chunks (chunking.py)
3. calcule les embeddings de chaque chunk (embeddings.py)
4. les stocke dans un index ChromaDB persistant (index_chroma/)

Ce n'est PAS un service appelé en direct par l'agent — c'est une étape
de préparation, à lancer hors ligne.
"""

import json
import os
import shutil

import chromadb

from chunking import chunker_toutes_formations
from embeddings import embed_batch

DOSSIER_FORMATIONS = os.path.join(os.path.dirname(__file__), "data", "formations")
DOSSIER_INDEX = os.path.join(os.path.dirname(__file__), "index_chroma")
NOM_COLLECTION = "formations"


def charger_formations(dossier: str) -> list[dict]:
    """Charge tous les fichiers .json d'un dossier en une liste de dicts."""
    formations = []
    if not os.path.isdir(dossier):
        raise FileNotFoundError(
            f"Le dossier {dossier} n'existe pas. "
            f"Vérifie que les fiches de M1 sont bien copiées dans data/formations/."
        )

    fichiers = [f for f in os.listdir(dossier) if f.endswith(".json")]
    if not fichiers:
        raise ValueError(f"Aucun fichier .json trouvé dans {dossier}.")

    for fichier in fichiers:
        chemin = os.path.join(dossier, fichier)
        with open(chemin, "r", encoding="utf-8") as f:
            formations.append(json.load(f))

    return formations


def build_index():
    print("=== Construction de l'index RAG ===\n")

    # 1. Charger les formations
    print(f"1. Chargement des fiches formation depuis {DOSSIER_FORMATIONS}...")
    formations = charger_formations(DOSSIER_FORMATIONS)
    print(f"   → {len(formations)} formation(s) chargée(s).\n")

    # 2. Chunker
    print("2. Découpage en chunks...")
    chunks = chunker_toutes_formations(formations)
    print(f"   → {len(chunks)} chunk(s) généré(s).\n")

    if not chunks:
        raise ValueError("Aucun chunk généré — vérifie le contenu des fiches formation.")

    # 3. Embeddings
    print("3. Calcul des embeddings (peut prendre un moment au premier lancement)...")
    textes = [c["texte"] for c in chunks]
    vecteurs = embed_batch(textes)
    print(f"   → {len(vecteurs)} vecteur(s) calculé(s).\n")

    # 4. Reconstruire l'index (on repart de zéro à chaque fois, plus simple et plus sûr)
    print(f"4. Écriture de l'index dans {DOSSIER_INDEX}...")
    if os.path.isdir(DOSSIER_INDEX):
        shutil.rmtree(DOSSIER_INDEX)

    client = chromadb.PersistentClient(path=DOSSIER_INDEX)
    collection = client.get_or_create_collection(NOM_COLLECTION)

    ids = [f"chunk-{i}" for i in range(len(chunks))]
    metadatas = [
        {
            "formation_id": c["formation_id"] or "",
            "source_id": c["source_id"] or "",
            "section": c["section"],
        }
        for c in chunks
    ]

    collection.add(
        ids=ids,
        embeddings=vecteurs,
        documents=textes,
        metadatas=metadatas,
    )

    print(f"   → Index construit avec succès : {len(ids)} chunks indexés.\n")
    print("=== Terminé. L'index est prêt à être interrogé via rag_service.py ===")


if __name__ == "__main__":
    build_index()