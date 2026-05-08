# -*- coding: utf-8 -*-
"""
Оперативная (рабочая) память агента
"""

from typing import List, Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Message:
    role: str
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict = field(default_factory=dict)

class WorkingMemory:
    """Краткосрочная память (буфер сообщений)"""

    def __init__(self, max_tokens: int = 4000):
        self.messages: List[Message] = []
        self.max_tokens = max_tokens
        self.current_tokens = 0

    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None) -> None:
        msg = Message(role=role, content=content, metadata=metadata or {})
        self.messages.append(msg)
        self.current_tokens += len(content) // 4

        # Обрезаем старые сообщения при переполнении
        while self.current_tokens > self.max_tokens and len(self.messages) > 1:
            removed = self.messages.pop(0)
            self.current_tokens -= len(removed.content) // 4

    def get_messages(self) -> List[Dict]:
        return [
            {"role": msg.role, "content": msg.content, "metadata": msg.metadata}
            for msg in self.messages
        ]

    def clear(self) -> None:
        self.messages.clear()
        self.current_tokens = 0

    def get_stats(self) -> Dict:
        return {
            "message_count": len(self.messages),
            "current_tokens": self.current_tokens,
            "max_tokens": self.max_tokens,
            "usage_percent": round((self.current_tokens / self.max_tokens) * 100, 1) if self.max_tokens else 0
        }