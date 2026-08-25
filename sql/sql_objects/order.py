from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .field import Field


class Order:
    def __init__(self, field: "Field", direction: str) -> None:
        self.field = field
        self.direction = direction

    def __str__(self) -> str:
        return f"{self.field} {self.direction}"