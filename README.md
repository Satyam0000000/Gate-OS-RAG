# GATE OS RAG

An AI-powered Retrieval-Augmented Generation (RAG) application for answering Operating Systems questions from course material.

The system retrieves relevant textbook chunks from Qdrant, reranks them using a cross-encoder model, and generates grounded answers with source references.

## Features

- Ask natural-language Operating Systems questions
- Semantic vector search with Qdrant
- OpenAI embeddings using `text-embedding-3-small`
- Cross-encoder reranking with `ms-marco-MiniLM-L-6-v2`
- OpenAI-generated answers
- Source section and PDF-page references
- React + Vite frontend
- FastAPI backend
- Retrieval evaluation using Recall@K

## Tech Stack

- Frontend: React, TypeScript, Vite, Tailwind CSS, shadcn/ui
- Backend: FastAPI, Python
- Vector Database: Qdrant
- Embeddings and Generation: OpenAI API
- Reranking: Sentence Transformers CrossEncoder

## Project Structure

```text
os-scholar-rag/
├── backend/                 # FastAPI API and retrieval logic
│   ├── main.py
│   ├── retriever.py
│   └── generator.py
├── ingestion/               # Scripts to chunk, embed, and index documents
├── eval/                    # Retrieval evaluation scripts
├── frontend/                # React + Vite user interface
├── data/                    # Local source documents (not committed)
├── requirements.txt         # Python dependencies
└── .env                     # Local secrets (not committed)
```

## Prerequisites

Install:

- Python 3.10 or later
- Node.js 18 or later
- npm
- Docker Desktop (recommended for local Qdrant)
- An OpenAI API key

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/os-scholar-rag.git
cd os-scholar-rag
```

### 2. Create and activate a Python environment

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` has not yet been generated:

```bash
python -m pip freeze > requirements.txt
```

### 4. Install frontend dependencies

```bash
cd frontend
npm install
cd ..
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=http://localhost:6333
```

Never commit `.env` or API keys to GitHub.

### 6. Start Qdrant locally

Using Docker:

```bash
docker run -p 6333:6333 -p 6334:6334 \
  -v "$(pwd)/qdrant_storage:/qdrant/storage" \
  qdrant/qdrant
```

Qdrant will be available at:

```text
http://localhost:6333
```

### 7. Index your course material

Place your permitted source documents inside `data/`, then run your ingestion script:

```bash
python ingestion/YOUR_INGESTION_SCRIPT.py
```

This creates the `gate_os` collection and uploads chunks, embeddings, and page metadata to Qdrant.

> Do not commit copyrighted textbook PDFs or other material you do not have permission to distribute.

## Run the Application

### Start the backend

From the project root:

```bash
source venv/bin/activate
cd backend
uvicorn main:app --reload --port 8000
```

Backend URL:

```text
http://localhost:8000
```

Health check:

```text
http://localhost:8000/health
```

### Start the frontend

Open a second terminal:

```bash
cd frontend
npm run dev
```

Open:

```text
http://localhost:5173
```

## API

### `POST /query`

Request:

```json
{
  "query": "What is the difference between preemptive and non-preemptive scheduling?"
}
```

Response:

```json
{
  "answer": "…",
  "sources": [
    {
      "section": "CPU Scheduling",
      "page": 205
    }
  ]
}
```

## Evaluation

Run the retrieval evaluation from the project root:

```bash
python -m eval.eval_retrieval
```

The evaluation measures whether the correct source page appears among the top retrieved results.

## Security

The following files and directories must remain untracked:

```gitignore
.env
venv/
qdrant_storage/
__pycache__/
*.pyc
frontend/node_modules/
```

## Future Improvements

- Page-level result deduplication
- Hybrid search with keyword and semantic retrieval
- Better retrieval benchmark dataset
- Dockerized deployment
- Rate limiting and API-cost protection
- Deployable demo using Qdrant Cloud


## Author

Satyam Goswami