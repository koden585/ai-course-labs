# -*- coding: utf-8 -*-
import sys
import os

# Подключаем пути для PyCharm
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from crew.research_crew import ResearchCrew
from agents.video_monitor_agent import VideoMonitorAgent
import json


def main():
    print("=" * 80)
    print("ЗАПУСК MULTI-AGENT СИСТЕМЫ: ИНТЕЛЛЕКТУАЛЬНЫЙ ВИДЕОМОНИТОРИНГ")
    print("=" * 80)

    # ---------------------------------------------------------
    # ЭТАП 1: Работа вашего дипломного агента (Анализ камер)
    # ---------------------------------------------------------
    print("\n[ЭТАП 1] Работа системы компьютерного зрения (VideoMonitorAgent)...")
    video_agent = VideoMonitorAgent()
    video_result = video_agent.execute_task("Анализ видеопотока с камеры CAM-04 за последние 5 минут")

    print("Сырые данные от видео-агента получены (в формате JSON).")
    # Выведем только найденные аномалии для наглядности
    print(f"Обнаружено: {video_result['anomalies']}")

    # ---------------------------------------------------------
    # ЭТАП 2: Передача данных Команде (Researcher -> Analyst -> Writer)
    # ---------------------------------------------------------
    print("\n" + "=" * 80)
    print("[ЭТАП 2] Передача данных Команде для составления рапорта об инциденте...")
    print("=" * 80)

    crew = ResearchCrew()

    # Формируем задачу для Crew на основе того, что нашел видео-агент!
    anomalies_str = ", ".join(video_result['anomalies'])
    task_for_crew = f"Сформировать протокол нарушения безопасности. Входные данные с камер: {anomalies_str}."

    # Передаем сырые видео-данные как контекст для аналитиков
    context = {"video_data": video_result}

    # Запускаем конвейер
    crew_result = crew.execute(task_for_crew, context)

    # ---------------------------------------------------------
    # ЭТАП 3: ФИНАЛЬНЫЙ ВЫВОД
    # ---------------------------------------------------------
    print("\n" + "=" * 80)
    print("ИТОГОВЫЙ ДОКУМЕНТ (Единый результат работы всех агентов):")
    print("=" * 80)
    print(crew_result.final_output)


if __name__ == "__main__":
    main()