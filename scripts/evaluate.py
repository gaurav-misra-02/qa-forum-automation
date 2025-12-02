import json
import argparse
from pathlib import Path
from typing import List, Tuple, Dict, Any
import pandas as pd
import evaluate

from src.llm.client import LLMClient
from src.database.retriever import Retriever
from src.config import Config


def load_test_data(filepath: Path) -> Tuple[List[str], List[str]]:
    data = pd.read_excel(filepath)
    questions = data['Question'].tolist()
    answers = data['Answer'].tolist()
    return questions, answers


def generate_responses(
    questions: List[str],
    contexts: List[Dict[str, Any]]
) -> List[str]:
    retriever = Retriever(contexts)
    llm_client = LLMClient()
    responses = []
    
    for question in questions:
        prompt = retriever.build_prompt(f"{question}?")
        response = llm_client.generate_response(prompt)
        responses.append(response)
    
    return responses


def compute_metrics(
    predictions: List[str],
    references: List[str]
) -> Dict[str, Any]:
    bleu = evaluate.load('bleu')
    rouge = evaluate.load('rouge')
    gbleu = evaluate.load('google_bleu')
    
    return {
        'bleu': bleu.compute(predictions=predictions, references=references),
        'rouge': rouge.compute(predictions=predictions, references=references),
        'google_bleu': gbleu.compute(predictions=predictions, references=references)
    }


def save_results(
    questions: List[str],
    answers: List[str],
    responses: List[str],
    metrics: Dict[str, Any],
    output_file: Path
) -> None:
    results = []
    for q, a, r in zip(questions, answers, responses):
        results.append({
            'question': q,
            'reference_answer': a,
            'generated_response': r
        })
    
    results.append({'metrics': metrics})
    
    with open(output_file, 'w') as f:
        json.dump(results, fp=f, indent=4)


def main():
    parser = argparse.ArgumentParser(description='Evaluate chatbot responses')
    parser.add_argument(
        '--test-file',
        type=Path,
        required=True,
        help='Path to test questions Excel file'
    )
    parser.add_argument(
        '--contexts-file',
        type=Path,
        default=Config.DATA_DIR / 'Task_Theory_Part_1_DB.json',
        help='Path to vector database JSON file'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('results.json'),
        help='Path to save results'
    )
    
    args = parser.parse_args()
    
    with open(args.contexts_file, 'r') as f:
        contexts = json.load(f)
    
    questions, answers = load_test_data(args.test_file)
    responses = generate_responses(questions, contexts)
    metrics = compute_metrics(responses, answers)
    
    print("Evaluation Results:")
    print(f"BLEU Score: {metrics['bleu']}")
    print(f"ROUGE Score: {metrics['rouge']}")
    print(f"Google BLEU Score: {metrics['google_bleu']}")
    
    save_results(questions, answers, responses, metrics, args.output)
    print(f"\nResults saved to {args.output}")


if __name__ == "__main__":
    main()

