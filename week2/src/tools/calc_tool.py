# -*- coding: utf-8 -*-
"""
Безопасный калькулятор (исправлено под ZERO_SHOT_REACT_DESCRIPTION)
"""

from langchain.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import ast
import operator
import logging

logger = logging.getLogger(__name__)

class CalculateInput(BaseModel):
    expression: str = Field(description="Математическое выражение (2+2*3)", min_length=1, max_length=200)

class SafeCalculator:
    OPERATORS = {
        ast.Add: operator.add, ast.Sub: operator.sub,
        ast.Mult: operator.mul, ast.Div: operator.truediv,
        ast.Pow: operator.pow, ast.USub: operator.neg,
    }

    def eval_expr(self, expr: str) -> float:
        node = ast.parse(expr, mode='eval').body
        return self._eval_node(node)

    def _eval_node(self, node):
        if isinstance(node, (ast.Constant, ast.Num)):
            return node.value if hasattr(node, 'value') else node.n
        if isinstance(node, ast.BinOp):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            return self.OPERATORS[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp):
            return self.OPERATORS[type(node.op)](self._eval_node(node.operand))
        raise ValueError(f"Неподдерживаемая операция: {type(node)}")

class CalculateTool(BaseTool):
    name = "calculate"
    description = "Безопасные математические вычисления. Поддерживает +, -, *, /, **."
    args_schema: Type[BaseModel] = CalculateInput

    calculator = SafeCalculator()

    def _run(self, expression: str) -> str:
        logger.info(f"Вычисление: {expression}")
        try:
            result = self.calculator.eval_expr(expression)
            return f"{expression} = {result:.2f}"
        except Exception as e:
            return f"Ошибка вычисления: {e}"

    async def _arun(self, expression: str) -> str:
        return self._run(expression)

    def to_langchain_tool(self) -> BaseTool:
        return self