from sqlalchemy import BinaryExpression
from sqlalchemy.sql import and_, true
from abc import ABC, abstractmethod
from sqlalchemy.sql import expression
from typing import Any, TYPE_CHECKING


class Specification(ABC):
    # def __init__(self, model) -> None:
    #     self._model = model

    @classmethod
    @abstractmethod
    def is_satisfied(cls, *args: Any, **kwargs: Any) -> expression.BinaryExpression:
        pass
    # def __and__(self):
    #     pass
    #
    # def __or__(self):
    #     pass
    #
    # def __eq__(self, other):
    #     pass


class ObjectExistsByRowsSpecification(Specification):

    @classmethod
    async def is_satisfied(cls, model, rows: dict[str, Any]) -> BinaryExpression | None:
        if rows:
            conditions = [getattr(model, key) == value for key, value in rows.items()]

            return and_(*conditions)

        return and_()


class OrderByRowsDefaultSpecification(Specification):
    @classmethod
    async def is_satisfied(cls, model, rows: dict[str, Any]) -> None:
        return and_()
