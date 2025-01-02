from typing import Type
import asyncio

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from pedant_killer.database.repository import CoreRepository
from pedant_killer.database.database import database_logger, connection
from pedant_killer.database.specification import Specification, ObjectExistsByIdSpecification
from pedant_killer.database.models.device_service import DeviceServiceOrm
from pedant_killer.database.models.order import OrderOrm
from pedant_killer.database.models.device import DeviceOrm
from pedant_killer.database.models.manufacturer_device_type import ManufacturerDeviceTypeOrm


class DeviceServiceRepository(CoreRepository):
    @connection
    async def save_device_service_order(self, session: AsyncSession, model_order: Type[OrderOrm],
                                        model_device_service: Type[DeviceServiceOrm], order_id: int,
                                        device_service_id: int,
                                        specification: Type[Specification] = ObjectExistsByIdSpecification
                                        ) -> [DeviceServiceOrm | None]:
        try:
            stmt_order = (select(model_order)
                          .options(joinedload(model_order.device_service))
                          .filter_by(**await specification.is_satisfied(self, model_order, order_id)))
            stmt_device_service = (select(model_device_service)
                                   .options(joinedload(model_device_service.order))
                                   .filter_by(**await specification.is_satisfied(self,
                                                                                 model_device_service,
                                                                                 device_service_id)
                                              )
                                   )
            async with asyncio.TaskGroup() as tg:
                order_task = tg.create_task(session.execute(stmt_order))
                device_service_task = tg.create_task(session.execute(stmt_device_service))

            order = await order_task
            device_service = await device_service_task

            order_orm = order.scalars().first()
            device_service_orm = device_service.scalars().first()
            device_service_orm.order.append(order_orm)
            await session.flush()
            await session.commit()
            await session.refresh(order_orm)
            return order_orm

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при создании связи между таблицами order и device_service: {e}')

            return None

    @connection
    async def get_order(self, session: AsyncSession, model: Type[DeviceServiceOrm], instance_id: int,
                                       specification: Type[Specification] = ObjectExistsByIdSpecification
                                       ) -> [OrderOrm | None]:
        try:
            stmt = (select(model)
                    .options(selectinload(model.order))
                    .filter_by(**await specification.is_satisfied(self, model, instance_id))
                    )

            instance = await session.execute(stmt)
            result = instance.scalars().first()

            return result

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при получении заказов через relationship'
                                  f'из таблицы:{model}'
                                  f'по id:{instance_id}: {e}')

            return None

    @connection
    async def get_device(self, session: AsyncSession, model: Type[DeviceServiceOrm],
                         instance_id: int, specification: Type[Specification] = ObjectExistsByIdSpecification,
                         ) -> [DeviceServiceOrm | None]:
        try:
            stmt = (select(model).options(
                joinedload(model.device)
                .joinedload(DeviceOrm.manufacturer_device_type)
                .joinedload(ManufacturerDeviceTypeOrm.manufacturer),

                joinedload(model.device)
                .joinedload(DeviceOrm.manufacturer_device_type)
                .joinedload(ManufacturerDeviceTypeOrm.device_type)
            )
                    .filter_by(**await specification.is_satisfied(self, model, instance_id)))
            instance = await session.execute(stmt)
            result = instance.scalars().first()
            return result

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при получении устройства через relationship из таблицы: {model} по id:'
                                  f' {instance_id}: {e}')
            return None

    @connection
    async def get_service(self, session: AsyncSession, model: Type[DeviceServiceOrm],
                          instance_id: int, specification: Type[Specification] = ObjectExistsByIdSpecification,
                          ) -> [DeviceServiceOrm | None]:
        try:
            stmt = (select(model).options(joinedload(model.service))
                    .filter_by(**await specification.is_satisfied(self, model, instance_id)))
            instance = await session.execute(stmt)
            result = instance.scalars().first()
            return result

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при получении устройства через relationship из таблицы: {model} по id:'
                                  f' {instance_id}: {e}')
            return None

    @connection
    async def get_device_service(self, session: AsyncSession, model: Type[DeviceServiceOrm], instance_id: int,
                                 specification: Type[Specification] = ObjectExistsByIdSpecification
                                 ) -> [DeviceServiceOrm | None]:
        try:
            stmt = (select(model)
                    .options(
                        joinedload(model.device)
                        .joinedload(DeviceOrm.manufacturer_device_type)
                        .joinedload(ManufacturerDeviceTypeOrm.manufacturer),

                        joinedload(model.device)
                        .joinedload(DeviceOrm.manufacturer_device_type)
                        .joinedload(ManufacturerDeviceTypeOrm.device_type),

                        joinedload(model.service)
                    )
                    .filter_by(**await specification.is_satisfied(self, model, instance_id)))
            instance = await session.execute(stmt)
            result = instance.scalars().first()
            return result

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при получении устройства и услуги через relationship'
                                  f'из таблицы:{model}'
                                  f'по id:{instance_id}: {e}')
            return None
