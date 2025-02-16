from sqlalchemy import BinaryExpression
from sqlalchemy.sql import and_
from abc import ABC, abstractmethod
from pedant_killer.database.database import Base
from sqlalchemy.sql import expression
from typing import Any, Coroutine, TYPE_CHECKING

if TYPE_CHECKING:
    from pedant_killer.database.repository.core_repository import CoreRepository


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

        return None


class OrderByRowsDefaultSpecification(Specification):
    @classmethod
    async def is_satisfied(cls, model, rows: dict[str, Any]) -> None:
        return None
