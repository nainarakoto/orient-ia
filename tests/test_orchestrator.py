import asyncio
from agent.orchestrator import OrientIAAgent  # adapte le chemin d'import si le fichier a un autre nom/emplacement


async def test_mode_normal():
    print("\n========== TEST MODE NORMAL ==========")
    agent = OrientIAAgent()
    resultat = await agent.executer_dialogue(
        "J'ai 18 ans, je suis en série C, ma moyenne est de 14, je préfère travailler "
        "en laboratoire, mon objectif est de devenir ingénieur. Je suis fort en maths "
        "et physique, faible en langues, j'aime la programmation, mes compétences sont "
        "Python et statistiques. Quelle filière me recommandes-tu ?"
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