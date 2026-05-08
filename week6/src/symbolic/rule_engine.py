# -*- coding: utf-8 -*-
# Движок логического вывода на правилах

import logging
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)

class RulePriority(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

@dataclass
class Rule:
    rule_id: str
    name: str
    condition: Callable[[Dict], bool]
    conclusion: str
    priority: RulePriority = RulePriority.MEDIUM
    description: str = ""
    domain: str = "general"

    def evaluate(self, facts: Dict[str, Any]) -> bool:
        try:
            return self.condition(facts)
        except Exception as e:
            logger.error(f"Ошибка оценки правила {self.rule_id}: {e}")
            return False

    def to_dict(self) -> Dict:
        return {
            "rule_id": self.rule_id,
            "name": self.name,
            "conclusion": self.conclusion,
            "priority": self.priority.value,
            "description": self.description,
            "domain": self.domain
        }

@dataclass
class InferenceResult:
    success: bool
    conclusions: List[str]
    triggered_rules: List[Rule]
    explanation: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

class RuleEngine:
    def __init__(self):
        self.rules: List[Rule] =[]
        self.facts: Dict[str, Any] = {}
        self.inference_history: List[InferenceResult] =[]
        logger.info("RuleEngine инициализирован")

    def add_rule(self, rule: Rule) -> None:
        self.rules.append(rule)
        self.rules.sort(key=lambda r: r.priority.value)
        logger.info(f"Добавлено правило: {rule.rule_id} ({rule.name})")

    def add_rules(self, rules: List[Rule]) -> None:
        for rule in rules:
            self.add_rule(rule)

    def set_facts(self, facts: Dict[str, Any]) -> None:
        self.facts = facts
        logger.debug(f"Установлено {len(facts)} фактов")

    def infer(self, facts: Optional[Dict[str, Any]] = None) -> InferenceResult:
        if facts:
            self.set_facts(facts)

        triggered_rules =[]
        conclusions = []
        explanation_parts =[]

        logger.info(f"Начало логического вывода ({len(self.rules)} правил)")

        for rule in self.rules:
            if rule.evaluate(self.facts):
                triggered_rules.append(rule)
                conclusions.append(rule.conclusion)
                explanation_parts.append(f"• Правило '{rule.name}': {rule.description} -> {rule.conclusion}")
                logger.debug(f"Сработало правило: {rule.rule_id}")

        if triggered_rules:
            explanation = "Логический вывод:\n" + "\n".join(explanation_parts)
        else:
            explanation = "Ни одно правило не сработало"

        result = InferenceResult(
            success=len(triggered_rules) > 0,
            conclusions=conclusions,
            triggered_rules=triggered_rules,
            explanation=explanation
        )

        self.inference_history.append(result)
        logger.info(f"Вывод завершён: {len(conclusions)} заключений")
        return result

    def get_rule_statistics(self) -> Dict[str, Any]:
        return {
            "total_rules": len(self.rules),
            "rules_by_priority": {
                priority.name: sum(1 for r in self.rules if r.priority == priority)
                for priority in RulePriority
            },
            "rules_by_domain": {},
            "total_inferences": len(self.inference_history)
        }

    def clear_facts(self) -> None:
        self.facts = {}
        logger.debug("Факты очищены")

    def export_rules(self) -> List[Dict]:
        return [rule.to_dict() for rule in self.rules]