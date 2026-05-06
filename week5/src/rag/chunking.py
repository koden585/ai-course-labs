# -*- coding: utf-8 -*-
from langchain_text_splitters import RecursiveCharacterTextSplitter

class ChunkingStrategy:
    """Разбиение текста на чанки."""
    @staticmethod
    def split_documents(documents, chunk_size=512, chunk_overlap=50):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        return splitter.split_documents(documents)