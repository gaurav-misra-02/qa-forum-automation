import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Config:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    if not OPENAI_API_KEY:
        raise ValueError(
            "OPENAI_API_KEY environment variable is not set. "
            "Please create a .env file based on .env.example"
        )
    
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')
    LLM_MODEL = os.getenv('LLM_MODEL', 'gpt-3.5-turbo')
    
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / 'data'
    
    TOP_K = int(os.getenv('TOP_K', '3'))
    CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', '384'))
    
    FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_HOST = os.getenv('FLASK_HOST', '127.0.0.1')
    FLASK_PORT = int(os.getenv('FLASK_PORT', '8007'))
    
    SYSTEM_PROMPT = (
        "You are a chatbot designed to help a novice in the domain of "
        "Control Theory pertaining to Robotics."
    )
    
    INSTRUCTION_TEMPLATE = (
        "Please include at least one relevant example in your response. "
        "Additionally, please structure your response in the following format: "
        "a) Theory \nb)Mathematical Example. "
        "Also, please try and keep your responses short."
    )
    
    SUMMARIZATION_PROMPT = (
        "You are a chatbot designed to help a novice in the domain of "
        "Control Theory pertaining to Robotics. You are meant to summarize "
        "a series of question-answer pairs in brief."
    )
    
    SUMMARIZE_EVERY_N_TURNS = 5

