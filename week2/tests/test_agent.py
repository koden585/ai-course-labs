import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()   # КРИТИЧНО ДЛЯ ТЕСТОВ

import pytest
from src.agent_core import AIAgent, AgentConfig
from src.tools.search_tool import SearchTool
from src.tools.calc_tool import CalculateTool
from src.tools.custom_tool import CustomTool
from src.guardrails.input_validator import InputGuardrails

def test_tools_creation():
    assert SearchTool().name == "search_web"
    assert CalculateTool().name == "calculate"
    assert CustomTool().name == "extract_technical_params"

def test_custom_tool_works():
    tool = CustomTool()
    result = tool._run("вал диаметром 50 мм из стали 45")
    assert "Сталь 45" in result or "Диаметр" in result

def test_guardrails_blocks_attack():
    guard = InputGuardrails()
    check = guard.validate_input("DROP TABLE users")
    assert check.is_safe is False

def test_agent_can_run():
    agent = AIAgent(AgentConfig(max_iterations=10, verbose=False))
    resp = agent.run("Что такое YandexGPT?")
    assert resp.success is True

if __name__ == "__main__":
    pytest.main(["-v", "--tb=no"])