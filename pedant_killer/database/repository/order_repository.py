import asyncio

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from pedant_killer.database.repository.core_repository import CoreRepository
from pedant_killer.database.database import database_logger
from pedant_killer.database.specification import Specification, ObjectExistsByRowsSpecification
from pedant_killer.database.models.device_service_orm import DeviceServiceOrm
from pedant_killer.database.models.order_orm import OrderOrm


class OrderRepository(CoreRepository[OrderOrm]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model_orm=OrderOrm)

    async def save_order_device_service(self, order_id: int, device_service_id: int,
                                        specification: type[Specification] = ObjectExistsByRowsSpecification
                                        ) -> 'OrderOrm | None':
        try:
            async with self._session as session:
                stmt_order = (select(self._model_orm)
                              .options(joinedload(self._model_orm.device_service))
                              .filter_by(**await specification.is_satisfied(self, self._model_orm, order_id)))
                stmt_device_service = (select(DeviceServiceOrm)
                                       .options(joinedload(DeviceServiceOrm.order))
                                       .filter_by(**await specification.is_satisfied(self,
                                                                                     DeviceServiceOrm,
                                                                                     device_service_id)
                                                  )
                                       )
            async with asyncio.TaskGroup() as tg:
                order_task = tg.create_task(session.execute(stmt_order))
                device_service_task = tg.create_task(session.execute(stmt_device_service))

            order = await order_task
            device_service = await device_service_task

            order_result = order.scalars().first()
            device_service_result = device_service.scalars().first
            order_result.device_service.append(device_service_result)  # type: ignore
            #await self._session.flush()
            await session.commit()
            await session.refresh(order_result)
            return order_result

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при создании связи между таблицами order и device_service: {e}')

            return None

    async def get_order_device_service(self, instance_id: int,
                                       specification: type[Specification] = ObjectExistsByRowsSpecification
                                       ) -> 'OrderOrm | None':
        try:
            async with self._session as session:
                stmt = (select(self._model_orm)
                        .options(selectinload(self._model_orm.device_service))
                        .filter_by(**await specification.is_satisfied(self, self._model_orm, instance_id))
                        )

                instance = await session.execute(stmt)
                result = instance.scalars().first()

                return result

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при получении device_service через relationship'
                                  f'из таблицы:{self._model_orm}'
                                  f'по id:{instance_id}: {e}')

            return None

    async def get_client(self, instance_id: int,
                         specification: type[Specification] = ObjectExistsByRowsSpecification
                         ) -> 'OrderOrm | None':
        try:
            async with self._session as session:
                stmt = (select(self._model_orm)
                        .options(joinedload(self._model_orm.user_client),
                                 joinedload(self._model_orm.user_master)
                                 )
                        .filter_by(**await specification.is_satisfied(self, self._model_orm, instance_id))
                        )

                instance = await session.execute(stmt)
                result = instance.scalars().first()

                return result

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при получении заказов через relationship'
                                  f'из таблицы:{self._model_orm}'
                                  f'по id:{instance_id}: {e}')

            return None

    async def get_master(self, instance_id: int,
                         specification: type[Specification] = ObjectExistsByRowsSpecification
                         ) -> 'OrderOrm | None':
        try:
            async with self._session as session:
                stmt = (select(self._model_orm)
                        .options(joinedload(self._model_orm.user_client),
                                 joinedload(self._model_orm.user_master)
                                 )
                        .filter_by(**await specification.is_satisfied(self, self._model_orm, instance_id))
                        )

                instance = await session.execute(stmt)
                result = instance.scalars().first()

                return result

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при получении заказов через relationship'
                                  f'из таблицы:{self._model_orm}'
                                  f'по id:{instance_id}: {e}')

            return None

    async def get_status(self, instance_id: int,
                         specification: type[Specification] = ObjectExistsByRowsSpecification
                         ) -> 'OrderOrm | None':
        try:
            async with self._session as session:
                stmt = (select(self._model_orm)
                        .options(joinedload(self._model_orm.status))
                        .filter_by(**await specification.is_satisfied(self, self._model_orm, instance_id))
                        )

                instance = await session.execute(stmt)
                result = instance.scalars().first()

                return result

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при получении статуса заказа через relationship'
                                  f'из таблицы:{self._model_orm}'
                                  f'по id:{instance_id}: {e}')

            return None

    async def get_device_service(self, instance_id: int,
                                 specification: type[Specification] = ObjectExistsByRowsSpecification
                                 ) -> 'OrderOrm | None':
        try:
            async with self._session as session:
                stmt = (select(self._model_orm)
                        .options(joinedload(self._model_orm.device_service))
                        .filter_by(**await specification.is_satisfied(self, self._model_orm, instance_id))
                        )

                instance = await session.execute(stmt)
                result = instance.scalars().first()

                return result

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при получении устройства и услуги через relationship'
                                  f'из таблицы:{self._model_orm}'
                                  f'по id:{instance_id}: {e}')

            return None
