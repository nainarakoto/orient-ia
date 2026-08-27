"""
build_index.py (v2 — corpus réel ISPM)
------------------------------------------
Script à RELANCER À LA MAIN chaque fois que M1 met à jour le corpus
(data/corpus_ispm.md) :

    python build_index.py

Ce script :
1. parse le fichier corpus (parser.py)
2. découpe chaque fiche en chunks (chunking.py)
3. calcule les embeddings de chaque chunk (embeddings.py)
4. les stocke dans un index ChromaDB persistant (index_chroma/)
"""

import os
import shutil

import chromadb

from parser import parser_corpus
from chunking import chunker_tout_le_corpus
from embeddings import embed_batch

FICHIER_CORPUS = os.path.join(os.path.dirname(__file__), "data", "corpus_ispm.md")
DOSSIER_INDEX = os.path.join(os.path.dirname(__file__), "index_chroma")
NOM_COLLECTION = "ispm_corpus"


def build_index():
    print("=== Construction de l'index RAG (corpus réel ISPM) ===\n")

    # 1. Parser le corpus
    print(f"1. Lecture et parsing du corpus depuis {FICHIER_CORPUS}...")
    if not os.path.isfile(FICHIER_CORPUS):
        raise FileNotFoundError(
            f"Fichier corpus introuvable : {FICHIER_CORPUS}. "
            f"Place le fichier livré par M1 à cet emplacement exact."
        )
    fiches = parser_corpus(FICHIER_CORPUS)
    print(f"   → {len(fiches)} fiche(s) trouvée(s).\n")

    # 2. Chunker
    print("2. Découpage en chunks...")
    chunks = chunker_tout_le_corpus(fiches)
    print(f"   → {len(chunks)} chunk(s) généré(s).\n")

    if not chunks:
        raise ValueError("Aucun chunk généré — vérifie le format du fichier corpus.")

    # 3. Embeddings
    print("3. Calcul des embeddings (peut prendre un moment au premier lancement)...")
    textes = [c["texte"] for c in chunks]
    vecteurs = embed_batch(textes)
    print(f"   → {len(vecteurs)} vecteur(s) calculé(s).\n")

    # 4. Reconstruire l'index (on repart de zéro à chaque fois)
    print(f"4. Écriture de l'index dans {DOSSIER_INDEX}...")
    if os.path.isdir(DOSSIER_INDEX):
        shutil.rmtree(DOSSIER_INDEX)

    client = chromadb.PersistentClient(path=DOSSIER_INDEX)
    collection = client.get_or_create_collection(NOM_COLLECTION)

    ids = [f"chunk-{i}" for i in range(len(chunks))]
    metadatas = []
    for c in chunks:
        metadatas.append({
            "formation_id": c["formation_id"] or "",
            "type": c["type"] or "",
            "parcours": c["parcours"] or "",
            "section": c["section"] or "",
            "source_id": c["source_id"] or "",
            # ChromaDB n'accepte pas les listes en métadonnées : on les
            # joint en une chaîne, séparée par des virgules.
            "sources_ids": ",".join(c["sources_ids"]) if c["sources_ids"] else "",
        })

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