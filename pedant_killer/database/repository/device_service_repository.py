import asyncio
from typing import Sequence

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from pedant_killer.database.repository.core_repository import CoreRepository
from pedant_killer.database.database import database_logger
from pedant_killer.database.models.device_orm import DeviceOrm
from pedant_killer.database.models.manufacturer_device_type_orm import ManufacturerDeviceTypeOrm
from pedant_killer.database.models.device_service_orm import DeviceServiceOrm
from pedant_killer.database.models.order_orm import OrderOrm


class DeviceServiceRepository(CoreRepository[DeviceServiceOrm]):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        super().__init__(session_factory=session_factory, model_orm=DeviceServiceOrm)

    async def save_device_service_order(self, order_id: int,
                                        device_service_id: int,
                                        ) -> int | None:
        try:
            async with self._session_factory() as session:
                stmt_order = (select(OrderOrm)
                              .options(joinedload(OrderOrm.device_service))
                              .filter_by(id=order_id))
                stmt_device_service = (select(self._model_orm)
                                       .options(joinedload(self._model_orm.order))
                                       .filter_by(id=device_service_id))

                async with asyncio.TaskGroup() as tg:
                    order_task = tg.create_task(session.execute(stmt_order))
                    device_service_task = tg.create_task(session.execute(stmt_device_service))

                order = await order_task
                device_service = await device_service_task

                order_orm = order.scalars().first()
                device_service_orm = device_service.scalars().first()
                device_service.order.append(order_orm)
                #await self._session.flush() #TODO: Проверить, нужна ли строчка
                await session.commit()
                await session.refresh(device_service_orm)
                return device_service_orm.id

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при создании связи между таблицами order и device_service: {e}')

            return None

    async def get_order(self, instance_id: int) -> 'Sequence[DeviceServiceOrm] | None':
        try:
            async with self._session_factory() as session:
                stmt = (select(self._model_orm)
                        .options(selectinload(self._model_orm.order))
                        .filter_by(id=instance_id)
                        )

                instance = await session.execute(stmt)
                result = instance.scalars().all()

                return result

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при получении заказов через relationship'
                                  f'из таблицы:{self._model_orm}'
                                  f'по id:{instance_id}: {e}')

            return None

    async def get_device(self, instance_id: int) -> 'Sequence[DeviceServiceOrm] | None':
        try:
            async with self._session_factory() as session:
                stmt = (select(self._model_orm).options(
                    joinedload(self._model_orm.device)
                    .joinedload(DeviceOrm.manufacturer_device_type)
                    .joinedload(ManufacturerDeviceTypeOrm.manufacturer),

                    joinedload(self._model_orm.device)
                    .joinedload(DeviceOrm.manufacturer_device_type)
                    .joinedload(ManufacturerDeviceTypeOrm.device_type)
                )
                        .filter_by(id=instance_id))
                instance = await session.execute(stmt)
                result = instance.scalars().all()
                return result

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при получении устройства через relationship из таблицы:'
                                  f' {self._model_orm} по id:'
                                  f' {instance_id}: {e}')
            return None

    async def get_service(self, instance_id: int) -> 'DeviceServiceOrm | None':
        try:
            async with self._session_factory() as session:
                stmt = (select(self._model_orm).options(joinedload(self._model_orm.service))
                        .filter_by(id=instance_id))
                instance = await session.execute(stmt)
                result = instance.scalars().first()

                return result

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при получении устройства через relationship из таблицы: {self._model_orm}'
                                  f' по id:'
                                  f' {instance_id}: {e}')
            return None

    async def get_device_service(self, instance_id: int) -> 'DeviceServiceOrm | None':
        try:
            async with self._session_factory() as session:
                stmt = (select(self._model_orm)
                        .options(
                            joinedload(self._model_orm.device)
                            .joinedload(DeviceOrm.manufacturer_device_type)
                            .joinedload(ManufacturerDeviceTypeOrm.manufacturer),

                            joinedload(self._model_orm.device)
                            .joinedload(DeviceOrm.manufacturer_device_type)
                            .joinedload(ManufacturerDeviceTypeOrm.device_type),

                            joinedload(self._model_orm.service)
                        )
                        .filter_by(id=instance_id))
                instance = await session.execute(stmt)
                result = instance.scalars().first()

                return result

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при получении устройства и услуги через relationship'
                                  f'из таблицы:{self._model_orm}'
                                  f'по id:{instance_id}: {e}')
            return None
