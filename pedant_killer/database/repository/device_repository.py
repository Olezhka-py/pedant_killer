from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from pedant_killer.database.repository.core_repository import CoreRepository
from pedant_killer.database.database import database_logger
from pedant_killer.database.specification import Specification, ObjectExistsByRowsSpecification
from pedant_killer.database.models.manufacturer_device_type_orm import ManufacturerDeviceTypeOrm
from pedant_killer.database.models.device_orm import DeviceOrm


class DeviceRepository(CoreRepository[DeviceOrm]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model_orm=DeviceOrm)

    async def get_manufacturer_device_type(self, instance_id: int,
                                           specification: type[Specification] = ObjectExistsByRowsSpecification
                                           ) -> 'DeviceOrm | None':
        try:
            async with self._session as session:
                stmt = (select(self._model_orm)
                        .options(
                            joinedload(self._model_orm.manufacturer_device_type)
                            .joinedload(ManufacturerDeviceTypeOrm.manufacturer),

                            joinedload(self._model_orm.manufacturer_device_type)
                            .joinedload(ManufacturerDeviceTypeOrm.device_type)
                        )
                        .filter_by(**await specification.is_satisfied(self, self._model_orm, instance_id)))
                instance = await session.execute(stmt)
                result = instance.scalars().first()
                return result

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при получении типа устройства и устройства через relationship'
                                  f'из таблицы:{self._model_orm}'
                                  f'по id:{instance_id}: {e}')
        return None
