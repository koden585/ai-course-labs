# -*- coding: utf-8 -*-
"""
Базовый класс для специализированных агентов
Лабораторная работа №3
Автор: [Ваши ФИО]
Группа: [Номер группы]
"""
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class AgentConfig:
    role: str = "Assistant"
    goal: str = "Help users with their tasks"
    backstory: str = "You are a helpful AI assistant"
    verbose: bool = True
    allow_delegation: bool = False
    max_iter: int = 10


@dataclass
class AgentState:
    agent_id: str = field(default_factory=lambda: f"agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    current_task: Optional[str] = None
    completed_tasks: List[str] = field(default_factory=list)
    message_history: List[Dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    last_active: datetime = field(default_factory=datetime.now)


class BaseAgent:
    """Базовый класс для всех агентов в системе."""

    def __init__(self, config: Optional[AgentConfig] = None):
        self.config = config or AgentConfig()
        self.state = AgentState()
        self.tools = []
        self.statistics = {
            "tasks_completed": 0,
            "tasks_failed": 0,
            "total_execution_time": 0,
            "messages_sent": 0,
            "messages_received": 0
        }
        logger.info(f"Агент инициализирован: {self.config.role}")

    def execute_task(self, task_description: str, context: Optional[Dict] = None) -> Dict:
        raise NotImplementedError("Метод execute_task должен быть реализован в наследнике")

    def get_capabilities(self) -> List[str]:
        raise NotImplementedError("Метод get_capabilities должен быть реализован в наследнике")

    def receive_message(self, message: Dict) -> None:
        self.state.message_history.append({
            "direction": "incoming",
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
        self.statistics["messages_received"] += 1
        self.state.last_active = datetime.now()
        logger.debug(f"Агент {self.state.agent_id} получил сообщение")

    def send_message(self, receiver_id: str, content: Dict) -> Dict:
        message = {
            "sender_id": self.state.agent_id,
            "receiver_id": receiver_id,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "type": "agent_message"
        }
        self.state.message_history.append({
            "direction": "outgoing",
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
        self.statistics["messages_sent"] += 1
        logger.debug(f"Агент {self.state.agent_id} отправил сообщение агенту {receiver_id}")
        return message

    def get_statistics(self) -> Dict:
        return {
            "agent_id": self.state.agent_id,
            "role": self.config.role,
            "statistics": self.statistics,
            "completed_tasks_count": len(self.state.completed_tasks),
            "message_history_length": len(self.state.message_history)
        }

    def reset_state(self) -> None:
        self.state.current_task = None
        self.state.message_history = []
        logger.info(f"Агент {self.state.agent_id} сбросил состояние")