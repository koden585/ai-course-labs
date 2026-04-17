# -*- coding: utf-8 -*-
from typing import Dict, Optional, List
import time
import logging
from agents.base_agent import BaseAgent, AgentConfig

logger = logging.getLogger(__name__)


class ResearcherAgent(BaseAgent):
    def __init__(self, config: Optional[AgentConfig] = None):
        default_config = AgentConfig(
            role="Офицер по сбору данных видеонаблюдения",
            goal="Сбор сырых фактов и логов с камер слежения",
            backstory="Вы — агент, агрегирующий данные со всех подсистем видеоаналитики."
        )
        super().__init__(config or default_config)

    def execute_task(self, task_description: str, context: Optional[Dict] = None) -> Dict:
        start_time = time.time()
        self.state.current_task = task_description

        # ДОСТАЕМ РЕАЛЬНЫЕ ДАННЫЕ ОТ ВИДЕО-АГЕНТА
        video_data = context.get("video_data", {}) if context else {}

        results = {
            "task": task_description,
            "status": "completed",
            "sources_found": [
                {"title": f"Камера: {video_data.get('camera_id', 'Неизвестно')}", "url": "local://dvr/cam-04"}],
            "key_facts": self._extract_facts(video_data),
            "recommendations": ["Необходимо передать данные аналитику для оценки угрозы."],
            "execution_time": time.time() - start_time
        }
        return results

    def _extract_facts(self, video_data: Dict) -> List[str]:
        facts = []
        for anomaly in video_data.get("anomalies", []):
            facts.append(f"ЗАФИКСИРОВАНО: {anomaly}")
        for obj in video_data.get("detected_objects", []):
            facts.append(f"РАСПОЗНАН ОБЪЕКТ: {obj}")
        return facts if facts else ["Событий не зафиксировано"]

    def get_capabilities(self) -> List[str]:
        return ["Сбор логов камер", "Фильтрация событий"]