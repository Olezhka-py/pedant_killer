from typing import TYPE_CHECKING

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from pedant_killer.database.repository.core_repository import CoreRepository
from pedant_killer.database.database import database_logger
from pedant_killer.database.specification import Specification, ObjectExistsByRowsSpecification
from pedant_killer.database.models.manufacturer_device_type_orm import ManufacturerDeviceTypeOrm


class ManufacturerDeviceTypeRepository(CoreRepository[ManufacturerDeviceTypeOrm]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model_orm=ManufacturerDeviceTypeOrm)

    async def get_manufacturer(self, instance_id: int,
                               specification: type[Specification] = ObjectExistsByRowsSpecification
                               ) -> 'ManufacturerDeviceTypeOrm | None':
        try:
            async with self._session as session:
                stmt = (select(self._model_orm).options(joinedload(self._model_orm.manufacturer))
                        .filter_by(**await specification.is_satisfied(self, self._model_orm, instance_id)))
                instance = await session.execute(stmt)
                result = instance.scalars().first()
                database_logger.info(f'Данные из таблицы {self._model_orm} с устройствами получены')  # TODO: Добавить проверку существует ли manufacturer с таким id
                return result

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при получении устройства через relationship из таблицы:'
                                  f' {self._model_orm} по id:'
                                  f' {instance_id}: {e}')
            return None

    async def get_device_type(self, instance_id: int,
                              specification: type[Specification] = ObjectExistsByRowsSpecification
                              ) -> 'ManufacturerDeviceTypeOrm | None':
        try:
            async with self._session as session:
                stmt = (select(self._model_orm).options(joinedload(self._model_orm.device_type))
                        .filter_by(**await specification.is_satisfied(self, self._model_orm, instance_id)))
                instance = await session.execute(stmt)
                result = instance.scalars().first()
                return result

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при получении типа устройства через relationship из таблицы:'
                                  f' {self._model_orm} по id:'
                                  f' {instance_id}: {e}')
            return None

    async def get_manufacturer_device_type(self,
                                           instance_id: int,
                                           specification: type[Specification] = ObjectExistsByRowsSpecification
                                           ) -> 'ManufacturerDeviceTypeOrm | None':
        try:
            async with self._session as session:
                stmt = (select(self._model_orm)
                        .options(joinedload(self._model_orm.manufacturer), joinedload(self._model_orm.device_type))
                        .filter_by(**await specification.is_satisfied(self, self._model_orm, instance_id)))
                instance = await session.execute(stmt)
                result = instance.scalars().first()
                return result

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при получении типа устройства и устройства через relationship'
                                  f'из таблицы:{self._model_orm}'
                                  f'по id:{instance_id}: {e}')
            return None
