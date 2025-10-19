from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from ai_bots.config import load_config
from ai_bots.logging_setup import configure_logging, get_logger
from ai_bots.rag.pipeline import RAGPipeline


app = FastAPI(title="AI Bots API", version="0.1.0")


class AskRequest(BaseModel):
    query: str


class AskResponse(BaseModel):
    answer: str


@app.on_event("startup")
def on_startup() -> None:
    cfg = load_config()
    configure_logging(cfg.log_level)
    log = get_logger("api")
    log.info("startup", environment=cfg.environment)


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask(body: AskRequest) -> AskResponse:
    cfg = load_config()

    pipeline = RAGPipeline(
        openai_api_key=cfg.openai_api_key,
        model=cfg.model,
        persist_dir=cfg.chroma_persist_dir,
    )

    store = pipeline.build_vector_store([
        "Acme Inc. returns policy: customers can return items within 30 days of purchase with receipt.",
        "Acme Inc. support hours are 9am-6pm Monday through Friday.",
        "Pricing for product X: $49 per seat per month, discounts available for annual billing.",
    ])

    chain = pipeline.build_qa_chain(store)
    answer = pipeline.ask(chain, body.query)
    return AskResponse(answer=answer)
