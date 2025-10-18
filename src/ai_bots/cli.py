from __future__ import annotations

import argparse
import sys

from ai_bots.config import load_config
from ai_bots.logging_setup import configure_logging, get_logger
from ai_bots.rag.pipeline import RAGPipeline


EXAMPLE_TEXTS = [
    "Acme Inc. returns policy: customers can return items within 30 days of purchase with receipt.",
    "Acme Inc. support hours are 9am-6pm Monday through Friday.",
    "Pricing for product X: $49 per seat per month, discounts available for annual billing.",
]


def main() -> int:
    parser = argparse.ArgumentParser(prog="ai-bots", description="AI bots and automation CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ingest = subparsers.add_parser("ingest", help="Ingest and embed example texts")
    ingest.add_argument("--persist", action="store_true", help="Persist the vector store to disk")

    ask = subparsers.add_parser("ask", help="Ask a question against embedded docs")
    ask.add_argument("query", help="The user question to ask")

    args = parser.parse_args()

    config = load_config()
    configure_logging(config.log_level)
    log = get_logger("cli")

    pipeline = RAGPipeline(
        openai_api_key=config.openai_api_key,
        model=config.model,
        persist_dir=config.chroma_persist_dir if args.command == "ingest" and args.persist else None,
    )

    if args.command == "ingest":
        log.info("build_vector_store.start", persist=bool(args.persist))
        store = pipeline.build_vector_store(EXAMPLE_TEXTS)
        # Persist if requested
        if args.persist and config.chroma_persist_dir:
            store.persist()
        log.info("build_vector_store.success")
        return 0

    if args.command == "ask":
        log.info("qa.ask.start", query=args.query)
        store = pipeline.build_vector_store(EXAMPLE_TEXTS)
        chain = pipeline.build_qa_chain(store)
        answer = pipeline.ask(chain, args.query)
        print(answer)
        log.info("qa.ask.success")
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
