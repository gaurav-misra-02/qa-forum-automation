# Control Theory Educational Chatbot

An intelligent chatbot system powered by Retrieval-Augmented Generation (RAG) to assist students learning Controls Theory in Robotics. The system combines semantic search over educational content with OpenAI's GPT-3.5 to provide accurate, contextually-aware responses.

## Overview

This system implements a RAG-based approach for educational Q&A in Control Theory. It processes student questions by:

1. Retrieving relevant content from a vector database of course materials
2. Augmenting the query with retrieved context
3. Generating responses using GPT-3.5 with structured formatting
4. Maintaining conversation history with automatic summarization

## Features

- **Semantic Search**: Finds relevant content using sentence transformers and cosine similarity
- **Structured Responses**: Formats answers as Theory + Mathematical Examples
- **Conversation Management**: Maintains session history with automatic summarization every 5 turns
- **Web Interface**: Modern, responsive chat UI with feedback mechanisms
- **Evaluation Framework**: Comprehensive metrics using BLEU, ROUGE, and Google BLEU
- **Modular Architecture**: Clean separation of concerns for easy maintenance and extension

## Architecture

```
User Query → Retriever (Semantic Search) → Context + Query → LLM → Structured Response
                ↓
         Vector Database
         (Course Material)
```

**Components:**
- **Vector Database**: Embedded course content with code examples
- **Retriever**: Semantic search using sentence transformers
- **LLM Client**: OpenAI GPT-3.5 integration
- **Chat Session**: Conversation state management
- **Web Interface**: Flask-based UI

## Impact & Results

**This section highlights the measurable outcomes and effectiveness of the chatbot system based on empirical evaluation with MOOC learners and graduate students.**

### Learning Performance Improvements
Deployed across two MOOC cohorts with 183 total learners, the system demonstrated significant educational impact:
- **15.8% increase** in post-test problem-solving accuracy compared to traditional discussion forums
- Students using the chatbot (n=91) outperformed forum-based learners (n=92) on multi-step control theory tasks
- Most learner problems resolved within **2-4 conversational turns**, indicating efficient problem resolution

### Cognitive Load Reduction
Evaluated via NASA Task Load Index (NASA-TLX) with 19 graduate students during 30-minute tutoring sessions:
- **Mental Demand**: Mean score of 34.8 (reduced compared to Q&A-based learning)
- **Frustration**: Mean score of 31.5 (lower than baseline)
- Structured explanations and multimodal output (theory + mathematical examples) helped reduce cognitive burden
- Lower perceived workload correlated with better performance on follow-up tasks

### Usability & User Satisfaction
System usability assessed via the System Usability Scale (SUS):
- **SUS Score: 76.58** (indicating strong usability above industry average of 68)
- Learners appreciated multi-step explanations and response adaptability
- Responses rated as more complete and relevant compared to peer discussion forum replies
- High satisfaction reported for clarity and instructional helpfulness

---

## Installation

### Prerequisites
- Python 3.8 or higher
- OpenAI API key

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd qa-forum-automation
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your_actual_api_key_here
```

4. Prepare data directory:
```bash
mkdir -p data
```

Move your course materials to the project root:
- `Task_Theory_Part_1.txt` - Course content
- `Code_QnA.xlsx` - Code examples

## Usage

### Building the Knowledge Base

Before using the chatbot, create the vector database from your course materials:

```bash
python scripts/build_database.py
```

With custom paths:
```bash
python scripts/build_database.py \
  --input path/to/your/content.txt \
  --code-examples path/to/code_examples.xlsx \
  --output data/vector_db.json
```

### Running the Web Interface

Start the Flask web application:

```bash
python -m src.web.app
```

The chatbot will be available at `http://127.0.0.1:8007`

To use a different port:
```bash
# Edit .env file
FLASK_PORT=5000
```

### Command Line Interface

For interactive terminal sessions:

```bash
python scripts/interactive_chat.py
```

Enter questions and receive responses. Type `8465` to exit.

### Evaluation

Evaluate the chatbot against test questions:

```bash
python scripts/evaluate.py --test-file path/to/test_questions.xlsx
```

Results will be saved to `results.json` by default. Customize output location:

```bash
python scripts/evaluate.py \
  --test-file test_data.xlsx \
  --output evaluation_results.json
```

## Configuration

Key settings in `.env`:

```bash
OPENAI_API_KEY=your_key_here
EMBEDDING_MODEL=all-MiniLM-L6-v2
LLM_MODEL=gpt-3.5-turbo
TOP_K=3
CHUNK_SIZE=384
FLASK_HOST=127.0.0.1
FLASK_PORT=8007
```

Additional configuration options are available in `src/config.py`.

## Project Structure

```
qa-forum-automation/
├── src/
│   ├── config.py              # Configuration management
│   ├── database/
│   │   ├── vector_db.py       # Vector database creation
│   │   └── retriever.py       # Semantic search
│   ├── llm/
│   │   └── client.py          # OpenAI client wrapper
│   ├── chat/
│   │   └── session.py         # Session management
│   └── web/
│       ├── app.py             # Flask application
│       └── templates/
│           └── chat.html      # Web interface
├── scripts/
│   ├── build_database.py      # Database creation script
│   ├── interactive_chat.py    # CLI interface
│   └── evaluate.py            # Evaluation script
├── data/                      # Vector database storage
├── .env.example               # Environment template
├── requirements.txt
└── README.md
```

## Technology Stack

- **Web Framework**: Flask
- **LLM**: OpenAI GPT-3.5 Turbo
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Search**: Cosine similarity on dense vectors
- **Evaluation**: Hugging Face Evaluate (BLEU, ROUGE, Google BLEU)
- **Data Processing**: Pandas, NumPy

## Evaluation Metrics

The system uses three complementary metrics:

- **BLEU**: Measures n-gram overlap between generated and reference responses
- **ROUGE**: Focuses on recall of n-grams and longest common sequences
- **Google BLEU**: Variant of BLEU designed for sentence-level evaluation

## Development

### Adding New Course Material

1. Update your content files (`Task_Theory_Part_1.txt`, `Code_QnA.xlsx`)
2. Rebuild the vector database:
```bash
python scripts/build_database.py
```

### Customizing Response Format

Edit the instruction template in `src/config.py`:
```python
INSTRUCTION_TEMPLATE = "Your custom instructions here"
```

### Adjusting Retrieval

Modify `TOP_K` in `.env` to retrieve more or fewer context chunks:
```bash
TOP_K=5  # Retrieve top 5 most relevant chunks
```

## Security Notes

- Never commit `.env` file or API keys to version control
- API keys are loaded from environment variables only
- Use `.env.example` as a template for configuration

## License

[Add your license here]

## Citation

If you use this work in your research, please cite:

```
[Add citation information if applicable]
```

## Acknowledgments

Built for educational purposes to assist students learning Control Theory in Robotics.

