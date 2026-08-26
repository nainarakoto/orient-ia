from typing import Dict, List, Any
import logging

class RAGAdapter:
    def rechercher(self, query: str, top_k: int = 3) -> Dict[str, Any]:
        try:
            # Point d'extension pour appeler les fonctions réelles du module rag/
            mock_corpus = [
                {
                    "parcours_id": "info-l3",
                    "source_id": "src-004",
                    "extrait": "La Licence Informatique requiert de solides bases en Mathématiques et algorithmique.",
                    "score": 0.89
                },
                {
                    "parcours_id": "math-l3",
                    "source_id": "src-002",
                    "extrait": "La Licence Mathématiques est axée sur l'analyse, l'algèbre et la modélisation.",
                    "score": 0.78
                }
            ]
            return {"status": "success", "results": mock_corpus[:top_k]}
        except Exception as e:
            logging.error(f"Erreur RAG Adapter: {str(e)}")
            return {"status": "error", "results": [], "message": str(e)}

    def obtenir_fiche(self, parcours_id: str) -> Dict[str, Any]:
        fiches = {
            "info-l3": {
                "nom": "Licence Informatique",
                "matieres": ["Algorithmique", "Mathématiques", "Bases de données"],
                "prerequis": ["Mathématiques", "Informatique"],
                "source_id": "src-004"
            },
            "gestion-m1": {
                "nom": "Master Gestion",
                "matieres": ["Management", "Comptabilité", "Statistiques"],
                "prerequis": ["Gestion de projet"],
                "source_id": "src-010"
            }
        }
        return fiches.get(parcours_id, {})

rag_adapter = RAGAdapter()