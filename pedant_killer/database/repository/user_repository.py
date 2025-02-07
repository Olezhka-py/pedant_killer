from typing import Sequence

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from pedant_killer.database.repository.core_repository import CoreRepository
from pedant_killer.database.database import database_logger
from pedant_killer.database.specification import Specification, ObjectExistsByIdSpecification
from pedant_killer.database.models.user_orm import UserOrm
from pedant_killer.database.models.access_level_orm import AccessLevelOrm


class UserRepository(CoreRepository[UserOrm]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model_orm=UserOrm)

    async def get_master(self, instance_id: int,
                         specification: type[Specification] = ObjectExistsByIdSpecification
                         ) -> 'Sequence[UserOrm] | None':
        try:
            stmt = (select(self._model_orm)
                    .options(selectinload(self._model_orm.orders_master),
                             selectinload(self._model_orm.orders_client),
                             joinedload(self._model_orm.access_level)
                             )
                    .filter_by(**await specification.is_satisfied(self, self._model_orm, instance_id))
                    .filter(AccessLevelOrm.importance == 30)
                    .join(AccessLevelOrm, self._model_orm.access_level_id == AccessLevelOrm.id)
                    )

            instance = await self._session.execute(stmt)
            result = instance.scalars().all()

            return result

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при получении заказов через relationship'
                                  f'из таблицы:{self._model_orm}'
                                  f'по id:{instance_id}: {e}')

            return None

    async def get_client(self, instance_id: int,
                         specification: type[Specification] = ObjectExistsByIdSpecification
                         ) -> 'Sequence[UserOrm] | None':
        try:
            stmt = (select(self._model_orm)
                    .options(selectinload(self._model_orm.orders_master),
                             selectinload(self._model_orm.orders_client),
                             joinedload(self._model_orm.access_level)
                             )
                    .filter_by(**await specification.is_satisfied(self, self._model_orm, instance_id))
                    .filter(AccessLevelOrm.importance == 10)
                    .join(AccessLevelOrm, self._model_orm.access_level_id == AccessLevelOrm.id)
                    )

            instance = await self._session.execute(stmt)
            result = instance.scalars().all()

            return result

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при получении заказов через relationship'
                                  f'из таблицы:{self._model_orm}'
                                  f'по id:{instance_id}: {e}')
            return None

    async def get_access_level(self, instance_id: int,
                               specification: type[Specification] = ObjectExistsByIdSpecification
                               ) -> 'UserOrm | None':
        try:
            stmt = (select(self._model_orm)
                    .options(joinedload(self._model_orm.access_level))
                    .filter_by(**await specification.is_satisfied(self, self._model_orm, instance_id))
                    )
            instance = await self._session.execute(stmt)
            result = instance.scalars().first()

            return result

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при получении уровня доступа через relationship'
                                  f'из таблицы:{self._model_orm}'
                                  f'по id:{instance_id}: {e}')
            return None
