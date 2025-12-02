# Migration Guide

This document explains the refactoring changes and how to migrate from the old codebase structure to the new one.

## Overview of Changes

The codebase has been restructured for better maintainability, security, and usability:

1. **Security**: API keys moved to environment variables
2. **Structure**: Code organized into logical modules
3. **Naming**: Following Python conventions (PEP 8)
4. **Type Safety**: Type hints added throughout
5. **Configuration**: Centralized in `src/config.py`

## File Mapping

### Old → New Structure

| Old File | New Location | Changes |
|----------|-------------|---------|
| `make_vectordb.py` | `src/database/vector_db.py` | Renamed class, added type hints, extracted chunking function |
| `make_prompt.py` | `src/database/retriever.py` | Created `Retriever` class, snake_case naming |
| `gen_ans.py` | `src/llm/client.py` | Consolidated into `LLMClient` class |
| `interact.py` | `scripts/interactive_chat.py` | Uses new `ChatSession` class |
| `once_interact.py` | `src/chat/session.py` | Refactored into `ChatSession` and `single_turn_interaction` |
| `main_1_sessions.py` | `src/web/app.py` | Separated template, fixed bugs, cleaner routes |
| `test.py` | `scripts/evaluate.py` | Added CLI args, better structure |

## Key API Changes

### Vector Database Creation

**Old:**
```python
from make_vectordb import Make_Retrieval_Database

retrievedb = Make_Retrieval_Database(contexts, save_file, code_filepath)
retrievedb.createDatabase()
```

**New:**
```python
from src.database.vector_db import VectorDatabase

vector_db = VectorDatabase(contexts, save_file, code_filepath)
vector_db.create_database()
```

### Semantic Search

**Old:**
```python
from make_prompt import searchVectorDb

new_prompt = searchVectorDb(prompt, contexts)
```

**New:**
```python
from src.database.retriever import Retriever

retriever = Retriever(contexts)
new_prompt = retriever.build_prompt(prompt)
```

### Response Generation

**Old:**
```python
from openai import OpenAI

client = OpenAI(api_key="sk-...")
completion = client.chat.completions.create(...)
```

**New:**
```python
from src.llm.client import LLMClient

client = LLMClient()  # API key from environment
response = client.generate_response(prompt)
```

### Chat Sessions

**Old:**
```python
from once_interact import interactions

response, history = interactions(user_input, contexts, instruction, history, call_no)
```

**New:**
```python
from src.chat.session import ChatSession

session = ChatSession(contexts)
response = session.process_query(user_input)
```

## Configuration Changes

### Old Approach
Constants scattered across files:
- `TOP_K = 3` in make_prompt.py
- `LIMIT = 384` in make_vectordb.py
- API keys hardcoded in multiple files

### New Approach
Centralized in `src/config.py` and `.env`:

```python
from src.config import Config

top_k = Config.TOP_K
model = Config.EMBEDDING_MODEL
api_key = Config.OPENAI_API_KEY  # from environment
```

## Environment Setup

1. Copy `.env.example` to `.env`
2. Add your API key to `.env`
3. Never commit `.env` to version control

## Running Scripts

### Old Commands
```bash
python make_vectordb.py
python interact.py
python main_1_sessions.py
python test.py
```

### New Commands
```bash
python scripts/build_database.py
python scripts/interactive_chat.py
python -m src.web.app
python scripts/evaluate.py --test-file path/to/file.xlsx
```

## Breaking Changes

1. **API Keys**: Must be set in environment variables (no hardcoded keys)
2. **Import Paths**: All imports updated to use `src.*` module structure
3. **Function Names**: Now follow snake_case convention
4. **Class Names**: Now follow PascalCase convention
5. **CLI Scripts**: Now accept command-line arguments

## Backward Compatibility

Old files are preserved in `old_code/` directory for reference. However, they will not work without modification due to:
- Hardcoded (revoked) API keys
- Old import structure
- Missing dependencies on new modules

## Testing Your Migration

1. Build the database:
```bash
python scripts/build_database.py
```

2. Test web interface:
```bash
python -m src.web.app
```

3. Test CLI:
```bash
python scripts/interactive_chat.py
```

If you encounter import errors, ensure you're running Python from the project root directory.

## Benefits of New Structure

1. **Security**: No accidental API key commits
2. **Maintainability**: Clear module boundaries
3. **Testability**: Functions are easier to unit test
4. **Extensibility**: Easy to add new features
5. **Documentation**: Type hints improve IDE support
6. **Deployment**: Cleaner structure for production

## Questions?

Refer to the main README.md for full documentation on the new structure.

