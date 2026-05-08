# -*- coding: utf-8 -*-
import os
import sys

# Определяем точные абсолютные пути, чтобы не было путаницы
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(BASE_DIR, "src"))

from dotenv import load_dotenv
from langchain_community.llms import YandexGPT
from langchain.prompts import ChatPromptTemplate
from rag.document_loader import DocumentLoader
from rag.chunking import ChunkingStrategy
from rag.vector_store import VectorStoreManager
from rag.rag_pipeline import RAGPipeline


class VideoSurveillanceRAG(RAGPipeline):
    def __init__(self, vectorstore, llm, top_k=3):
        super().__init__(vectorstore, llm, top_k)
        self.prompt_template = ChatPromptTemplate.from_template("""
Ты - главный инженер системы интеллектуального видеомониторинга.
Ответь на вопрос оператора, используя СТРОГО только предоставленные выдержки из регламента.
Если в тексте нет ответа, скажи "Согласно регламенту, информации об этом нет".

Текст регламента:
{context}

Вопрос оператора: {question}
Ответ:""")


def main():
    # Загружаем ключи по абсолютному пути
    load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))

    docs_dir = os.path.join(BASE_DIR, "data", "documents")
    chroma_dir = os.path.join(BASE_DIR, "data", "chroma_db")

    print(f"1. Загрузка документов из папки {docs_dir}...")
    loader = DocumentLoader(source_directory=docs_dir)
    docs = loader.load_directory()

    if not docs:
        print(
            "\n❌ ОШИБКА: Документы не найдены! Убедитесь, что вы создали файл week5/data/documents/video_surveillance.txt")
        return

    print("2. Разбиение текста на чанки...")
    chunks = ChunkingStrategy.split_documents(docs, chunk_size=512, chunk_overlap=50)

    print(f"3. Индексация {len(chunks)} чанков в базу ChromaDB...")
    vectorstore = VectorStoreManager(persist_directory=chroma_dir)
    vectorstore.add_documents(chunks)

    print("4. Подключение к YandexGPT...")
    llm = YandexGPT(
        iam_token=os.getenv("YANDEX_IAM_TOKEN"),
        folder_id=os.getenv("YANDEX_FOLDER_ID"),
        max_tokens=500,
        temperature=0.1
    )

    rag = VideoSurveillanceRAG(vectorstore=vectorstore, llm=llm, top_k=3)

    questions = [
        "Что делать, если в зоне Б (Парковка) машина стоит 2 дня?",
        "Можно ли людям находиться в Зоне А ночью?",
        "Как система распознает номера машин?"
    ]

    print("\n" + "=" * 50)
    print("ТЕСТИРОВАНИЕ RAG: СИСТЕМА ИНТЕЛЛЕКТУАЛЬНОГО ВИДЕОМОНИТОРИНГА")
    print("=" * 50)

    for q in questions:
        print(f"\n❓ ВОПРОС: {q}")
        res = rag.query(q)
        print(f"🤖 ОТВЕТ: {res['answer']}")
        print(f"   (Источников использовано: {len(res['sources'])}, Время: {res['execution_time']}с)")


if __name__ == "__main__":
    main()