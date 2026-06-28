# chat.py
from app.db.database import SessionLocal
from app.services.query_service import understand_query
from app.services.search_service import search_from_query_result
from app.services.response_service import process_chat

def main():
    db = SessionLocal()
    print("=" * 50)
    print("   AI Bank Chatbot")
    print("=" * 50)
    print("Ask me anything about the bank!")
    print("Type 'exit' or 'quit' to stop.")
    print("=" * 50)
    print()

    while True:
        try:
            question = input("You: ").strip()

            if not question:
                continue

            if question.lower() in ("exit", "quit", "bye"):
                print("Bot: Goodbye! Have a great day.")
                break

            query_result = understand_query(question)
            search_result = search_from_query_result(db, query_result)
            chat_response = process_chat(db, question, search_result)

            print(f"Bot: {chat_response['answer']}")
            print()

        except KeyboardInterrupt:
            print("\nBot: Goodbye! Have a great day.")
            break

    db.close()

if __name__ == "__main__":
    main()