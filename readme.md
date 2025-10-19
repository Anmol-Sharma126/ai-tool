## AI Bots — Production-Ready RAG and Automation

A production-grade Python package for building AI-powered assistants: retrieval-augmented generation (RAG), a FastAPI service, and a CLI. Comes with config management, structured logging, tests, linters, Docker, and CI.

### Features
- Modular RAG pipeline using LangChain and Chroma
- FastAPI service with health check and Ask endpoint
- CLI for ingest and question answering
- Environment-based config via `.env`
- Structured JSON logging (structlog)
- Tests (pytest), type checks (mypy), lint/format (ruff, black)
- Dockerfile and GitHub Actions CI

### Quick start (local)
1) Create virtualenv and install dev deps:
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .[dev]
```
2) Configure environment:
```bash
cp .env.example .env
# Edit .env to set OPENAI_API_KEY
```
3) Run the API:
```bash
make run-api
# -> http://localhost:8000/healthz
```
4) Use the CLI:
```bash
make cli-ingest
make cli-ask
```

### Configuration
Set values in `.env` or environment variables:
- `OPENAI_API_KEY` (required)
- `OPENAI_MODEL` (default: gpt-4o-mini)
- `CHROMA_PERSIST_DIR` (optional persist dir)
- `APP_ENV` (default: development)
- `LOG_LEVEL` (default: INFO)

### Development
```bash
make dev          # install dev dependencies
make lint         # ruff checks
make format       # ruff format + black
make type         # mypy
make test         # pytest
```

### Docker
```bash
docker build -t ai-bots:local .
docker run --rm -p 8000:8000 -e OPENAI_API_KEY=$OPENAI_API_KEY ai-bots:local
```

### Repository layout
- `src/ai_bots` – package code (`config.py`, `logging_setup.py`, `rag/`, `api/`, `cli.py`)
- `tests/` – unit tests for CLI and API
- `.github/workflows/ci.yml` – CI pipeline
- `Dockerfile` – production container image
- `.env.example` – config template

### Migration note
The original demo script `src_simple_bot_Version2.py` has been superseded by the package. Use `ai-bots` CLI or the FastAPI service instead.
