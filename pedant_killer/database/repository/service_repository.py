from typing import Sequence
import asyncio

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError

from pedant_killer.database.repository.core_repository import CoreRepository
from pedant_killer.database.database import database_logger
from pedant_killer.database.models.service_orm import ServiceOrm
from pedant_killer.database.models.breaking_orm import BreakingOrm
from pedant_killer.database.models.service_breaking import ServiceBreakingOrm


class ServiceRepository(CoreRepository[ServiceOrm]):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        super().__init__(session_factory=session_factory, model_orm=ServiceOrm)

    async def save_service_breaking(self, service_id: int, breaking_id: int) -> int | None:
        try:
            async with self._session_factory() as session:
                stmt_service = select(ServiceOrm).options(selectinload(ServiceOrm.breaking)).filter_by(id=service_id)
                stmt_breaking = select(BreakingOrm).options(selectinload(BreakingOrm.service)).filter_by(id=breaking_id)

                service_result = await session.execute(stmt_service)
                breaking_result = await session.execute(stmt_breaking)

                service_orm = service_result.scalars().first()
                breaking_orm = breaking_result.scalars().first()

                service_orm.breaking.append(breaking_orm)
                await session.commit()
                await session.refresh(service_orm)

                stmt_service_breaking = select(ServiceBreakingOrm).where(
                    ServiceBreakingOrm.service_id == service_id,
                    ServiceBreakingOrm.breaking_id == breaking_id)

                service_breaking_result = await session.execute(stmt_service_breaking)
                service_breaking_orm = service_breaking_result.scalars().first()

                return service_breaking_orm.id

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при создании связи между таблицами service и breaking: {e}')

            return None

    async def get_breaking(self, service_id: int | list[int]) -> Sequence[ServiceOrm] | None:
        try:
            async with self._session_factory() as session:
                stmt = (select(self._model_orm)
                        .options(selectinload(self._model_orm.breaking))
                        .where(self._model_orm.id.in_(service_id))
                        )
                instance = await session.execute(stmt)
                result = instance.scalars().all()

                return result

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при получении услуги и поломки через relationship'
                                  f'из таблицы:{self._model_orm}'
                                  f'по id:{service_id}: {e}')
            return None

