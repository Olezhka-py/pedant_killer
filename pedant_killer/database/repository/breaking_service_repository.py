from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from pedant_killer.database.models.service_breaking_orm import ServiceBreakingOrm
from pedant_killer.database.repository import CoreRepository


class BreakingServiceRepository(CoreRepository):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        super().__init__(session_factory=session_factory, model_orm=ServiceBreakingOrm)