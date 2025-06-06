from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from pedant_killer.database.repository.core_repository import CoreRepository
from pedant_killer.database.models.manufacturer_orm import ManufacturerOrm


class ManufacturerRepository(CoreRepository[ManufacturerOrm]):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        super().__init__(session_factory=session_factory, model_orm=ManufacturerOrm)

