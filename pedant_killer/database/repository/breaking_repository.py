from typing import Sequence, Any

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from pedant_killer.database.repository.core_repository import CoreRepository
from pedant_killer.database.database import database_logger
from pedant_killer.database.models.breaking_orm import BreakingOrm
from pedant_killer.database.specification import (Specification,
                                                  OrderByRowsDefaultSpecification,
                                                  ObjectExistsByRowsSpecification)


class BreakingRepository(CoreRepository[BreakingOrm]):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        super().__init__(session_factory=session_factory, model_orm=BreakingOrm)

    async def get(self, specification_filter: type[Specification] = ObjectExistsByRowsSpecification,
                  specification_sort: type[Specification] = OrderByRowsDefaultSpecification,
                  **rows: dict[str, Any]) -> Sequence[BreakingOrm] | None:
        try:
            async with self._session_factory() as session:
                stmt = (select(self._model_orm)
                        .options(selectinload(self._model_orm.services))
                        .where(specification_filter.is_satisfied(self._model_orm, rows))
                        .order_by(specification_sort.is_satisfied(self._model_orm, rows)))
                instance = await session.execute(stmt)
                result = instance.scalars().all()
                database_logger.info(f'Данные из таблицы {self._model_orm} по {rows=} получены')
                return result

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при получении услуги и поломки через relationship'
                                  f'из таблицы:{self._model_orm}'
                                  f'по rows:{rows}: {e}')
            return None

