from typing import List, Any, Type

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, text, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from models import *
from specification import Specification
from database import async_session_factory, connection, database_logger


class CoreRepository:
    @connection
    async def save(self, session: AsyncSession, model: Type[Base], **kwargs: Any) -> [Base | None]:
        try:
            instance = model(**kwargs)
            session.add(instance)
            await session.commit()
            database_logger.info(f'Запись добавлена в таблицу {model}')
            return model
        except SQLAlchemyError as e:
            await session.rollback()
            database_logger.erorr(f'Ошибка при добавлении записи в таблицу {model}: {e}')
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
                  specification: Specification) -> [Base | None]:
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
            item = result.all()
            database_logger.info(f'Данные из таблицы {model} получены')
            return item
        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при получении данных из таблицы {model}: {e}')
            await session.rollback()
            return None

    @connection
    async def delete(self, session: AsyncSession, model: Type[Base],
                     instance_id: int, specifications: Type[Specification]) -> [Type[Base] | None]:
        try:
            stmt = delete(model).filter_by(**await specifications.is_satisfied(self, model, instance_id))
            await session.execute(stmt)
            await session.commit()
            database_logger.info(f'Удалена запись с id: {instance_id} из таблицы {model}')
            return model
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
    async def update(self, session: AsyncSession, model: Base, instance_id: int,
                     specification: Type[Specification], **kwargs: Any) -> [Base | None]:
        try:
            stmt = update(model).filter_by(**await specification.is_satisfied(self, model, instance_id)).values(**kwargs)
            instance = await session.execute(stmt)
            result = instance.scalars().first()
            await session.commit()
            database_logger.info(f'Обновлена информация в таблице: {model} по id: {instance_id}')
            return result
        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при обновлении записи из таблицы: {model} по id: {instance_id}: {e}')
            await session.rollback()
            return None





class ManufacturerRepository(CoreRepository):
    pass


class DeviceTypeRepository(CoreRepository):
    pass


class ManufacturerDeviceTypeRepository(CoreRepository):
    pass


class DeviceRepository(CoreRepository):
    pass


class ServiceRepository(CoreRepository):
    pass


class DeviceServiceRepository(CoreRepository):
    pass


class OrderDeviceServiceRepository(CoreRepository):
    pass


class OrderStatusRepository(CoreRepository):
    pass


class OrderRepository(CoreRepository):
    pass


class UserRepository(CoreRepository):
    pass


class AccessLevelRepository(CoreRepository):
    pass

