from __future__ import annotations

from typing import Any


class Expression:
    def __and__(self, other: Any) -> "CompoundCondition":
        return CompoundCondition(self, "AND", other)

    def __or__(self, other: Any) -> "CompoundCondition":
        return CompoundCondition(self, "OR", other)

    def __add__(self, other: Any) -> "ArithmeticExpression":
        return ArithmeticExpression(self, "+", other)

    def __sub__(self, other: Any) -> "ArithmeticExpression":
        return ArithmeticExpression(self, "-", other)

    def __mul__(self, other: Any) -> "ArithmeticExpression":
        return ArithmeticExpression(self, "*", other)

    def __truediv__(self, other: Any) -> "ArithmeticExpression":
        return ArithmeticExpression(self, "/", other)


class BinaryExpression(Expression):
    def __init__(self, left: Any, operator: str, right: Any) -> None:
        self.left = left
        self.operator = operator
        self.right = right

class CompoundCondition(BinaryExpression):
    pass

class ArithmeticExpression(BinaryExpression):
    pass

class UnaryExpression(Expression):
    def __init__(self, operator: str, expression: Any) -> None:
        self.operator = operator
        self.expression = expression


class FunctionExpression(Expression):
    def __init__(self, name: str, *args: Any) -> None:
        self.name = name
        self.args = args


class Condition(Expression):
    def __init__(self, column: Any, operator: str, value: Any) -> None:
        self.column = column
        self.operator = operator
        self.value = value