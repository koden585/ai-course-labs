# -*- coding: utf-8 -*-
import logging
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredMarkdownLoader

logger = logging.getLogger(__name__)


class DocumentLoader:
    """Загрузчик документов из директории."""

    def __init__(self, source_directory: str):
        self.source_directory = Path(source_directory)
        self.supported_extensions = ['.pdf', '.txt', '.md']

    def load_document(self, file_path: str):
        path = Path(file_path)
        ext = path.suffix.lower()

        if ext == '.pdf':
            loader = PyPDFLoader(str(path))
        elif ext == '.txt':
            loader = TextLoader(str(path), encoding='utf-8')
        elif ext == '.md':
            loader = UnstructuredMarkdownLoader(str(path))
        else:
            raise ValueError(f"Неподдерживаемый формат: {ext}")

        docs = loader.load()
        for doc in docs:
            doc.metadata['source'] = str(path.name)
        return docs

    def load_directory(self):
        all_documents = []
        for ext in self.supported_extensions:
            for file_path in self.source_directory.glob(f"**/*{ext}"):
                all_documents.extend(self.load_document(str(file_path)))
        return all_documents