"""
Simple retrieval-augmented assistant demo (Python).

Requirements:
- pip install langchain openai chromadb tiktoken
- Set OPENAI_API_KEY env var

This is a small demo showing:
- embedding a short set of documents (in-memory)
- building a Chroma vector store
- running a basic retrieval QA chain
"""

import os
from typing import List

from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.embeddings.fake import FakeEmbeddings
from langchain.llms.fake import FakeListLLM

def build_documents(texts: List[str]):
    docs = []
    for i, t in enumerate(texts):
        docs.append({"page_content": t, "metadata": {"id": str(i)}})
    return docs

def main():
    use_fake = os.environ.get("USE_FAKE") in ("1", "true", "True", "yes")
    api_key = os.environ.get("OPENAI_API_KEY")
    if not use_fake and not api_key:
        raise RuntimeError("Set OPENAI_API_KEY in your environment (or set USE_FAKE=1)")

    texts = [
        "Acme Inc. returns policy: customers can return items within 30 days of purchase with receipt.",
        "Acme Inc. support hours are 9am-6pm Monday through Friday.",
        "Pricing for product X: $49 per seat per month, discounts available for annual billing."
    ]

    # Split (small demo; not necessary for short texts)
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = []
    for t in texts:
        pages = splitter.split_text(t)
        split_docs.extend([{"page_content": p, "metadata": {}} for p in pages])

    # Embeddings + vector DB
    if use_fake:
        embeddings = FakeEmbeddings(size=1536)
    else:
        embeddings = OpenAIEmbeddings(openai_api_key=api_key)

    chroma_db = Chroma.from_texts([d["page_content"] for d in split_docs], embedding=embeddings)

    # LLM
    if use_fake:
        # Return deterministic answers for the three demo queries below
        llm = FakeListLLM(responses=[
            "Customers can return items within 30 days of purchase with receipt.",
            "Support is available 9am-6pm Monday through Friday.",
            "Product X costs $49 per seat per month; annual discounts available.",
        ])
    else:
        llm = OpenAI(openai_api_key=api_key, temperature=0.0)

    # Retrieval QA chain
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=chroma_db.as_retriever())

    # Example queries
    queries = [
        "What is the return window for Acme Inc.?",
        "When is support available?",
        "How much does product X cost?"
    ]

    for q in queries:
        print("Q:", q)
        ans = qa.run(q)
        print("A:", ans)
        print("------")

if __name__ == "__main__":
    main()