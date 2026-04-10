# -*- coding: utf-8 -*-
"""
Guardrails — проверка безопасности входных данных
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class SecurityCheck:
    is_safe: bool
    reason: Optional[str] = None

class InputGuardrails:
    """Простая защита от вредоносных запросов"""

    def validate_input(self, query: str) -> SecurityCheck:
        query_lower = query.lower()

        # Запрещённые слова/паттерны
        forbidden = ["sql injection", "rm -rf", "delete from", "drop table", "<script>"]
        for word in forbidden:
            if word in query_lower:
                return SecurityCheck(
                    is_safe=False,
                    reason=f"Обнаружен потенциально опасный запрос: {word}"
                )

        # Проверка длины
        if len(query) > 1000:
            return SecurityCheck(
                is_safe=False,
                reason="Запрос слишком длинный (>1000 символов)"
            )

        return SecurityCheck(is_safe=True)