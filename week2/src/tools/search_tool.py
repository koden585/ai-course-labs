# -*- coding: utf-8 -*-
"""
Инструмент поиска в интернете (исправлено под ZERO_SHOT_REACT_DESCRIPTION)
"""

from langchain.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)

class SearchInput(BaseModel):
    query: str = Field(description="Поисковый запрос", min_length=1, max_length=500)

class SearchTool(BaseTool):
    name = "search_web"
    description = """
    Поиск актуальной информации в интернете.
    Используй, когда нужно получить свежие данные, документацию или новости.
    """
    args_schema: Type[BaseModel] = SearchInput

    def _run(self, query: str) -> str:
        logger.info(f"Поиск: {query}")
        # Mock-данные (учебная версия)
        return f"🔎 Результаты поиска по запросу '{query}':\n" \
               f"1. YandexGPT 3.0 — сентябрь 2025\n" \
               f"2. Обновления LangChain 0.1.x — март 2026\n" \
               f"3. Актуальная документация по агентам 2026 года"

    async def _arun(self, query: str) -> str:
        return self._run(query)

    def to_langchain_tool(self) -> BaseTool:
        return self