from typing import List, Any, Type

from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy import select, text, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from pedant_killer.database.models import *
from pedant_killer.database.specification import Specification, ObjectExistsByIdSpecification
from pedant_killer.database.database import async_session_factory, connection, database_logger


class CoreRepository:
    @connection
    async def save(self, session: AsyncSession, model: Type[Base], **kwargs: Any) -> [int | None]:
        try:
            instance = model(**kwargs)
            session.add(instance)
            await session.commit()
            database_logger.info(f'Запись добавлена в таблицу {model}')
            await session.refresh(instance)
            return instance.id  # type: ignore
        except SQLAlchemyError as e:
            await session.rollback()
            database_logger.error(f'Ошибка при добавлении записи в таблицу {model}: {e}')
            return None

    @connection
    async def get_without_checks(self, session: AsyncSession, model: Type[Base], instance_id: int) -> [Base | None]:
        try:
            stmt = select(model).filter_by(id=instance_id)
            instance = await session.execute(stmt)
            return instance.scalars().first()

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при получении записи из таблицы {model} по {instance_id}: {e}')
            return None

    @connection
    async def get(self, session: AsyncSession, model: Type[Base], instance_id: int,
                  specification: Type[Specification] = ObjectExistsByIdSpecification) -> [Base | None]:
        try:
            stmt = select(model).filter_by(**await specification.is_satisfied(self, model, instance_id))
            instance = await session.execute(stmt)
            result = instance.scalars().first()
            database_logger.info(f'Данные из таблицы {model} по {instance_id} получены')
            return result
        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при получении данных из таблицы {model} по {instance_id}: {e}')
            return None

        # добавить, если не нашлось

    @connection
    async def get_all(self, session: AsyncSession, model: Base) -> [List[Base] | None]:
        try:
            stmt = select(model)
            result = await session.execute(stmt)
            item = result.scalars().all()
            database_logger.info(f'Данные из таблицы {model} получены')
            return item
        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при получении данных из таблицы {model}: {e}')
            return None

    @connection
    async def delete(self, session: AsyncSession, model: Type[Base],
                     instance_id: int, specifications: Type[Specification] = ObjectExistsByIdSpecification
                     ) -> [Type[Base] | None]:
        try:
            stmt = delete(model).filter_by(**await specifications.is_satisfied(self, model, instance_id))
            await session.execute(stmt)
            await session.commit()
            database_logger.info(f'Удалена запись с id: {instance_id} из таблицы {model}')
        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при удалении записи из таблицы: {model} по id: {instance_id}: {e}')
            await session.rollback()
            return None

    @connection
    async def delete_all(self, session: AsyncSession, model: Type[Base]) -> [Type[Base] | None]:
        try:
            stmt = delete(model)
            await session.execute(stmt)
            await session.commit()
            database_logger.info(f'Удалены все записи из таблицы: {model}')
            return model
        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при удалении всех записей из таблицы: {model}: {e}')
            await session.rollback()
            return None

    @connection
    async def update(self, session: AsyncSession, model: Base, instance_id: int,  **kwargs: Any) -> [Type[Base] | None]:
        try:
            stmt = select(model).filter_by(id=instance_id)
            result = await session.execute(stmt)
            obj = result.scalars().one()
            for key, value in kwargs.items():
                setattr(obj, key, value)
            await session.commit()
            await session.refresh(obj)
            database_logger.info(f'Обновлена информация в таблице: {model} по id: {instance_id}')
            return obj

        except NoResultFound:
            database_logger.info(f'Запись с id: {instance_id} не найдена в таблице: {model}')
            return None

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при обновлении записи из таблицы: {model} по id: {instance_id}: {e}')
            await session.rollback()
            return None


class ManufacturerRepository(CoreRepository):
    pass


class DeviceTypeRepository(CoreRepository):
    pass


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


class ServiceRepository(CoreRepository):
    pass


class DeviceServiceRepository(CoreRepository):
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


class OrderDeviceServiceRepository(CoreRepository):
    pass


class OrderStatusRepository(CoreRepository):
    pass


class OrderRepository(CoreRepository):
    pass


class UserRepository(CoreRepository):
    @connection
    async def get_orders(self, session: AsyncSession, model: Type[UserOrm], instance_id: int,
                         specification: Type[Specification] = ObjectExistsByIdSpecification
                         ) -> [UserOrm | None]:
        try:
            stmt = (select(model)
                    .options(selectinload(model.orders_client),
                             selectinload(model.orders_master),
                             joinedload(model.access_level)
                             )
                    .filter_by(**await specification.is_satisfied(self, model, instance_id)))

            instance = await session.execute(stmt)
            result = instance.scalars().all()

            return result

        except SQLAlchemyError:
            pass


class AccessLevelRepository(CoreRepository):
    pass

