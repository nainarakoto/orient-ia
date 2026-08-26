# ORIENT'IA — Backend (M5)

## Démarrer

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Docs interactives auto-générées : http://localhost:8000/docs

## Endpoints (§17 du plan)

- `POST /profile` — créer/mettre à jour un profil
- `GET /profile/{id}` — lire un profil
- `POST /recommend` — **endpoint central** : profil (+question) → ML → RAG → règles → recommandation expliquée et sourcée
- `POST /chat` — interaction conversationnelle libre (route vers le même orchestrateur)
- `GET /formations` / `GET /formations/{id}` — corpus des formations
- `GET /evaluate/cases` — liste les cas de test (`data/test_cases.json`)
- `POST /evaluate/run` — exécute tous les cas de test contre l'agent réel et renvoie des résultats chiffrés
- `GET /traces` — dernières traces d'exécution (à afficher en live pendant la démo, §20/§23)

## Où brancher le travail des autres membres

| Fichier | À remplacer par | Responsable |
|---|---|---|
| `ml_service.py` | Appel au vrai modèle entraîné (garder la signature `score_parcours`) | M2 |
| `rag_engine.py` | Vrai pipeline embeddings + vector DB (garder la signature `search`) | M3 |
| `data/formations.json` | Vrai corpus structuré collecté | M1 |
| `data/test_cases.json` | Les 32 cas de test réels par catégorie (§13) | M6 |
| `tool_registry.py` | Ajouter/affiner des outils si besoin (garder ≥3 outils réels) | M4 |
| `agent_orchestrator.py` | Insérer un vrai LLM pour la génération conversationnelle si le temps le permet | M4 |

## Ce qui est déjà fonctionnel de bout en bout

- Workflow complet §10/§18 : profil → clarification si incomplet → RAG → ML → règles prérequis → explication distinguant ML/documents/règles → citations → incertitude → trace.
- Sécurité (§16/§21) : refus testé pour prompt injection, critères discriminatoires, profilage psychologique — **avant** même d'appeler l'agent.
- Mention légale obligatoire injectée automatiquement dans chaque `RecommendResponse` (§16).
- Traces JSON-lines (`observability/traces.jsonl`) consultables via `GET /traces` — utile pour prouver en démo que ML/RAG sont réellement appelés.
- Baselines ML (similarité mots-clés) et RAG (recherche lexicale) qui tournent sans dépendance externe, pour que toute l'équipe puisse développer contre une API stable dès aujourd'hui.

## Non testé dans ce sandbox

Le sandbox de génération n'avait pas d'accès réseau pour installer `fastapi`/`pydantic` :
le code a été vérifié par compilation (`py_compile`) et par un test manuel du module
`security_guard` (sans dépendance externe), qui passe. **Lance `pip install -r
requirements.txt` puis `uvicorn main:app --reload` dès que possible pour valider l'API
elle-même (routes, sérialisation Pydantic, etc.).**
