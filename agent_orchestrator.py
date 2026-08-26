"""
Agent orchestrator — ORIENT'IA (§10, §18 du plan)

Implémente le workflow exact décrit dans le sujet :
  1. réception question
  2. mise à jour du profil
  3. clarification si info essentielle manquante
  4. appel outils factuels (RAG / prérequis / comparaison)
  5. appel du modèle ML
  6. application des règles (filtrage/pénalité prérequis)
  7. vérification de cohérence ML <-> règles <-> documents
  8. génération de l'explication (facteurs distingués)
  9. ajout des citations
  10. déclaration d'incertitude si besoin
  11. réponse finale
  12. enregistrement de la trace

NOTE : ce module n'appelle PAS de LLM externe pour rester autonome et
testable sans clé API. Le texte de "génération" (étape 8) est actuellement
assemblé par `tool_registry.expliquer_recommandation`. Si l'équipe branche un
vrai LLM (agent conversationnel libre, §9 "Capacités conversationnelles"),
c'est ICI qu'il faut l'insérer, entre les étapes 7 et 8, en lui donnant en
contexte : profil, scores ML, passages RAG, règles appliquées — jamais en
lui laissant inventer des faits hors de ce contexte (cf. security_guard).
"""
from __future__ import annotations
import time

from schemas import (
    Profile, RecommendResponse, RecommendationExplanation,
    Trace, ToolCallTrace,
)
import tool_registry
import security_guard
from trace_logger import log_trace


def run_recommendation(profile: Profile, question: str | None = None) -> RecommendResponse:
    start = time.perf_counter()
    trace = Trace(question=question, profil=profile.model_dump())

    # --- Étape "sécurité amont" (couvre T26-T32) ---------------------------
    if question:
        verdict = security_guard.check_input(question)
        if not verdict.allowed:
            trace.erreurs_refus.append(f"{verdict.category}: {verdict.reason}")
            trace.reponse_finale = verdict.reason
            trace.latence_ms = (time.perf_counter() - start) * 1000
            log_trace(trace)
            return RecommendResponse(
                trace_id=trace.trace_id,
                parcours_recommandes=[],
                explication=RecommendationExplanation(texte_genere=verdict.reason),
                refus=verdict.reason,
            )

    # --- Étape 3 : clarification si profil trop pauvre ---------------------
    if not profile.is_complete_enough_for_recommendation():
        msg = (
            "Pour vous orienter, il me manque des informations essentielles : "
            "pouvez-vous indiquer au moins vos matières préférées, vos centres "
            "d'intérêt ou des compétences que vous pensez avoir développées ?"
        )
        trace.reponse_finale = msg
        trace.erreurs_refus.append("profil_incomplet")
        trace.latence_ms = (time.perf_counter() - start) * 1000
        log_trace(trace)
        return RecommendResponse(
            trace_id=trace.trace_id,
            parcours_recommandes=[],
            explication=RecommendationExplanation(texte_genere=msg, incertitude=msg),
        )

    # --- Étape 4 : outil RAG (si une question texte a été posée) -----------
    passages = []
    if question:
        passages = tool_registry.rechercher_formation(question)
        trace.outils_appeles.append(ToolCallTrace(
            nom="rechercher_formation", input={"query": question},
            output={"n_passages": len(passages)},
        ))
        trace.passages_recuperes.extend(passages)

    # --- Étape 5 : outil ML --------------------------------------------------
    scores = tool_registry.calculer_score_adequation(profile)
    trace.outils_appeles.append(ToolCallTrace(
        nom="calculer_score_adequation",
        input={"profile_id": profile.id},
        output={"n_scores": len(scores)},
    ))

    # --- Étape 6 : règles (prérequis) — déjà calculées dans ScoreParcours ---
    regles_appliquees = []
    for s in scores[:3]:
        if not s.prerequis_ok:
            regles_appliquees.append(
                f"Parcours {s.parcours_id} pénalisé : prérequis manquants "
                f"({', '.join(s.prerequis_manquants)})"
            )

    # --- Étape 7 : cohérence — on ne recommande que des parcours dont on a
    #     un score, en priorisant ceux dont les prérequis sont remplis -------
    scores_ok_dabord = sorted(scores, key=lambda s: (not s.prerequis_ok, -s.score_ml))
    top_parcours = [s.parcours_id for s in scores_ok_dabord[:3] if s.score_ml > 0]

    # --- Étape 8-9 : génération de l'explication + citations ----------------
    texte = tool_registry.expliquer_recommandation(scores_ok_dabord, passages, regles_appliquees)

    # --- Étape 10 : incertitude ----------------------------------------------
    incertitude = None
    if not top_parcours:
        incertitude = (
            "Les informations fournies ne permettent pas d'identifier un "
            "parcours avec confiance. Un échange avec un conseiller "
            "pédagogique de l'ISPM est recommandé."
        )

    explication = RecommendationExplanation(
        facteurs_ml=scores_ok_dabord[:5],
        facteurs_documentaires=passages,
        regles_appliquees=regles_appliquees,
        texte_genere=texte,
        incertitude=incertitude,
    )

    # --- Étape 12 : trace ------------------------------------------------------
    trace.reponse_finale = texte
    trace.latence_ms = (time.perf_counter() - start) * 1000
    log_trace(trace)

    return RecommendResponse(
        trace_id=trace.trace_id,
        parcours_recommandes=top_parcours,
        explication=explication,
    )
