from .query import Query

class Select(Query):
    operation = "select"

    def sql(self) -> str:
        self._reset_params()

        columns = self._compile_fields()

        template = (
            f"SELECT "
            f"{self._compile_distinct()}"
            f"{columns} "
            f"{self._compile_from()}"
            f"{self._compile_joins()}"
            f"{self._compile_where()}"
            f"{self._compile_group_by()}"
            f"{self._compile_order_by()}"
            f"{self._compile_limit()}"
            f"{self._compile_offset()}"
        )

        return template