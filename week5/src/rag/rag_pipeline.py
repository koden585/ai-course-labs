# -*- coding: utf-8 -*-
import time
from langchain.prompts import ChatPromptTemplate


class RAGPipeline:
    def __init__(self, vectorstore, llm, top_k=3):
        self.vectorstore = vectorstore
        self.llm = llm
        self.top_k = top_k
        self.prompt_template = ChatPromptTemplate.from_template("""
Ты — ИИ-помощник. Используй ТОЛЬКО следующий контекст для ответа на вопрос.
Контекст:
{context}

Вопрос: {question}
Ответ:""")

    def query(self, question: str):
        start_time = time.time()
        search_results = self.vectorstore.search_with_scores(question, k=self.top_k)

        if not search_results:
            return {"answer": "Нет релевантных документов.", "sources": []}

        # Собираем найденный текст в одну строку
        context_text = "\n\n".join(
            [f"Источник: {res['metadata'].get('source')}\n{res['content']}" for res in search_results])
        prompt = self.prompt_template.format(context=context_text, question=question)

        try:
            response = self.llm.invoke(prompt)
            # В зависимости от ответа (строка или объект Message)
            answer = response if isinstance(response, str) else response.content
        except Exception as e:
            answer = f"Ошибка генерации: {e}"

        return {
            "question": question,
            "answer": answer,
            "sources": search_results,
            "execution_time": round(time.time() - start_time, 2)
        }