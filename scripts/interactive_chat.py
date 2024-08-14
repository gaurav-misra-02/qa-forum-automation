import json
import argparse
from pathlib import Path

from src.chat.session import ChatSession
from src.config import Config


EXIT_CODE = 8465


def main():
    parser = argparse.ArgumentParser(description='Interactive chat session')
    parser.add_argument(
        '--contexts-file',
        type=Path,
        default=Config.DATA_DIR / 'task_theory_part_1_db.json',
        help='Path to vector database JSON file'
    )
    
    args = parser.parse_args()
    
    with open(args.contexts_file, 'r') as f:
        contexts = json.load(f)
    
    session = ChatSession(contexts, Config.INSTRUCTION_TEMPLATE)
    
    print(f"Control Theory Chatbot - Interactive Session")
    print(f"To end this thread, please enter the exit code: {EXIT_CODE}\n")
    
    while True:
        user_input = input("You: ")
        
        if user_input.isnumeric() and int(user_input) == EXIT_CODE:
            print("Ending session. Goodbye!")
            break
        
        response = session.process_query(user_input)
        print(f"\nBot: {response}\n")


if __name__ == "__main__":
    main()

