from typing import Any, Sequence

from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from sqlalchemy import select, delete
from pedant_killer.database.database import database_logger, Base
from pedant_killer.database.specification import (Specification,
                                                  ObjectExistsByRowsSpecification, OrderByRowsDefaultSpecification)


class CoreRepository[T: Base]:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession], model_orm: type[T]) -> None:
        self._session_factory = session_factory
        self._model_orm = model_orm

    async def save(self, **kwargs: Any) -> int | None:
        try:
            async with self._session_factory() as session:
                instance = self._model_orm(**kwargs)
                session.add(instance)
                await session.commit()
                database_logger.info(f'Запись добавлена в таблицу {self._model_orm}')
                await session.refresh(instance)
                return instance.id  # type: ignore
        except SQLAlchemyError as e:
            await session.rollback()
            database_logger.error(f'Ошибка при добавлении записи в таблицу {self._model_orm}: {e}')
            return None

    async def get(self, specification_filter: type[Specification] = ObjectExistsByRowsSpecification,
                  specification_sort: type[Specification] = OrderByRowsDefaultSpecification,
                  **rows: dict[str, Any]) -> Sequence[T] | None:
        try:
            async with self._session_factory() as session:
                stmt = (select(self._model_orm)
                        .where(await specification_filter.is_satisfied(self._model_orm, rows))
                        .order_by(await specification_sort.is_satisfied(self._model_orm, rows)))
                instance = await session.execute(stmt)
                result = instance.scalars().all()
                database_logger.info(f'Данные из таблицы {self._model_orm} по {rows=} получены')
                return result

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при получении данных из таблицы {self._model_orm} по {rows=}: {e}')
            return None

    async def delete(self, specification: type[Specification] = ObjectExistsByRowsSpecification,
                     **row) -> bool | None:
        try:
            async with self._session_factory() as session:
                stmt = delete(self._model_orm).where(await specification.is_satisfied(self._model_orm, row))
                await session.execute(stmt)
                await session.commit()
                database_logger.info(f'Удалена запись с id: {row=} из таблицы {self._model_orm}')
                return True
        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при удалении записи из таблицы: {self._model_orm} по id: {row=}: {e}')
            await session.rollback()
            return None

    async def update(self, **rows: dict[str, Any]) -> T | None:
        try:
            async with self._session_factory() as session:
                instance_id = rows.get('id', None)
                rows.pop('id')
                stmt = select(self._model_orm).filter_by(id=instance_id)
                result = await session.execute(stmt)
                obj = result.scalars().one()
                for key, value in rows.items():
                    setattr(obj, key, value)
                await session.commit()
                await session.refresh(obj)
                database_logger.info(f'Обновлена информация в таблице: {self._model_orm} по id: {instance_id}')
                return obj

        except NoResultFound:
            database_logger.info(f'Запись с id: {instance_id} не найдена в таблице: {self._model_orm}')
            return None

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при обновлении записи из таблицы: {self._model_orm} по id:'
                                  f' {instance_id}: {e}')
            await session.rollback()
            return None
