# -*- coding: utf-8 -*-
"""
Ядро AI-агента с поддержкой инструментов и памяти
Лабораторная работа №2

Дисциплина: Искусственный интеллект
Автор: [ТВОЁ ФИО]
Группа: [ТВОЯ ГРУППА]
Дата: 2026
"""

import sys
from pathlib import Path

# ←←←←← ЭТО ИСПРАВЛЕНИЕ ПУТЕЙ ←←←←←
sys.path.insert(0, str(Path(__file__).parent.parent))
# =====================================

import os
import logging
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import time

from langchain.agents import initialize_agent, AgentType, Tool
from langchain.memory import ConversationBufferMemory
from langchain_community.llms import YandexGPT

# Локальные импорты (будем создавать дальше)
from src.tools.search_tool import SearchTool
from src.tools.calc_tool import CalculateTool
from src.tools.custom_tool import CustomTool
from src.memory.working_memory import WorkingMemory
from src.memory.semantic_memory import SemanticMemory
from src.guardrails.input_validator import InputGuardrails

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agent.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class AgentConfig:
    name: str = "TechnicalDataRecognizer"
    version: str = "2.0"
    max_iterations: int = 20
    temperature: float = 0.7
    memory_enabled: bool = True
    guardrails_enabled: bool = True
    verbose: bool = True


@dataclass
class AgentResponse:
    success: bool
    answer: str
    steps: List[Dict]
    duration_ms: int
    tokens_used: int
    error: Optional[str] = None


class AIAgent:
    """
    Основной класс агента для твоей дипломной темы:
    «Информационная система распознавания технических данных с графических материалов»
    """

    def __init__(self, config: Optional[AgentConfig] = None):
        self.config = config or AgentConfig()
        logger.info(f"🚀 Инициализация агента: {self.config.name} v{self.config.version}")

        # LLM (YandexGPT — использует твои токены из .env)
        self.llm = self._init_llm()

        # Инструменты
        self.tools = self._init_tools()

        # Память
        self.working_memory = WorkingMemory() if self.config.memory_enabled else None
        self.semantic_memory = SemanticMemory() if self.config.memory_enabled else None

        # Guardrails
        self.guardrails = InputGuardrails() if self.config.guardrails_enabled else None

        # LangChain агент (ReAct)
        self.agent = self._init_agent()

        self.request_count = 0
        self.total_tokens = 0
        logger.info("✅ Агент полностью готов к работе!")

    def _init_llm(self):
        iam_token = os.getenv("YANDEX_IAM_TOKEN")
        folder_id = os.getenv("YANDEX_FOLDER_ID")

        if not iam_token or not folder_id:
            raise ValueError("❌ Не найдены YANDEX_IAM_TOKEN или YANDEX_FOLDER_ID в .env")

        return YandexGPT(
            iam_token=iam_token,
            folder_id=folder_id,
            temperature=self.config.temperature,
            max_tokens=1200
        )

    def _init_tools(self) -> List[Tool]:
        return [
            SearchTool().to_langchain_tool(),
            CalculateTool().to_langchain_tool(),
            CustomTool().to_langchain_tool(),   # ← адаптирован под твою дипломную тему
        ]

    def _init_agent(self):
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            max_token_limit=4000
        ) if self.working_memory else None

        return initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            memory=memory,
            verbose=self.config.verbose,
            max_iterations=self.config.max_iterations,
            handle_parsing_errors=True
        )

    def run(self, query: str, session_id: Optional[str] = None) -> AgentResponse:
        start_time = time.time()
        session_id = session_id or f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Guardrails
        if self.guardrails:
            check = self.guardrails.validate_input(query)
            if not check.is_safe:
                return AgentResponse(
                    success=False,
                    answer="Запрос отклонён системой безопасности.",
                    steps=[],
                    duration_ms=0,
                    tokens_used=0,
                    error=check.reason
                )

        try:
            result = self.agent.run(query)

            # Сохраняем в память
            if self.working_memory:
                self.working_memory.add_message("user", query)
                self.working_memory.add_message("assistant", result)

            if self.semantic_memory:
                self.semantic_memory.add_document(
                    content=f"Query: {query}\nAnswer: {result}",
                    metadata={"session_id": session_id, "type": "interaction"}
                )

            duration_ms = int((time.time() - start_time) * 1000)
            tokens_used = (len(query) + len(result)) // 4

            self.request_count += 1
            self.total_tokens += tokens_used

            return AgentResponse(
                success=True,
                answer=result,
                steps=[],
                duration_ms=duration_ms,
                tokens_used=tokens_used
            )

        except Exception as e:
            logger.error(f"Ошибка: {e}", exc_info=True)
            return AgentResponse(
                success=False,
                answer="Произошла ошибка при обработке запроса.",
                steps=[],
                duration_ms=0,
                tokens_used=0,
                error=str(e)
            )

    def get_stats(self) -> Dict:
        return {
            "name": self.config.name,
            "version": self.config.version,
            "tools": len(self.tools),
            "memory_enabled": self.config.memory_enabled,
            "requests": self.request_count,
            "tokens_total": self.total_tokens
        }


# ==================== ТЕСТ ====================
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    print("=" * 90)
    print("ЛАБОРАТОРНАЯ РАБОТА №2 — ТЕСТ АГЕНТА")
    print("=" * 90)

    agent = AIAgent()
    test_query = "Найди информацию о последнем обновлении YandexGPT и рассчитай, сколько месяцев прошло с момента выхода последней версии"

    response = agent.run(test_query)

    print(f"\n✅ Ответ агента:\n{response.answer}")
    print(f"\n⏱ Время: {response.duration_ms} мс | Токены: {response.tokens_used}")
    print(f"Статус: {'Успех ✅' if response.success else 'Ошибка ❌'}")