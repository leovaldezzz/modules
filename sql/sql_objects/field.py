from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .condition import Condition
from .order import Order

if TYPE_CHECKING:
    from .table import Table


class Field:
    def __init__(self, table: "Table", name: str) -> None:
        self.table = table
        self.name = name

    def __str__(self) -> str:
        return f"{self.table.tablename}.{self.name}"

    def __eq__(self, other: Any) -> Condition:
        return Condition(self, "=", other)

    def __ne__(self, other: Any) -> Condition:
        return Condition(self, "!=", other)

    def __lt__(self, other: Any) -> Condition:
        return Condition(self, "<", other)

    def __le__(self, other: Any) -> Condition:
        return Condition(self, "<=", other)

    def __gt__(self, other: Any) -> Condition:
        return Condition(self, ">", other)

    def __ge__(self, other: Any) -> Condition:
        return Condition(self, ">=", other)

    def like(self, value: Any) -> Condition:
        return Condition(self, "LIKE", value)

    def ilike(self, value: Any) -> Condition:
        return Condition(self, "ILIKE", value)

    def isin(self, values: Any) -> Condition:
        return Condition(self, "IN", values)

    def asc(self) -> Order:
        return Order(self, "ASC")

    def desc(self) -> Order:
        return Order(self, "DESC")