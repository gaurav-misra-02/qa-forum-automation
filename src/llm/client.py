from typing import List, Dict, Optional
from openai import OpenAI

from src.config import Config


class LLMClient:
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = Config.LLM_MODEL
    
    def generate_response(
        self,
        prompt: str,
        system_prompt: str = Config.SYSTEM_PROMPT
    ) -> str:
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content
    
    def generate_response_with_history(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str = Config.SYSTEM_PROMPT
    ) -> str:
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": system_prompt}] + messages
        )
        return completion.choices[0].message.content

