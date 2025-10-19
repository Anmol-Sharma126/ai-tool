from __future__ import annotations

from typing import Iterable, List

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA


class RAGPipeline:
    def __init__(self, openai_api_key: str, model: str = "gpt-4o-mini", persist_dir: str | None = None):
        self.openai_api_key = openai_api_key
        self.model = model
        self.persist_dir = persist_dir

    def build_vector_store(self, texts: Iterable[str]) -> Chroma:
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        split_docs = []
        for t in texts:
            split_docs.extend(splitter.split_text(t))

        embeddings = OpenAIEmbeddings(api_key=self.openai_api_key)
        if self.persist_dir:
            vector_store = Chroma.from_texts(split_docs, embedding=embeddings, persist_directory=self.persist_dir)
        else:
            vector_store = Chroma.from_texts(split_docs, embedding=embeddings)
        return vector_store

    def build_qa_chain(self, vector_store: Chroma) -> RetrievalQA:
        llm = ChatOpenAI(model=self.model, api_key=self.openai_api_key, temperature=0.0)
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vector_store.as_retriever(),
        )
        return qa_chain

    def ask(self, qa_chain: RetrievalQA, query: str) -> str:
        """Ask a question using the provided QA chain.

        Uses invoke() for compatibility with modern LangChain runnables.
        Falls back to common result keys when a dict is returned.
        """
        result = qa_chain.invoke({"query": query})
        if isinstance(result, dict):
            for key in ("result", "output_text", "text", "answer"):
                if key in result and isinstance(result[key], str):
                    return result[key]
            return str(result)
        return str(result)
