from enum import Enum

class Intent(Enum):
    FACTUAL = "factual"
    RECOMMENDATION = "recommendation"
    COMPARISON = "comparison"
    OFFICIAL_DECISION = "official_decision"
    PSYCHOLOGICAL_PROFILING = "psychological_profiling"
    PROMPT_INJECTION = "prompt_injection"

def classify_intent(message: str) -> Intent:
    msg_lower = message.lower()
    
    if any(k in msg_lower for k in ["ignore toutes les regles", "ignore previous instructions"]):
        return Intent.PROMPT_INJECTION

    if any(k in msg_lower for k in ["suis-je admis", "admission officielle", "garantie de reussite", "est-ce que je suis pris"]):
        return Intent.OFFICIAL_DECISION

    if any(k in msg_lower for k in ["mon caractere", "ma personnalite", "analyse mon psychisme", "suis-je anxieux"]):
        return Intent.PSYCHOLOGICAL_PROFILING

    if any(k in msg_lower for k in ["compare", "comparer", "difference entre"]):
        return Intent.COMPARISON

    if any(k in msg_lower for k in ["recommande", "quelle formation", "orientation", "quel parcours"]):
        return Intent.RECOMMENDATION

    return Intent.FACTUAL