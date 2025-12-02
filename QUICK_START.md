# Quick Start Guide

Get the Controls Theory QnA Chatbot running quickly.

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Set Up Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-actual-key-here
```

## Step 3: Prepare Data

Ensure these files are in the project root:
- `Task_Theory_Part_1.txt` (course content)
- `Code_QnA.xlsx` (code examples)

## Step 4: Build Vector Database

```bash
python scripts/build_database.py
```

This creates `data/Task_Theory_Part_1_DB.json`

## Step 5: Run the Chatbot

Choose your interface:

### Web Interface (Recommended)
```bash
python -m src.web.app
```
Visit `http://127.0.0.1:8007` in your browser

### Command Line
```bash
python scripts/interactive_chat.py
```

## Troubleshooting

**Import Error**: Make sure you're in the project root directory

**API Key Error**: Check that `.env` file exists and contains valid `OPENAI_API_KEY`

**Module Not Found**: Run `pip install -r requirements.txt`

**Database Error**: Ensure `data/Task_Theory_Part_1_DB.json` exists (run Step 4)

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) if migrating from old code
- Run evaluation: `python scripts/evaluate.py --test-file your_test.xlsx`

