from typing import Type


from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from core import CoreRepository
from pedant_killer.database.database import database_logger, connection
from pedant_killer.database.specification import Specification, ObjectExistsByIdSpecification
from pedant_killer.database.models.device import DeviceOrm
from pedant_killer.database.models.manufacturer_device_type import ManufacturerDeviceTypeOrm


class DeviceRepository(CoreRepository):
    @connection
    async def get_manufacturer_device_type(self, session: AsyncSession,
                                           model: Type[DeviceOrm],
                                           instance_id: int,
                                           specification: Type[Specification] = ObjectExistsByIdSpecification
                                           ) -> [ManufacturerDeviceTypeOrm | None]:
        try:
            stmt = (select(model)
                    .options(
                        joinedload(model.manufacturer_device_type)
                        .joinedload(ManufacturerDeviceTypeOrm.manufacturer),

                        joinedload(model.manufacturer_device_type)
                        .joinedload(ManufacturerDeviceTypeOrm.device_type)
                    )
                    .filter_by(**await specification.is_satisfied(self, model, instance_id)))
            instance = await session.execute(stmt)
            result = instance.scalars().first()
            return result

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при получении типа устройства и устройства через relationship'
                                  f'из таблицы:{model}'
                                  f'по id:{instance_id}: {e}')
        return None

