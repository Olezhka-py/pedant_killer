from typing import Any

import pydantic
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from pedant_killer.database.database import database_logger, connection, Base
from pedant_killer.database.specification import Specification, ObjectExistsByIdSpecification


class CoreRepository:
    def __init__(self, session: AsyncSession, model_class: type[Base]):
        # нижнее подчеркивание перед названием поля или метода обозначает, что он приватный
        self._session = session
        self._model_class = model_class

    async def create(self, dto: pydantic.BaseModel) -> Base:   
        try:
            instance = self._model_class(**dto.model_dump())
            self._session.add(instance)
            await self._session.commit()
            database_logger.info(f'Запись добавлена в таблицу {self._model_class}')
            await self._session.refresh(instance)
            return instance  # нужно вернуть созданный объект
        except SQLAlchemyError as e:
            await self._session.rollback()
            database_logger.error(f'Ошибка при добавлении записи в таблицу {self._model_class}: {e}')
            return None

    async def get_without_checks(self, instance_id: int) -> Base | None:
        try:
            stmt = select(self._model_class).filter_by(id=instance_id)
            instance = await self._session.execute(stmt)
            return instance.scalars().first()

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при получении записи из таблицы {self._model_class} по {instance_id}: {e}')
            return None

    async def get(
        self,
        instance_id: int,
        specification: type[Specification] = ObjectExistsByIdSpecification,
    ) -> Base | None:
        try:
            specification_compliance = await specification.is_satisfied(
                self,
                self._model_class,
                instance_id,
            )
            stmt = select(self._model_class).filter_by(**specification_compliance)
            instance = await self._session.execute(stmt)
            result = instance.scalars().first()
            database_logger.info(f'Данные из таблицы {self._model_class} по {instance_id} получены')
            return result
        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при получении данных из таблицы {self._model_class} по {instance_id}: {e}')
            return None

    async def get_all(self) -> list[Base]:
        try:
            stmt = select(self._model_class)
            result = await self._session.execute(stmt)
            items = result.scalars().all()
            database_logger.info(f'Данные из таблицы {self._model_class} получены')
            return items
        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при получении данных из таблицы {self._model_class}: {e}')
            return []

    async def delete(
        self,
        instance_id: int,
        specification: type[Specification] = ObjectExistsByIdSpecification,
    ) -> bool:
        try:
            specification_compliance = await specification.is_satisfied(
                self,
                self._model_class,
                instance_id,
            )
            stmt = delete(self._model_class).filter_by(**specification_compliance)
            await self._session.execute(stmt)
            await self._session.commit()
            database_logger.info(f'Удалена запись с id: {instance_id} из таблицы {model}')
            return True
        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при удалении записи из таблицы: {model} по id: {instance_id}: {e}')
            await self._session.rollback()

        return False

    # мне кажется, что в продакшене метод delete_all не будет использоваться, поэтому я его убрал

    async def update(self, instance_id: int, dto: pydantic.BaseModel) -> type[Base] | None:
        try:
            stmt = select(self._model_class).filter_by(id=instance_id)
            result = await self._session.execute(stmt)
            obj = result.scalars().one()

            for key, value in dto.model_dump():
                setattr(obj, key, value)

            await self._session.commit()
            await self._session.refresh(obj)
            database_logger.info(f'Обновлена информация в таблице: {self._model_class} по id: {instance_id}')
            return obj

        except NoResultFound:
            database_logger.info(f'Запись с id: {instance_id} не найдена в таблице: {self._model_class}')
            return None

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при обновлении записи из таблицы: {self._model_class} по id: {instance_id}: {e}')
            await self._session.rollback()
            return None

