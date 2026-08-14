from models import create_model
from agents.orchestrator import Orchestrator


def main():

    llm = create_model(
        provider="gemini",
        model_name="gemini-2.5-flash",
        temperature=0,
    )

    orchestrator = Orchestrator(llm)

    print("Multi-agent system ready.")
    print("Type 'exit' to quit.")

    while True:

        user_input = input("\nUser: ")

        if user_input.lower() in {"exit", "quit"}:
            break

        try:
            answer = orchestrator.run(user_input)

            print("\nFinal Answer:")
            print(answer)

        except Exception as exc:
            print(f"\nError: {exc}")


if __name__ == "__main__":
    main()
