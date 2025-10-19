"""
Simple retrieval-augmented assistant demo (Python).

Requirements:
- Create a venv and install dependencies from requirements.txt
- Set OPENAI_API_KEY environment variable

This demo shows:
- embedding a short set of documents (in-memory)
- building a Chroma vector store
- running a basic retrieval QA chain
"""

import os

from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.embeddings.fake import FakeEmbeddings
from langchain.llms.fake import FakeListLLM


def main():
    use_fake = os.environ.get("USE_FAKE") in ("1", "true", "True", "yes")
    api_key = os.environ.get("OPENAI_API_KEY")
    if not use_fake and not api_key:
        raise RuntimeError("Set OPENAI_API_KEY in your environment (or set USE_FAKE=1)")

    seed_texts = [
        "Acme Inc. returns policy: customers can return items within 30 days of purchase with receipt.",
        "Acme Inc. support hours are 9am-6pm Monday through Friday.",
        "Pricing for product X: $49 per seat per month, discounts available for annual billing.",
    ]

    # Split (small demo; not necessary for short texts, but included for realism)
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_texts = []
    for text in seed_texts:
        split_texts.extend(splitter.split_text(text))

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

    # Retriever
    retriever = vector_store.as_retriever()

    # Example queries
    queries = [
        "What is the return window for Acme Inc.?",
        "When is support available?",
        "How much does product X cost?",
    ]

    for query in queries:
        print("Q:", query)
        docs = retriever.get_relevant_documents(query)
        context = "\n\n".join(d.page_content for d in docs)
        messages = [
            SystemMessage(
                content=(
                    "You are a helpful assistant. Answer using only the provided context."
                )
            ),
            HumanMessage(content=f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"),
        ]
        response = llm.invoke(messages)
        print("A:", response.content)
        print("------")


if __name__ == "__main__":
    main()