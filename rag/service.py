def rechercher_documents_rag(requete: str, top_k: int = 3) -> list:
    """Effectue une recherche vectorielle dans le corpus ISPM."""
    # MOCK : À remplacer par ChromaDB / FAISS / BM25
    return [
        {
            "source": "Brochure_ISPM_2026.pdf",
            "contenu": "Le parcours ISAIA (Informatique Statistique Appliquée et IA) exige un bon niveau en mathématiques et algorithmique."
        }
    ]