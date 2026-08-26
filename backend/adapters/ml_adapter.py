from typing import Dict, List, Any
import logging

class MLAdapter:
    def classer_parcours(self, profil: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # ⚠️ À REMPLACER PLUS TARD : Supprime ce dictionnaire "mock" et appelle la vraie fonction du dossier ml/
            return {
                "status": "success",
                "data": [
                    {"parcours_id": "info-l3", "score": 0.91, "nom": "Licence Informatique"},
                    {"parcours_id": "math-l3", "score": 0.82, "nom": "Licence Mathématiques"},
                    {"parcours_id": "gestion-m1", "score": 0.65, "nom": "Master Gestion & Data"}
                ]
            }
        except Exception as e:
            logging.error(f"Erreur ML Adapter: {str(e)}")
            return {"status": "error", "message": str(e), "data": []}

    def identifier_points_forts(self, profil: Dict[str, Any]) -> List[str]:
        # ⚠️ À REMPLACER PLUS TARD : Cette logique basique devra être remplacée par l'analyse du vrai modèle
        points = []
        notes = profil.get("notes", {})
        if notes.get("Mathématiques", 0) >= 14:
            points.append("Aptitudes solides en compétences quantitatives")
        if "Python" in profil.get("competences", []):
            points.append("Maîtrise de la programmation en Python")
        if not points:
            points.append("Profil polyvalent avec potentiel d'apprentissage")
        return points

ml_adapter = MLAdapter()