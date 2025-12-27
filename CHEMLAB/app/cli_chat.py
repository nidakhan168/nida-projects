import os
from datetime import datetime

from chatbot_core import ChemLabBuddy


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAQ_PATH = os.path.join(BASE_DIR, "data", "chem_faq.csv")
LOG_PATH = os.path.join(BASE_DIR, "logs", "unknown_questions.log")


def log_unknown_question(question: str, score: float) -> None:
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().isoformat()} | score={score:.3f} | {question}\n")


def main():
    print(f"[cli_chat] FAQ_PATH = {FAQ_PATH}")
    bot = ChemLabBuddy(FAQ_PATH)

    print("🧪 Welcome to ChemLabBuddy – Virtual Chemistry Lab Assistant")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        user_query = input("You: ").strip()
        if user_query.lower() in {"exit", "quit"}:
            print("Bot: Goodbye! Stay safe in the lab 👋")
            break

        answer, topic, score = bot.get_answer(user_query)

        if answer is None:
            print(
                "Bot: I'm not sure about that yet. "
                "Please check your lab manual or supervisor."
            )
            log_unknown_question(user_query, score)
        else:
            print(f"Bot ({topic}, match={score:.2f}): {answer}\n")


if __name__ == "__main__":
    main()
