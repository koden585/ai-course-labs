# -*- coding: utf-8 -*-
from typing import Dict, Optional, List
import time
import logging
from agents.base_agent import BaseAgent, AgentConfig

logger = logging.getLogger(__name__)


class AnalystAgent(BaseAgent):
    def __init__(self, config: Optional[AgentConfig] = None):
        default_config = AgentConfig(
            role="Аналитик кибер-физических угроз",
            goal="Оценка уровня опасности на основе собранных фактов",
            backstory="Вы — аналитик службы безопасности. Ваша задача выявлять критические инциденты."
        )
        super().__init__(config or default_config)

    def execute_task(self, task_description: str, context: Optional[Dict] = None) -> Dict:
        start_time = time.time()
        self.state.current_task = task_description

        research_data = context.get("research_data", {}) if context else {}

        results = {
            "task": task_description,
            "status": "completed",
            "patterns_identified": ["Паттерн: Возможное несанкционированное проникновение в закрытую зону"],
            "insights": [
                "Уровень угрозы: КРИТИЧЕСКИЙ (КРАСНЫЙ)",
                "Требуется немедленное реагирование группы быстрого реагирования (ГБР)"
            ],
            "execution_time": time.time() - start_time
        }
        return results

    def get_capabilities(self) -> List[str]:
        return ["Оценка угроз", "Выявление паттернов нарушений"]