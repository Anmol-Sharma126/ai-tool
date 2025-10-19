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

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.messages import SystemMessage, HumanMessage


def main() -> None:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Set OPENAI_API_KEY in your environment")

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
    embeddings = OpenAIEmbeddings(api_key=api_key)
    vector_store = Chroma.from_texts(texts=split_texts, embedding=embeddings)

    # LLM
    llm = ChatOpenAI(api_key=api_key, model="gpt-4o-mini", temperature=0.0)

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