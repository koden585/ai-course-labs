# -*- coding: utf-8 -*-
import os
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


class VectorStoreManager:
    """Менеджер векторной базы ChromaDB."""

    def __init__(self, persist_directory="./data/chroma_db", collection_name="rag_documents"):
        os.makedirs(persist_directory, exist_ok=True)

        # Локальная модель векторизации
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
            model_kwargs={'device': 'cpu'}
        )

        self.vectorstore = Chroma(
            collection_name=collection_name,
            embedding_function=self.embeddings,
            persist_directory=persist_directory
        )

    def add_documents(self, chunks):
        self.vectorstore.add_documents(chunks)

    def search_with_scores(self, query, k=3):
        # Возвращает список кортежей (Document, score)
        results = self.vectorstore.similarity_search_with_score(query, k=k)
        formatted = []
        for doc, score in results:
            formatted.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
                "similarity_score": score
            })
        return formatted