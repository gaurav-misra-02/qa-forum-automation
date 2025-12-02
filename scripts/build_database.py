import argparse
from pathlib import Path

from src.database.vector_db import VectorDatabase
from src.config import Config


def main():
    parser = argparse.ArgumentParser(description='Build vector database from text content')
    parser.add_argument(
        '--input',
        type=Path,
        default=Config.BASE_DIR / 'Task_Theory_Part_1.txt',
        help='Path to input text file'
    )
    parser.add_argument(
        '--code-examples',
        type=Path,
        default=Config.BASE_DIR / 'Code_QnA.xlsx',
        help='Path to code examples Excel file'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Config.DATA_DIR / 'Task_Theory_Part_1_DB.json',
        help='Path to save vector database'
    )
    
    args = parser.parse_args()
    
    print(f"Reading content from {args.input}")
    with open(args.input, 'r', encoding='utf8') as f:
        contexts = f.read()
    
    print("Building vector database...")
    vector_db = VectorDatabase(contexts, args.output, args.code_examples)
    vector_db.create_database()
    
    print(f"Vector database saved to {args.output}")


if __name__ == "__main__":
    main()

