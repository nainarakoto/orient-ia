import os
import json
import asyncio
import logging

from groq import AsyncGroq

from agent.tools import tool_analyser_profil_ml, tool_rechercher_doc_rag, tool_verifier_prerequis

logger = logging.getLogger("OrientIA")

GROQ_MODEL = "openai/gpt-oss-20b"

# Nombre maximum d'allers-retours "appel d'outil -> résultat -> nouvel appel"
# avant de forcer une réponse finale sans outils (protection anti-boucle infinie).
MAX_TOOL_ROUNDS = 3

_groq_client = None


def _get_client():
    global _groq_client
    if _groq_client is None:
        _groq_client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
    return _groq_client


TOOLS_MAP = {
    "tool_analyser_profil_ml": tool_analyser_profil_ml,
    "tool_rechercher_doc_rag": tool_rechercher_doc_rag,
    "tool_verifier_prerequis": tool_verifier_prerequis,
}

# Groq (API compatible OpenAI) attend un schéma JSON explicite pour chaque
# outil, contrairement au SDK Gemini qui génère ça automatiquement à partir
# des type hints Python. On réutilise les docstrings existantes (déjà
# enrichies avec la liste des métiers pour tool_analyser_profil_ml).
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "tool_analyser_profil_ml",
            "description": tool_analyser_profil_ml.__doc__,
            "parameters": {
                "type": "object",
                "properties": {
                    "age": {"type": "integer"},
                    "sexe": {"type": "string"},
                    "serie": {"type": "string"},
                    "moyenne_generale": {"type": "number"},
                    "preferences_env": {"type": "string"},
                    "objectif_professionnel": {"type": "string"},
                    "matieres_fortes": {"type": "array", "items": {"type": "string"}},
                    "matieres_faibles": {"type": "array", "items": {"type": "string"}},
                    "centres_interet": {"type": "array", "items": {"type": "string"}},
                    "competences": {"type": "array", "items": {"type": "string"}},
                },
                "required": [
                    "age", "sexe", "serie", "moyenne_generale", "preferences_env",
                    "objectif_professionnel", "matieres_fortes", "matieres_faibles",
                    "centres_interet", "competences",
                ],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "tool_rechercher_doc_rag",
            "description": tool_rechercher_doc_rag.__doc__,
            "parameters": {
                "type": "object",
                "properties": {
                    "requete": {"type": "string"},
                },
                "required": ["requete"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "tool_verifier_prerequis",
            "description": tool_verifier_prerequis.__doc__,
            "parameters": {
                "type": "object",
                "properties": {
                    "parcours": {"type": "string"},
                    "matieres": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["parcours", "matieres"],
            },
        },
    },
]


async def _executer_outil(func_name: str, func_args: dict):
    if func_name not in TOOLS_MAP:
        return f"Erreur : L'outil {func_name} n'existe pas."

    tool_func = TOOLS_MAP[func_name]
    try:
        if asyncio.iscoroutinefunction(tool_func):
            return await tool_func(**func_args)
        return tool_func(**func_args)
    except Exception as e_outil:
        logger.error(f"Erreur outil (fallback Groq) {func_name} : {str(e_outil)}")
        return f"Erreur technique : {str(e_outil)}"


async def executer_dialogue_groq(message_utilisateur: str, system_instruction: str) -> dict:
    """Rejoue le dialogue via Groq/Llama quand Gemini est indisponible (quota épuisé)."""
    client = _get_client()
    outils_appeles = []

    messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": message_utilisateur},
    ]

    try:
        message = None

        for _ in range(MAX_TOOL_ROUNDS):
            response = await client.chat.completions.create(
                model=GROQ_MODEL,
                messages=messages,
                tools=TOOLS_SCHEMA,
                tool_choice="auto",
                temperature=0.2,
            )
            message = response.choices[0].message

            if not message.tool_calls:
                break

            messages.append(message.model_dump(exclude_unset=True))
            for call in message.tool_calls:
                func_name = call.function.name
                func_args = json.loads(call.function.arguments)
                outils_appeles.append({"outil": func_name, "arguments": func_args})

                resultat_outil = await _executer_outil(func_name, func_args)

                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": str(resultat_outil),
                })
        else:
            # On a atteint la limite de tours d'outils : on force une réponse
            # finale texte, sans redonner d'outils au modèle, pour éviter une
            # boucle infinie tout en garantissant une réponse à l'utilisateur.
            response = await client.chat.completions.create(
                model=GROQ_MODEL,
                messages=messages,
                tool_choice="none",
                temperature=0.2,
            )
            message = response.choices[0].message

        return {
            "reponse_finale": message.content or "Désolé, je n'ai pas pu formuler de réponse.",
            "traces": {
                "outils_executes": outils_appeles,
                "modele_llm": GROQ_MODEL,
                "statut": "Succès (Fallback Groq)",
            },
        }

    except Exception as e:
        logger.error(f"Le fallback Groq a également échoué : {e}")
        return {
            "reponse_finale": "Désolé, je rencontre actuellement une difficulté technique. Pouvez-vous réessayer dans quelques instants ?",
            "traces": {
                "outils_executes": outils_appeles,
                "modele_llm": "aucun (Groq indisponible)",
                "statut": "Erreur Critique",
                "erreur_technique": str(e),
            },
        }


async def executer_dialogue_stream_groq(message_utilisateur: str, system_instruction: str):
    """Version streaming du fallback Groq."""
    client = _get_client()

    messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": message_utilisateur},
    ]

    try:
        for _ in range(MAX_TOOL_ROUNDS):
            response = await client.chat.completions.create(
                model=GROQ_MODEL,
                messages=messages,
                tools=TOOLS_SCHEMA,
                tool_choice="auto",
                temperature=0.2,
            )
            message = response.choices[0].message

            if not message.tool_calls:
                break

            messages.append(message.model_dump(exclude_unset=True))
            for call in message.tool_calls:
                func_name = call.function.name
                func_args = json.loads(call.function.arguments)
                logger.info(f"Exécution de l'outil (Stream, fallback Groq) : {func_name}")

                resultat_outil = await _executer_outil(func_name, func_args)

                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": str(resultat_outil),
                })
        else:
            # Limite de tours d'outils atteinte : on ne redonne pas d'outils,
            # le prochain appel (streaming) ci-dessous partira sans tools.
            pass

        stream = await client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=0.2,
            stream=True,
        )

        async for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                yield delta.content

    except Exception as e:
        logger.error(f"Le fallback Groq (stream) a également échoué : {e}")
        yield "Désolé, une erreur technique est survenue lors de la génération de la réponse."