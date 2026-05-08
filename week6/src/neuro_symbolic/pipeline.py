# -*- coding: utf-8 -*-
"""
Нейро-символьный гибридный пайплайн
Лабораторная работа №6
"""
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import time

from neural.llm_client import LLMClient
from symbolic.rule_engine import RuleEngine, InferenceResult
from symbolic.knowledge_base import KnowledgeBase

logger = logging.getLogger(__name__)


class NeuroSymbolicPipeline:
    def __init__(self, llm: Optional[LLMClient] = None, rule_engine: Optional[RuleEngine] = None,
                 knowledge_base: Optional[KnowledgeBase] = None, neural_weight: float = 0.6,
                 symbolic_weight: float = 0.4):
        self.llm = llm or LLMClient()
        self.rule_engine = rule_engine or RuleEngine()
        self.knowledge_base = knowledge_base or KnowledgeBase()
        self.neural_weight = neural_weight
        self.symbolic_weight = symbolic_weight
        logger.info(f"NeuroSymbolicPipeline инициализирован (neural={neural_weight}, symbolic={symbolic_weight})")

    def process(self, input_data: Dict[str, Any], include_explanation: bool = True) -> Dict[str, Any]:
        start_time = time.time()
        logger.info(f"Обработка запроса: {input_data.get('query', 'N/A')[:100]}...")

        neural_result = self._neural_processing(input_data)
        symbolic_result = self._symbolic_processing(input_data)
        integrated_result = self._integrate_results(neural_result, symbolic_result, input_data)

        execution_time = time.time() - start_time
        result = {
            "success": True,
            "input": input_data,
            "neural_output": neural_result,
            "symbolic_output": symbolic_result,
            "final_decision": integrated_result["decision"],
            "confidence": integrated_result["confidence"],
            "explanation": integrated_result["explanation"] if include_explanation else "",
            "execution_time": round(execution_time, 3),
            "timestamp": datetime.now().isoformat()
        }
        logger.info(f"Пайплайн завершён за {execution_time:.3f}с")
        return result

    def _neural_processing(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        query = input_data.get("query", "")
        categories = input_data.get("categories", ["норма", "предупреждение", "критично"])
        classification = self.llm.classify(query, categories)

        prompt = f"Проанализируй данные и сделай предварительный вывод.\nДанные: {input_data}\nВывод:"
        llm_response = self.llm.generate(prompt=prompt,
                                         system_prompt="Ты — эксперт-аналитик. Делай точные выводы на основе данных.")

        return {
            "classification": classification,
            "preliminary_conclusion": llm_response.get("text", ""),
            "confidence": classification.get("confidence", 0.5),
            "success": llm_response.get("success", False)
        }

    def _symbolic_processing(self, input_data: Dict[str, Any]) -> InferenceResult:
        facts = input_data.get("facts", {})
        return self.rule_engine.infer(facts)

    def _integrate_results(self, neural: Dict[str, Any], symbolic: InferenceResult, input_data: Dict[str, Any]) -> Dict[
        str, Any]:
        neural_conclusion = neural.get("preliminary_conclusion", "")
        neural_confidence = neural.get("confidence", 0.5)
        symbolic_conclusions = symbolic.conclusions
        symbolic_confidence = 1.0 if symbolic.success else 0.0

        final_confidence = (neural_confidence * self.neural_weight + symbolic_confidence * self.symbolic_weight)

        decision_parts = []
        if neural_conclusion:
            decision_parts.append(f"Нейронный вывод: {neural_conclusion}")
        if symbolic_conclusions:
            decision_parts.append(f"Символьный вывод: {', '.join(symbolic_conclusions)}")

        final_decision = "\n".join(decision_parts) if decision_parts else "Нет выводов"
        explanation = self._generate_explanation(neural, symbolic, final_confidence)

        return {"decision": final_decision, "confidence": round(final_confidence, 3), "explanation": explanation}

    def _generate_explanation(self, neural: Dict[str, Any], symbolic: InferenceResult, confidence: float) -> str:
        explanation_parts = ["=== ОБЪЯСНЕНИЕ РЕШЕНИЯ ===\n", "Нейронная компонента:"]
        explanation_parts.append(
            f" • Классификация: {neural.get('classification', {}).get('predicted_category', 'N/A')}")
        explanation_parts.append(f" • Уверенность: {neural.get('confidence', 0):.1%}")

        explanation_parts.append("\nСимвольная компонента:")
        if symbolic.triggered_rules:
            for rule in symbolic.triggered_rules:
                explanation_parts.append(f" • {rule.name}: {rule.description}")
        else:
            explanation_parts.append(" • Правила не сработали")

        explanation_parts.append(f"\nИтоговая уверенность: {confidence:.1%}")
        explanation_parts.append(f" • Вес нейронной компоненты: {self.neural_weight:.1%}")
        explanation_parts.append(f" • Вес символьной компоненты: {self.symbolic_weight:.1%}")
        return "\n".join(explanation_parts)

    def get_statistics(self) -> Dict[str, Any]:
        return {
            "neural_weight": self.neural_weight,
            "symbolic_weight": self.symbolic_weight,
            "rules_count": len(self.rule_engine.rules),
            "facts_count": len(self.knowledge_base.facts),
            "inferences_count": len(self.rule_engine.inference_history)
        }