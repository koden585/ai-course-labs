# -*- coding: utf-8 -*-
import sys, os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from dotenv import load_dotenv
from neural.llm_client import LLMClient
from symbolic.rule_engine import RuleEngine
from symbolic.video_rules import get_video_rules
from neuro_symbolic.pipeline import NeuroSymbolicPipeline


def main():
    load_dotenv(dotenv_path="../.env")
    print("=" * 80)
    print("ТЕСТИРОВАНИЕ НЕЙРО-СИМВОЛЬНОГО ПАЙПЛАЙНА (ВИДЕОМОНИТОРИНГ)")
    print("=" * 80)

    llm = LLMClient()
    rule_engine = RuleEngine()
    rule_engine.add_rules(get_video_rules())

    pipeline = NeuroSymbolicPipeline(llm=llm, rule_engine=rule_engine)

    test_event = {
        "query": "На камере CAM-02 видно человека в черном капюшоне, который оставил рюкзак возле серверной стойки. Рюкзак лежит 120 секунд.",
        "facts": {
            "object": "backpack",
            "geozone": "Серверная",
            "time_unattended_sec": 120,
            "is_night": False,
            "weapon_detected": False
        },
        "categories": ["норма", "предупреждение", "критично"]
    }

    print(f"\n[ВХОДНЫЕ ДАННЫЕ]:\nТекст для LLM: {test_event['query']}\nФакты для Правил: {test_event['facts']}\n")

    result = pipeline.process(test_event)

    print(f"[КЛАССИФИКАЦИЯ LLM]: {result['neural_output']['classification']['predicted_category']}")
    print(f"\n[ФИНАЛЬНОЕ РЕШЕНИЕ]:\n{result['final_decision']}")
    print(f"\n{result['explanation']}")
    print(f"\nСТАТИСТИКА: {pipeline.get_statistics()}")


if __name__ == "__main__":
    main()