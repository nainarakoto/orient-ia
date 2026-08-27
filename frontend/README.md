# ORIENT'IA

Assistant d'aide à l'orientation pédagogique pour l'ISPM. Prototype combinant acquisition de
données, Machine Learning et assistant conversationnel, développé dans le cadre d'un hackathon.

## Structure du projet

- `backend/` — API exposant les formations, le modèle ML et l'agent conversationnel
- `frontend/` — interface Streamlit destinée aux utilisateurs
- `data/` — corpus pédagogique et jeux de données
- `survey/` — questionnaire d'enquête et registre de collecte
- `ml/` — entraînement et évaluation du modèle de Machine Learning
- `rag/` — indexation et recherche documentaire
- `agent/` — orchestration de l'agent conversationnel et de ses outils
- `knowledge/` — ontologie et graphe de connaissances
- `evaluation/` — jeu de test et résultats d'évaluation
- `observability/` — traces d'exécution
- `docs/` — schéma d'architecture, notes de limites et de biais
- `tests/` — tests automatisés
- `scripts/` — scripts utilitaires

## Lancer l'interface

```bash
pip install -r requirements.txt
cd frontend
streamlit run app.py
```

Sans backend disponible, l'interface fonctionne avec des données fictives clairement identifiées
comme telles. Pour connecter un backend, définir la variable d'environnement `ORIENTIA_BACKEND_URL`.

## Mention obligatoire

ORIENT'IA constitue un outil d'aide à l'orientation. Ses recommandations ne remplacent ni l'avis
d'un conseiller pédagogique ni une décision officielle d'admission.
