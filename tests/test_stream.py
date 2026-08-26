import sys
import os
import asyncio

# Ajoute le dossier parent au chemin Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.orchestrator import OrientIAAgent

async def tester_streaming():
    print("==================================================")
    print("🌊 TEST DU STREAMING (EFFET MACHINE À ÉCRIRE)")
    print("==================================================")
    
    agent = OrientIAAgent()
    message = (
        "Bonjour, je m'appelle Joël. J'ai de très bonnes notes en mathématiques "
        "et je m'intéresse à l'intelligence artificielle. Peux-tu me présenter le parcours ISAIA à l'ISPM ?"
    )
    
    print(f"👤 Message envoyé : {message}\n")
    print("🤖 Réponse en direct de l'agent :")
    print("--------------------------------------------------")
    
    # Consommation du générateur asynchrone (chunk par chunk)
    async for chunk in agent.executer_dialogue_stream(message):
        # flush=True force l'affichage immédiat du mot dans la console
        print(chunk, end="", flush=True)
        
    print("\n--------------------------------------------------")
    print("==================================================")
    print("✅ TEST DE STREAMING TERMINÉ AVEC SUCCÈS !")
    print("==================================================")

if __name__ == "__main__":
    asyncio.run(tester_streaming())