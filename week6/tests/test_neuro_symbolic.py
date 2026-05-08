# -*- coding: utf-8 -*-
import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from symbolic.rule_engine import RuleEngine
from symbolic.video_rules import get_video_rules

class TestVideoRules(unittest.TestCase):
    def setUp(self):
        self.engine = RuleEngine()
        self.engine.add_rules(get_video_rules())

    def test_unattended_baggage(self):
        """Тест правила: оставленный багаж > 60 сек"""
        facts = {"object": "backpack", "time_unattended_sec": 120}
        result = self.engine.infer(facts)
        self.assertTrue(result.success)
        self.assertIn("ТРЕВОГА: Проверить на ВУ", result.conclusions)

    def test_weapon_detected(self):
        """Тест правила: обнаружено оружие"""
        facts = {"weapon_detected": True}
        result = self.engine.infer(facts)
        self.assertTrue(result.success)
        self.assertIn("КРИТИЧЕСКАЯ ТРЕВОГА: БЛОКИРОВКА ДВЕРЕЙ", result.conclusions)

    def test_normal_behavior(self):
        """Тест: нет нарушений"""
        facts = {"object": "person", "geozone": "Холл", "weapon_detected": False}
        result = self.engine.infer(facts)
        self.assertFalse(result.success)

if __name__ == '__main__':
    unittest.main()