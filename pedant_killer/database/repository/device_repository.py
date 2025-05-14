from typing import Any, Sequence

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from pedant_killer.database.repository.core_repository import CoreRepository
from pedant_killer.database.database import database_logger
from pedant_killer.database.models.manufacturer_device_type_orm import ManufacturerDeviceTypeOrm
from pedant_killer.database.models.device_orm import DeviceOrm
from pedant_killer.database.specification import (Specification,
                                                  ObjectExistsByRowsSpecification,
                                                  OrderByRowsDefaultSpecification)


class DeviceRepository(CoreRepository[DeviceOrm]):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        super().__init__(session_factory=session_factory, model_orm=DeviceOrm)

    async def get(self, specification_filter: type[Specification] = ObjectExistsByRowsSpecification,
                  specification_sort: type[Specification] = OrderByRowsDefaultSpecification,
                  **rows: dict[str, Any]) -> Sequence[DeviceOrm] | None:
        try:
            async with self._session_factory() as session:
                stmt = (select(self._model_orm)
                        .options(
                            joinedload(self._model_orm.manufacturer_device_type)
                            .joinedload(ManufacturerDeviceTypeOrm.manufacturer),

                            joinedload(self._model_orm.manufacturer_device_type)
                            .joinedload(ManufacturerDeviceTypeOrm.device_type)
                        )
                        .where(specification_filter.is_satisfied(self._model_orm, rows))
                        .order_by(specification_sort.is_satisfied(self._model_orm, rows)))
                instance = await session.execute(stmt)
                result = instance.scalars().all()
                return result

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при получении типа устройства и устройства через relationship'
                                  f'из таблицы:{self._model_orm}'
                                  f'по rows:{rows}: {e}')
        return None
