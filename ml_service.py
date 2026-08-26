"""
ML service — interface entre le backend/agent et le modèle entraîné par M2.

MVP : baseline de similarité mots-clés (score de similarité intérêts <-> matières)
pour que l'API tourne de bout en bout dès aujourd'hui. À REMPLACER par
l'appel au vrai modèle (ranking/score d'adéquation, §7) dès qu'il est prêt —
sans changer la signature de `score_parcours`, pour ne rien casser côté agent.
"""
from __future__ import annotations
from schemas import Profile, Formation, ScoreParcours


def _jaccard(a: list[str], b: list[str]) -> float:
    sa, sb = {x.lower() for x in a}, {x.lower() for x in b}
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def score_parcours(profile: Profile, formations: list[Formation]) -> list[ScoreParcours]:
    """
    Retourne un score [0,1] par parcours + vérification des prérequis.

    TODO (M2): remplacer ce calcul par l'appel réel au modèle entraîné,
    ex: `MODEL.predict_proba(featurize(profile))`. Garder la même sortie
    (liste de ScoreParcours) pour que l'agent n'ait rien à changer.
    """
    results: list[ScoreParcours] = []
    for f in formations:
        sim_matieres = _jaccard(profile.matieres_preferees, f.matieres)
        sim_competences = _jaccard(profile.competences_declarees, f.competences)
        sim_interets = _jaccard(profile.interets, f.matieres + f.competences)
        score = round(0.4 * sim_matieres + 0.3 * sim_competences + 0.3 * sim_interets, 4)

        prerequis_manquants = [
            p for p in f.prerequis
            if p.lower() not in {c.lower() for c in profile.competences_declarees}
        ]
        results.append(
            ScoreParcours(
                parcours_id=f.id,
                score_ml=score,
                prerequis_ok=len(prerequis_manquants) == 0,
                prerequis_manquants=prerequis_manquants,
            )
        )
    return sorted(results, key=lambda r: r.score_ml, reverse=True)
