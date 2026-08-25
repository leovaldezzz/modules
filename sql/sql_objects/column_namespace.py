from __future__ import annotations

from typing import TYPE_CHECKING, Iterator

from .field import Field

if TYPE_CHECKING:
    from .table import Table


class ColumnNamespace:
    def __init__(self, table: "Table") -> None:
        self.table = table

        for name in table.schema:
            setattr(
                self,
                name,
                Field(table, name)
            )

    def __getitem__(self, name: str) -> Field:
        try:
            return getattr(self, name)
        except AttributeError as exc:
            raise KeyError(name) from exc

    def __iter__(self) -> Iterator[str]:
        return iter(self.table.schema)