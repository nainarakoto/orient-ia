import sys
import os
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.orchestrator import OrientIAAgent

async def executer_scenario():
    print("==================================================")
    print("🎬 LANCEMENT DU SCÉNARIO DE TEST GLOBAL D'ORIENT'IA")
    print("==================================================")
    
    agent = OrientIAAgent()
    
    # --- SCÉNARIO 1 : Test du Gardien (Hors-sujet) ---
    print("\n--- [TEST 1] Tentative de hors-sujet (Sécurité) ---")
    msg_hors_sujet = "Peux-tu me donner une recette de cuisine malgache ? "
    print(f"👤 Utilisateur : {msg_hors_sujet}")
    
    reponse_1 = await agent.executer_dialogue(msg_hors_sujet)
    print(f"🤖 Agent :\n{reponse_1['reponse_finale']}")
    
    # --- SCÉNARIO 2 : Test Nominal Complet (ML + RAG + Knowledge + Balises) ---
    print("\n--- [TEST 2] Requête complexe avec appels d'outils et traçabilité ---")
    msg_nominal = (
        "Bonjour, je m'appelle Joël, j'ai d'excellentes notes en mathématiques et algorithmique. "
        "Je souhaite intégrer la filière ISAIA à l'ISPM. "
        "Peux-tu analyser mon profil, vérifier les documents officiels et valider mes prérequis ?"
    )
    print(f"👤 Utilisateur : {msg_nominal}")
    
    resultat_nominal = await agent.executer_dialogue(msg_nominal)
    
    print("\n🤖 RÉPONSE FINALE DE L'AGENT :")
    print(resultat_nominal["reponse_finale"])
    
    print("\n🔍 TRACES & OBSERVABILITÉ :")
    print(f"Statut : {resultat_nominal['traces'].get('statut')}")
    print(f"Outils exécutés : {resultat_nominal['traces'].get('outils_executes')}")
    print("==================================================")
    print("✅ SCÉNARIO GLOBAL TERMINÉ AVEC SUCCÈS !")
    print("==================================================")

if __name__ == "__main__":
    asyncio.run(executer_scenario())