from typing import Type
import asyncio

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from core import CoreRepository
from pedant_killer.database.database import database_logger, connection
from pedant_killer.database.specification import Specification, ObjectExistsByIdSpecification
from pedant_killer.database.models.user import UserOrm
from pedant_killer.database.models.access_level import AccessLevelOrm


class UserRepository(CoreRepository):
    @connection
    async def get_master(self, session: AsyncSession, model: Type[UserOrm], instance_id: int,
                         specification: Type[Specification] = ObjectExistsByIdSpecification
                         ) -> [UserOrm | None]:
        try:
            stmt = (select(model)
                    .options(selectinload(model.orders_master),
                             selectinload(model.orders_client),
                             joinedload(model.access_level)
                             )
                    .filter_by(**await specification.is_satisfied(self, model, instance_id))
                    .filter(AccessLevelOrm.importance == 30)
                    .join(AccessLevelOrm, model.access_level_id == AccessLevelOrm.id)
                    )

            instance = await session.execute(stmt)
            result = instance.scalars().all()

            return result

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при получении заказов через relationship'
                                  f'из таблицы:{model}'
                                  f'по id:{instance_id}: {e}')

            return None

    @connection
    async def get_client(self, session: AsyncSession, model: Type[UserOrm], instance_id: int,
                                specification: Type[Specification] = ObjectExistsByIdSpecification
                                ) -> [UserOrm | None]:
        try:
            stmt = (select(model)
                    .options(selectinload(model.orders_master),
                             selectinload(model.orders_client),
                             joinedload(model.access_level)
                             )
                    .filter_by(**await specification.is_satisfied(self, model, instance_id))
                    .filter(AccessLevelOrm.importance == 10)
                    .join(AccessLevelOrm, model.access_level_id == AccessLevelOrm.id)
                    )

            instance = await session.execute(stmt)
            result = instance.scalars().all()

            return result

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при получении заказов через relationship'
                                  f'из таблицы:{model}'
                                  f'по id:{instance_id}: {e}')
            return None

    @connection
    async def get_access_level(self, session: AsyncSession, model: Type[UserOrm], instance_id: int,
                               specification: Type[Specification] = ObjectExistsByIdSpecification) -> [UserOrm | None]:
        try:
            stmt = (select(model)
                    .options(joinedload(model.access_level))
                    .filter_by(**await specification.is_satisfied(self, model, instance_id))
                    )
            instance = await session.execute(stmt)
            result = instance.scalars().first()

            return result

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при получении уровня доступа через relationship'
                                  f'из таблицы:{model}'
                                  f'по id:{instance_id}: {e}')
            return None