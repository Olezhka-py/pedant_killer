from typing import Sequence, Any

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from pedant_killer.database.models import ServiceOrm
from pedant_killer.database.repository.core_repository import CoreRepository
from pedant_killer.database.database import database_logger
from pedant_killer.database.models.device_orm import DeviceOrm
from pedant_killer.database.models.manufacturer_device_type_orm import ManufacturerDeviceTypeOrm
from pedant_killer.database.models.device_service_orm import DeviceServiceOrm
from pedant_killer.database.specification import (Specification,
                                                  ObjectExistsByRowsSpecification,
                                                  OrderByRowsDefaultSpecification)


class DeviceServiceRepository(CoreRepository[DeviceServiceOrm]):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        super().__init__(session_factory=session_factory, model_orm=DeviceServiceOrm)

    async def get(self, specification_filter: type[Specification] = ObjectExistsByRowsSpecification,
                  specification_sort: type[Specification] = OrderByRowsDefaultSpecification,
                  **rows: dict[str, Any]) -> Sequence[DeviceServiceOrm] | None:
        try:
            async with self._session_factory() as session:
                stmt = (select(self._model_orm)
                        .options(
                    joinedload(self._model_orm.device)
                    .joinedload(DeviceOrm.manufacturer_device_type)
                    .options(joinedload(ManufacturerDeviceTypeOrm.manufacturer),
                             joinedload(ManufacturerDeviceTypeOrm.device_type)),

                    joinedload(self._model_orm.service)
                    .selectinload(ServiceOrm.breakings),

                    selectinload(self._model_orm.orders)
                )
                        .where(await specification_filter.is_satisfied(self._model_orm, rows))
                        .order_by(await specification_sort.is_satisfied(self._model_orm, rows)))
                instance = await session.execute(stmt)
                result = instance.scalars().all()
                database_logger.info(f'Данные из таблицы {self._model_orm} по {rows=} получены')
                return result

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при получении заказов через relationship'
                                  f'из таблицы:{self._model_orm}'
                                  f'по rows:{rows}: {e}')

            return None
