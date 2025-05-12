from sqlalchemy import BinaryExpression
from sqlalchemy.sql import and_, func, true
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
    def is_satisfied(cls, model, rows: dict[str, Any]) -> BinaryExpression | None:
        if not rows:
            return and_()

        conditions = []
        for key, value in rows.items():
            column = getattr(model, key)

            if isinstance(value, (list, tuple, set)) and not isinstance(value, str):
                conditions.append(column.in_(value))
            else:
                conditions.append(column == value)

        return and_(*conditions)


class OrderByRowsDefaultSpecification(Specification):
    @classmethod
    async def is_satisfied(cls, model, rows: dict[str, Any]) -> None:
        return and_()


class DeleteSpaceAndLowerCaseSpecification(Specification):
    @classmethod
    async def is_satisfied(cls, model, rows: dict[str, Any]) -> BinaryExpression:
        conditions = []
        for key, value in rows.items():
            column = getattr(model, key)

            if isinstance(value, str) and value.replace(' ', '').strip():
                condition = func.replace(func.lower(column), ' ', '') == value.replace(' ', '').lower()
                conditions.append(condition)

            elif isinstance(value, (int, float, bool)):
                condition = column == value
                conditions.append(condition)

        return and_(*conditions) if conditions else and_()

