"""Entry point for the Agentic AI-Based Personalized Assistant."""

from agent_controller import AgentController
from database import init_db


def main() -> None:
    """Run the assistant with a simple console interface."""

    init_db()
    controller = AgentController()

    print("\nAgentic AI Assistant ready!")
    print("Examples:")
    print("- check email")
    print("- add task title=ProjectDemo date=2025-01-10 time=14:00 priority=High")
    print("- show tasks")
    print("- start reminders")
    print("- exit")

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        controller.handle_input(user_input)


if __name__ == "__main__":
    main()
