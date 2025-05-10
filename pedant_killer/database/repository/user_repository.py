from typing import Sequence, Any

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from pedant_killer.database.models import OrderOrm
from pedant_killer.database.repository.core_repository import CoreRepository
from pedant_killer.database.database import database_logger
from pedant_killer.database.models.user_orm import UserOrm
from pedant_killer.database.specification import (Specification,
                                                  ObjectExistsByRowsSpecification,
                                                  OrderByRowsDefaultSpecification)


class UserRepository(CoreRepository[UserOrm]):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        super().__init__(session_factory=session_factory, model_orm=UserOrm)

    async def get(self, specification_filter: type[Specification] = ObjectExistsByRowsSpecification,
                  specification_sort: type[Specification] = OrderByRowsDefaultSpecification,
                  **rows: dict[str, Any]) -> Sequence[UserOrm] | None:
        try:
            async with self._session_factory() as session:
                stmt = (select(self._model_orm)
                        .options(
                            selectinload(self._model_orm.orders_master)
                            .joinedload(OrderOrm.status),
                            selectinload(self._model_orm.orders_master)
                            .joinedload(OrderOrm.device_service),

                            selectinload(self._model_orm.orders_client)
                            .joinedload(OrderOrm.status),
                            selectinload(self._model_orm.orders_client)
                            .joinedload(OrderOrm.device_service),

                            joinedload(self._model_orm.access_level)
                        )
                        .where(await specification_filter.is_satisfied(self._model_orm, rows))
                        .order_by(await specification_sort.is_satisfied(self._model_orm, rows)))
                instance = await session.execute(stmt)
                result = instance.scalars().all()
                database_logger.info(f'Данные из таблицы {self._model_orm} по {rows=} получены')
                return result

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при получении данных из таблицы {self._model_orm} по {rows=}: {e}')
            return None