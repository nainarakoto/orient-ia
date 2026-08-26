import sys
import os

# Ajoute le dossier parent au chemin de recherche Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.orchestrator import OrientIAAgent

def tester_agent_global():
    print("==================================================")
    print("🚀 INITIALISATION DU TEST GLOBAL D'ORIENT'IA")
    print("==================================================")
    
    agent = OrientIAAgent()
    
    # Message complexe contenant plusieurs intentions :
    # 1. Fournir des notes et intérêts (doit déclencher l'outil ML)
    # 2. Poser une question sur les prérequis officiels (doit déclencher l'outil RAG)
    # 3. Demander une vérification de validation de parcours (doit déclencher l'outil Graphe/Knowledge)
    message_complexe = (
        "Bonjour, je m'appelle Joël. J'ai de très bonnes notes en Mathématiques et en Algorithmique, "
        "et je m'intéresse passionnément à l'Intelligence Artificielle et au Big Data. "
        "Est-ce que mon profil correspond au parcours ISAIA à l'ISPM ? "
        "Peux-tu lancer une analyse complète de mon profil, vérifier les documents officiels de la brochure "
        "et valider si mes prérequis académiques sont conformes ?"
    )
    
    print(f"\n📩 MESSAGE UTILISATEUR :\n{message_complexe}\n")
    print("⏳ L'agent analyse la demande et sélectionne les outils nécessaires...\n")
    
    # Exécution
    resultat = agent.executer_dialogue(message_complexe)
    
    print("==================================================")
    print("🤖 RÉPONSE FINALE DE L'AGENT")
    print("==================================================")
    print(resultat["reponse_finale"])
    
    print("\n==================================================")
    print("🔍 TRACES TECHNIQUES D'OBSERVABILITÉ")
    print("==================================================")
    print(f"Modèle LLM utilisé : {resultat['traces']['modele_llm']}")
    print(f"Outils déclenchés par le LLM : {resultat['traces']['outils_executes']}")
    print("==================================================")

if __name__ == "__main__":
    tester_agent_global()