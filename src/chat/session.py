from typing import List, Dict, Optional
import json

from src.llm.client import LLMClient
from src.database.retriever import Retriever
from src.config import Config


class ChatSession:
    def __init__(self, contexts: List[Dict], instruction: str = Config.INSTRUCTION_TEMPLATE):
        self.retriever = Retriever(contexts)
        self.llm_client = LLMClient()
        self.instruction = instruction
        self.history = ""
        self.turn_count = 0
    
    def process_query(self, user_input: str) -> str:
        self.turn_count += 1
        
        prompt = self._build_prompt(user_input)
        response = self.llm_client.generate_response(prompt)
        
        self.history = self.history + user_input + response
        
        if self.turn_count % Config.SUMMARIZE_EVERY_N_TURNS == 0:
            self._summarize_history()
        
        return response
    
    def _build_prompt(self, user_input: str) -> str:
        retrieved_context = self.retriever.build_prompt(user_input)
        full_prompt = f"{self.history}\n{retrieved_context}"
        if self.instruction:
            full_prompt = f"{full_prompt}\n{self.instruction}"
        return full_prompt
    
    def _summarize_history(self) -> None:
        summarization_prompt = (
            f"{self.history}\n"
            "Please summarize the above interaction in brief. "
            "Ensure your responses are not long."
        )
        self.history = self.llm_client.generate_response(
            summarization_prompt,
            system_prompt=Config.SUMMARIZATION_PROMPT
        )
    
    def reset(self) -> None:
        self.history = ""
        self.turn_count = 0


def single_turn_interaction(
    user_input: str,
    contexts: List[Dict],
    instruction: str = Config.INSTRUCTION_TEMPLATE
) -> str:
    retriever = Retriever(contexts)
    llm_client = LLMClient()
    
    prompt = retriever.build_prompt(user_input)
    if instruction:
        prompt = f"{prompt}\n{instruction}"
    
    return llm_client.generate_response(prompt)

