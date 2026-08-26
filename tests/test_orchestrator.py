import asyncio
from agent.orchestrator import OrientIAAgent  # adapte le chemin d'import si le fichier a un autre nom/emplacement


async def test_mode_normal():
    print("\n========== TEST MODE NORMAL ==========")
    agent = OrientIAAgent()
    resultat = await agent.executer_dialogue(
        "Quels sont les prérequis pour la filière ISAIA ?"
    )
    print("\n--- Réponse finale ---")
    print(resultat["reponse_finale"])
    print("\n--- Traces ---")
    print(resultat["traces"])


async def test_mode_streaming():
    print("\n========== TEST MODE STREAMING ==========")
    agent = OrientIAAgent()
    print("\n--- Réponse en streaming ---")
    async for chunk in agent.executer_dialogue_stream(
        "Parle-moi de la filière ISAIA et de ses débouchés."
    ):
        print(chunk, end="", flush=True)
    print()


async def main():
    await test_mode_normal()
    await test_mode_streaming()


if __name__ == "__main__":
    asyncio.run(main())