from typing import Type

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from core import CoreRepository
from pedant_killer.database.database import database_logger, connection
from pedant_killer.database.specification import Specification, ObjectExistsByIdSpecification
from pedant_killer.database.models.device_type import DeviceTypeOrm
from pedant_killer.database.models.manufacturer_device_type import ManufacturerDeviceTypeOrm


class ManufacturerDeviceTypeRepository(CoreRepository):
    @connection
    async def get_manufacturer(self, session: AsyncSession, model: Type[ManufacturerDeviceTypeOrm], instance_id: int,
                               specification: Type[Specification] = ObjectExistsByIdSpecification
                               ) -> [ManufacturerDeviceTypeOrm | None]:
        try:
            stmt = (select(model).options(joinedload(model.manufacturer))
                    .filter_by(**await specification.is_satisfied(self, model, instance_id)))
            instance = await session.execute(stmt)
            result = instance.scalars().first()
            database_logger.info(f'Данные из таблицы {model} с устройствами получены')  # TODO: Добавить проверку существует ли manufacturer с таким id
            return result

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при получении устройства через relationship из таблицы: {model} по id:'
                                  f' {instance_id}: {e}')
            return None

    @connection
    async def get_device_type(self, session: AsyncSession, model: Type[ManufacturerDeviceTypeOrm], instance_id: int,
                              specification: Type[Specification] = ObjectExistsByIdSpecification
                              ) -> [DeviceTypeOrm | None]:
        try:
            stmt = (select(model).options(joinedload(model.device_type))
                    .filter_by(**await specification.is_satisfied(self, model, instance_id)))
            instance = await session.execute(stmt)
            result = instance.scalars().first()
            return result

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при получении типа устройства через relationship из таблицы: {model} по id:'
                              f' {instance_id}: {e}')
            return None

    @connection
    async def get_manufacturer_device_type(self, session: AsyncSession, model: Type[ManufacturerDeviceTypeOrm],
                                                instance_id: int,
                                                specification: Type[Specification] = ObjectExistsByIdSpecification
                                               ) -> [ManufacturerDeviceTypeOrm | None]:
        try:
            stmt = (select(model)
                    .options(joinedload(model.manufacturer), joinedload(model.device_type))
                    .filter_by(**await specification.is_satisfied(self, model, instance_id)))
            instance = await session.execute(stmt)
            result = instance.scalars().first()
            return result

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при получении типа устройства и устройства через relationship'
                                  f'из таблицы:{model}'
                                  f'по id:{instance_id}: {e}')
            return None


