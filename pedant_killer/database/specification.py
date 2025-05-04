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
    async def is_satisfied(cls, model, rows: dict[str, Any]) -> BinaryExpression | None:
        if rows:
            conditions = [getattr(model, key) == value for key, value in rows.items()]

            return and_(*conditions)

        return and_()


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


class IdInListSpecification(Specification):
    @classmethod
    async def is_satisfied(cls, model, rows: dict[str, int | list[int]]) -> BinaryExpression:
        return and_(
            model.device_id == rows['device_id'],
            model.service_id.in_(rows['service_id'])
        )
