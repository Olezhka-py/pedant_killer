from typing import Sequence, Any

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError

from pedant_killer.database.repository.core_repository import CoreRepository
from pedant_killer.database.database import database_logger
from pedant_killer.database.models.service_orm import ServiceOrm

from pedant_killer.database.specification import (Specification,
                                                  ObjectExistsByRowsSpecification,
                                                  OrderByRowsDefaultSpecification)


class ServiceRepository(CoreRepository[ServiceOrm]):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        super().__init__(session_factory=session_factory, model_orm=ServiceOrm)

    async def get(self, specification_filter: type[Specification] = ObjectExistsByRowsSpecification,
                  specification_sort: type[Specification] = OrderByRowsDefaultSpecification,
                  **rows: dict[str, Any]) -> Sequence[ServiceOrm] | None:
        try:
            async with self._session_factory() as session:
                stmt = (select(self._model_orm)
                        .options(selectinload(self._model_orm.breakings))
                        .where(await specification_filter.is_satisfied(self._model_orm, rows))
                        .order_by(await specification_sort.is_satisfied(self._model_orm, rows)))
                instance = await session.execute(stmt)
                result = instance.scalars().all()
                database_logger.info(f'Данные из таблицы {self._model_orm} по {rows=} получены')
                return result

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при получении данных из таблицы {self._model_orm} по {rows=}: {e}')
            return None
