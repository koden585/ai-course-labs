# -*- coding: utf-8 -*-
"""
Специализированный инструмент для дипломной работы
Тема: Информационная система распознавания технических данных с графических материалов
"""

from langchain.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)

class CustomToolInput(BaseModel):
    drawing_description: str = Field(
        description="Текстовое описание чертежа/схемы (например: 'вал диаметром 50 мм из стали 45, длина 200 мм')",
        min_length=5
    )

class CustomTool(BaseTool):
    name = "extract_technical_params"
    description = """
    Инструмент распознавания технических данных с графических материалов.
    Принимает описание чертежа и возвращает структурированные параметры:
    размеры, материал, допуски, тип детали и т.д.
    Используй для анализа чертежей в рамках дипломной работы.
    """

    args_schema: Type[BaseModel] = CustomToolInput

    def _run(self, drawing_description: str) -> str:
        logger.info(f"Распознавание чертежа: {drawing_description[:100]}...")
        
        # Mock-реализация (для лабораторной). Позже можно подключить настоящую модель распознавания.
        return f"""
🔧 Распознанные технические параметры:
• Деталь: Вал / Цилиндр
• Диаметр: 50 мм
• Длина: 200 мм
• Материал: Сталь 45
• Допуск: h7
• Шероховатость: Ra 1.6
• Примечание: Соответствует ГОСТ 8732-78

(Это mock. В реальной дипломной работе здесь будет вызов нейросети или OCR-модели)
        """

    async def _arun(self, drawing_description: str) -> str:
        return self._run(drawing_description)

    def to_langchain_tool(self) -> BaseTool:
        return self