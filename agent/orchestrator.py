import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

from agent.system_prompt import SYSTEM_INSTRUCTION
from agent.tools import tool_analyser_profil_ml, tool_rechercher_doc_rag, tool_verifier_prerequis

load_dotenv()

class OrientIAAgent:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_name = "gemini-3.6-flash"
        # Cartographie des fonctions exécutables
        self.tools_map = {
            "tool_analyser_profil_ml": tool_analyser_profil_ml,
            "tool_rechercher_doc_rag": tool_rechercher_doc_rag,
            "tool_verifier_prerequis": tool_verifier_prerequis
        }

    def executer_dialogue(self, message_utilisateur: str, historique: list = None) -> dict:
        """Orchestre la réflexion, le choix des outils et la réponse finale[cite: 4]."""
        tools_list = [tool_analyser_profil_ml, tool_rechercher_doc_rag, tool_verifier_prerequis]
        
        # Appel initial à Gemini
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=message_utilisateur,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                tools=tools_list,
                temperature=0.2,
            )
        )

        outils_appeles = []
        
        # Gestion automatique du Function Calling si le LLM décide d'appeler un outil
        if response.function_calls:
            for call in response.function_calls:
                func_name = call.name
                func_args = call.args
                outils_appeles.append({"outil": func_name, "arguments": func_args})
                
                # Exécution de l'outil Python correspondant
                if func_name in self.tools_map:
                    resultat_outil = self.tools_map[func_name](**func_args)
                    
                    # Deuxième passage au LLM avec le résultat de l'outil
                    response = self.client.models.generate_content(
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
                "modele_llm": self.model_name
            }
        }