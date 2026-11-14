# KeyStone — Agentic Tax Research Assistant

KeyStone answers US tax questions (e.g. *"Can I deduct a home office as a W-2 employee?"*) using only a corpus of IRS documents. It retrieves relevant passages, reasons over them with a LangGraph agent, and returns an answer with inline citations. When the documents don't support an answer, it refuses.

> **Status:** Phase 1 of 8 — project scaffold and health check.

## Tech stack

| Layer | Choice |
|---|---|
| Language | Python 3.11 |
| API | FastAPI + Uvicorn |
| Agent | LangGraph |
| LLM / embeddings | OpenAI `gpt-4o-mini` / `text-embedding-3-small` |
| Vector store | Chroma (local, persistent) |
| Validation | Pydantic v2 |
| Tests & evals | pytest |
| Frontend | React + TypeScript |

## Architecture

_TODO (Phase 8): request flow from question → retrieval → agent → cited answer._

## Project structure

```
keystone/
├── keystone/            # Python package
│   ├── main.py          # FastAPI app factory + entry point
│   ├── config.py        # Settings loaded from .env
│   ├── schemas.py       # Pydantic models for API inputs/outputs
│   └── api/             # One router module per endpoint group
├── tests/               # pytest unit tests
├── data/
│   ├── raw/             # Source tax documents (not committed)
│   └── chroma/          # Generated vector DB (not committed)
├── .env.example         # Template for secrets/config
└── requirements.txt
```

## Setup (Windows / PowerShell)

```powershell
cd C:\Users\tarun\source\keystone
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env   # then put your OpenAI key in .env
```

## Running

```powershell
uvicorn keystone.main:app --reload
```

- Health check: http://127.0.0.1:8000/health
- Interactive API docs: http://127.0.0.1:8000/docs

## Testing

```powershell
pytest
```

## Data sources

_TODO (Phase 2): list of IRS publications in the corpus, with download links._

## Evaluation results

_TODO (Phase 6): retrieval hit rate, answer accuracy, hallucination rate, refusal correctness._

## Roadmap

- [x] Phase 1 — Scaffold + health check
- [ ] Phase 2 — Ingestion pipeline (chunk → embed → Chroma)
- [ ] Phase 3 — Retrieval + `/retrieve` endpoint
- [ ] Phase 4 — LangGraph agent + `/ask` endpoint
- [ ] Phase 5 — Guardrails (refusal, citations, uncertainty)
- [ ] Phase 6 — Evaluation harness
- [ ] Phase 7 — React + TypeScript frontend
- [ ] Phase 8 — Documentation
