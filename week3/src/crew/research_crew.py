# -*- coding: utf-8 -*-
from typing import Dict, Optional
from dataclasses import dataclass
from datetime import datetime
import time
import logging

from agents.researcher_agent import ResearcherAgent
from agents.analyst_agent import AnalystAgent
from agents.writer_agent import WriterAgent

logger = logging.getLogger(__name__)


@dataclass
class CrewConfig:
    name: str = "ResearchCrew"
    process_type: str = "sequential"
    verbose: bool = True
    memory_enabled: bool = True


@dataclass
class CrewResult:
    success: bool
    final_output: str
    agent_results: Dict
    execution_time: float
    timestamp: str


class ResearchCrew:
    def __init__(self, config: Optional[CrewConfig] = None):
        self.config = config or CrewConfig()
        self.researcher = ResearcherAgent()
        self.analyst = AnalystAgent()
        self.writer = WriterAgent()
        self.shared_context = {}

        self.statistics = {
            "crews_executed": 0,
            "successful_executions": 0,
            "failed_executions": 0,
            "total_execution_time": 0
        }
        logger.info(f"Команда агентов инициализирована: {self.config.name}")

    def execute(self, task: str, context: Optional[Dict] = None) -> CrewResult:
        start_time = time.time()
        logger.info(f"Команда начинает выполнение задачи: {task[:100]}...")

        agent_results = {}
        self.shared_context = context or {}

        try:
            logger.info("Этап 1: Сбор данных")
            researcher_result = self.researcher.execute_task(task, self.shared_context)
            agent_results["researcher"] = researcher_result
            self.shared_context["research_data"] = researcher_result

            logger.info("Этап 2: Анализ угрозы")
            analyst_result = self.analyst.execute_task(task, self.shared_context)
            agent_results["analyst"] = analyst_result
            self.shared_context["analysis_data"] = analyst_result

            logger.info("Этап 3: Формирование протокола")
            writer_result = self.writer.execute_task(task, self.shared_context)
            agent_results["writer"] = writer_result

            execution_time = time.time() - start_time
            self.statistics["crews_executed"] += 1
            self.statistics["successful_executions"] += 1
            self.statistics["total_execution_time"] += execution_time

            logger.info(f"Команда завершила работу за {execution_time:.2f}с")

            return CrewResult(
                success=True,
                final_output=writer_result.get("document", ""),
                agent_results=agent_results,
                execution_time=execution_time,
                timestamp=datetime.now().isoformat()
            )

        except Exception as e:
            logger.error(f"Ошибка выполнения команды: {e}", exc_info=True)
            execution_time = time.time() - start_time
            self.statistics["crews_executed"] += 1
            self.statistics["failed_executions"] += 1

            return CrewResult(
                success=False,
                final_output=f"Ошибка: {str(e)}",
                agent_results=agent_results,
                execution_time=execution_time,
                timestamp=datetime.now().isoformat()
            )