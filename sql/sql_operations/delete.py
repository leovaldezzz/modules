from .query import Query
from ..utils.errors import MissingConditionError

class Delete(Query):
    operation = "delete"

    def sql(self) -> str:

        if not self.has_where:
            # raise ValueError(
            #     "DELETE requires a WHERE condition"
            # )
            raise MissingConditionError()

        self._reset_params()

        template = (
            f"DELETE FROM {self.table}"
            f"{self._compile_where()}"
        )

        return template