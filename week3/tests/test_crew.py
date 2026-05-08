# -*- coding: utf-8 -*-
import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from agents.video_monitor_agent import VideoMonitorAgent
from crew.research_crew import ResearchCrew


class TestMultiAgentSystem(unittest.TestCase):

    def test_video_agent_initialization(self):
        """Проверка инициализации агента видеомониторинга"""
        agent = VideoMonitorAgent()
        self.assertEqual(agent.config.role, "Модуль видеоаналитики (CV/Surveillance)")
        self.assertTrue(len(agent.get_capabilities()) > 0)

    def test_crew_initialization(self):
        """Проверка создания команды"""
        crew = ResearchCrew()
        self.assertIsNotNone(crew.researcher)
        self.assertIsNotNone(crew.analyst)
        self.assertIsNotNone(crew.writer)


if __name__ == '__main__':
    unittest.main()