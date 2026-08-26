# orient-ia

# RAG (M3) — Comment l'utiliser

## Installation (une seule fois)

```bash
cd rag
pip install -r requirements.txt
python build_index.py
```

⚠️ Après chaque `git pull` sur cette branche, relancer `python build_index.py` — l'index n'est pas versionné (fichiers générés, dans le `.gitignore`).

## Utilisation

```python
from rag.rag_service import rechercher_formation

resultats = rechercher_formation("Quelles matières en licence informatique ?", top_k=5)
```

**Sortie :**
```python
[
    {
        "formation_id": "info-l3",
        "extrait": "Matières enseignées en Licence Informatique : ...",
        "source_id": "src-test-01",
        "score": 0.493
    },
    ...
]
```

- Liste vide `[]` = information absente du corpus. C'est normal, pas une erreur — ne pas inventer de réponse dans ce cas.
- `source_id` = à citer dans la réponse finale (voir `data/registre_sources.csv` de M1).

Exemples réels testés : voir `rag/exemple_input_output.json`.