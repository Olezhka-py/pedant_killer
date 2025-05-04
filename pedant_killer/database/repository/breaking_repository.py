import asyncio
from typing import Sequence

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from pedant_killer.database.repository.core_repository import CoreRepository
from pedant_killer.database.database import database_logger
from pedant_killer.database.models.service_orm import ServiceOrm
from pedant_killer.database.models.breaking_orm import BreakingOrm
from pedant_killer.database.models.service_breaking import ServiceBreakingOrm


class BreakingRepository(CoreRepository[BreakingOrm]):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        super().__init__(session_factory=session_factory, model_orm=BreakingOrm)

    async def save_breaking_service(self, service_id: int, breaking_id: int) -> int | None:
        try:
            async with self._session_factory() as session:
                stmt_service = select(ServiceOrm).options(selectinload(ServiceOrm.breaking)).filter_by(id=service_id)
                stmt_breaking = select(BreakingOrm).options(selectinload(BreakingOrm.service)).filter_by(id=breaking_id)

                service_result = await session.execute(stmt_service)
                breaking_result = await session.execute(stmt_breaking)

                service_orm = service_result.scalars().first()
                breaking_orm = breaking_result.scalars().first()

                breaking_orm.service.append(service_orm)
                await session.commit()
                await session.refresh(breaking_orm)

                stmt_service_breaking = select(ServiceBreakingOrm).where(
                    ServiceBreakingOrm.service_id == service_id,
                    ServiceBreakingOrm.breaking_id == breaking_id)

                service_breaking_result = await session.execute(stmt_service_breaking)
                service_breaking_orm = service_breaking_result.scalars().first()

                return service_breaking_orm.id

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при создании связи между таблицами service и breaking: {e}')

            return None

    async def get_service(self, instance_id: int) -> Sequence[BreakingOrm] | None:
        try:
            async with self._session_factory() as session:
                stmt = select(BreakingOrm).options(selectinload(BreakingOrm.service)).filter_by(id=instance_id)
                instance = await session.execute(stmt)
                result = instance.scalars().all()
                return result

        except SQLAlchemyError as e:
            database_logger.error(f'Ошибка при получении услуги и поломки через relationship'
                                  f'из таблицы:{self._model_orm}'
                                  f'по id:{instance_id}: {e}')
            return None

