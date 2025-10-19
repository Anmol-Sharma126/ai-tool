PY=python
PIP=pip
PACKAGE=ai_bots

.PHONY: help install dev lint format type test run-api cli-ingest cli-ask pre-commit

help:
	@echo "Targets: install, dev, lint, format, type, test, run-api, cli-ingest, cli-ask, pre-commit"

install:
	$(PIP) install -e .

dev:
	$(PIP) install -e .[dev]

lint:
	ruff check .

format:
	ruff format .
	black .

type:
	mypy src

test:
	pytest -q

run-api:
	uvicorn $(PACKAGE).api.server:app --host 0.0.0.0 --port 8000 --reload

cli-ingest:
	$(PY) -m $(PACKAGE).cli ingest --persist

cli-ask:
	$(PY) -m $(PACKAGE).cli ask "What is the return window?"

pre-commit:
	pre-commit install && pre-commit run --all-files
