# -*- coding: utf-8 -*-
from typing import Dict, Optional, List
import time
import logging
from agents.base_agent import BaseAgent, AgentConfig

logger = logging.getLogger(__name__)


class WriterAgent(BaseAgent):
    def __init__(self, config: Optional[AgentConfig] = None):
        default_config = AgentConfig(
            role="Генератор протоколов безопасности",
            goal="Создание официального рапорта об инциденте",
            backstory="Вы формируете автоматические рапорты для начальника смены охраны."
        )
        super().__init__(config or default_config)

    def execute_task(self, task_description: str, context: Optional[Dict] = None) -> Dict:
        start_time = time.time()
        self.state.current_task = task_description

        research_data = context.get("research_data", {}) if context else {}
        analysis_data = context.get("analysis_data", {}) if context else {}

        document = f"""
# ПРОТОКОЛ ИНЦИДЕНТА БЕЗОПАСНОСТИ
**Основание:** {task_description}

## 1. Сводка происшествия
*(Сгенерировано: {self.config.role})*
Данный протокол сформирован автоматической системой интеллектуального видеомониторинга. В отчёте зафиксированы нарушения периметра и подозрительные предметы.

## 2. Зафиксированные факты (Данные с камер)
*(Предоставлено: Офицер по сбору данных видеонаблюдения)*
{self._write_list(research_data.get("key_facts", []))}

## 3. Анализ угрозы
*(Предоставлено: Аналитик кибер-физических угроз)*
{self._write_list(analysis_data.get("insights", []))}
{self._write_list(analysis_data.get("patterns_identified", []))}

 ## 4. Резолюция
*(Совместный вывод)*
{self._write_list(research_data.get("recommendations", []))}

## 5. Источник данных
*(Предоставлено: Модуль видеоаналитики)*
{self._write_sources(research_data.get("sources_found", []))}
"""
        results = {
            "task": task_description,
            "status": "completed",
            "document": document,
            "execution_time": time.time() - start_time
        }
        return results

    def _write_list(self, items: List[str]) -> str:
        return "\n".join([f"• {item}" for item in items]) if items else "Нет данных."

    def _write_sources(self, sources: List[Dict]) -> str:
        return "\n".join([f"- {s.get('title')} ({s.get('url')})" for s in sources]) if sources else "Нет источников."

    def get_capabilities(self) -> List[str]:
        return ["Генерация рапортов", "Структурирование инцидентов"]