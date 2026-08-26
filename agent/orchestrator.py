import os
import json
import logging
import traceback
import asyncio
from dotenv import load_dotenv
from google import genai
from google.genai import types

from agent.system_prompt import SYSTEM_INSTRUCTION
from agent.tools import tool_analyser_profil_ml, tool_rechercher_doc_rag, tool_verifier_prerequis

# --- CONFIGURATION DU LOGGER ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s : %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("OrientIA")

load_dotenv()


class OrientIAAgent:
    def __init__(self):
        logger.info("Initialisation de l'agent OrientIA...")
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_name = "gemini-3.6-flash"
        self.tools_map = {
            "tool_analyser_profil_ml": tool_analyser_profil_ml,
            "tool_rechercher_doc_rag": tool_rechercher_doc_rag,
            "tool_verifier_prerequis": tool_verifier_prerequis
        }

    async def _executer_outil(self, func_name: str, func_args: dict):
        """Exécute un outil, qu'il soit synchrone ou asynchrone (coroutine)."""
        if func_name not in self.tools_map:
            return f"Erreur : L'outil {func_name} n'existe pas."

        tool_func = self.tools_map[func_name]
        try:
            if asyncio.iscoroutinefunction(tool_func):
                resultat_outil = await tool_func(**func_args)
            else:
                resultat_outil = tool_func(**func_args)
        except Exception as e_outil:
            logger.error(f"Erreur lors de l'exécution de l'outil {func_name} : {str(e_outil)}")
            resultat_outil = f"Erreur technique : {str(e_outil)}"

        return resultat_outil

    async def executer_dialogue(self, message_utilisateur: str, historique: list = None) -> dict:
        """Orchestre la réflexion, le choix des outils et la réponse finale de manière ASYNCHRONE."""
        logger.info(f"Nouveau message reçu (Standard) : '{message_utilisateur[:60]}...'")
        outils_appeles = []
        tools_list = [tool_analyser_profil_ml, tool_rechercher_doc_rag, tool_verifier_prerequis]

        try:
            response = await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=message_utilisateur,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    tools=tools_list,
                    temperature=0.2,
                )
            )

            if response.function_calls:
                for call in response.function_calls:
                    func_name = call.name
                    func_args = call.args
                    outils_appeles.append({"outil": func_name, "arguments": func_args})

                    resultat_outil = await self._executer_outil(func_name, func_args)

                    response = await self.client.aio.models.generate_content(
                        model=self.model_name,
                        contents=f"Résultat de l'outil {func_name}: {resultat_outil}\nQuestion initiale: {message_utilisateur}",
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_INSTRUCTION,
                            temperature=0.2,
                        )
                    )

            return {
                "reponse_finale": response.text,
                "traces": {
                    "outils_executes": outils_appeles,
                    "modele_llm": self.model_name,
                    "statut": "Succès"
                }
            }

        except Exception as e_global:
            logger.error("CRASH GLOBAL DE L'ORCHESTRATEUR :")
            logger.error(traceback.format_exc())
            return {
                "reponse_finale": "Désolé, je rencontre actuellement une difficulté technique. Pouvez-vous réessayer dans quelques instants ?",
                "traces": {
                    "outils_executes": outils_appeles,
                    "modele_llm": self.model_name,
                    "statut": "Erreur Critique",
                    "erreur_technique": str(e_global)
                }
            }

    async def executer_dialogue_stream(self, message_utilisateur: str):
        """Orchestre le dialogue en mode STREAMING (effet machine à écrire) avec exécution des outils."""
        logger.info(f"Nouveau message reçu (Streaming) : '{message_utilisateur[:60]}...'")
        tools_list = [tool_analyser_profil_ml, tool_rechercher_doc_rag, tool_verifier_prerequis]

        try:
            # Étape 1 : Analyse initiale et exécution des outils si nécessaire
            response = await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=message_utilisateur,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    tools=tools_list,
                    temperature=0.2,
                )
            )

            final_prompt = message_utilisateur
            if response.function_calls:
                for call in response.function_calls:
                    func_name = call.name
                    func_args = call.args
                    logger.info(f"Exécution de l'outil (Stream) : {func_name}")

                    resultat_outil = await self._executer_outil(func_name, func_args)

                    final_prompt = f"Résultat de l'outil {func_name}: {resultat_outil}\nQuestion initiale: {message_utilisateur}"

            # Étape 2 : Génération de la réponse en flux continu (Streaming)
            logger.info("Début du streaming de la réponse finale...")
            async for chunk in await self.client.aio.models.generate_content_stream(
                model=self.model_name,
                contents=final_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=0.2,
                )
            ):
                if chunk.text:
                    yield chunk.text

        except Exception as e_stream:
            logger.error(f"Erreur lors du streaming : {str(e_stream)}")
            yield "Désolé, une erreur technique est survenue lors de la génération de la réponse."