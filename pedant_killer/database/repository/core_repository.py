from typing import Type, Any, List

from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select, delete
from pedant_killer.database.database import database_logger, connection, Base
from pedant_killer.database.specification import Specification, ObjectExistsByIdSpecification


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
    async def update(self, session: AsyncSession, model: Base, instance_id: int, **kwargs: Any) -> [Type[Base] | None]:
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

