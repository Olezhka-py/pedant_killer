from sqlalchemy.ext.asyncio import AsyncSession

from pedant_killer.database.repository.core_repository import CoreRepository
from pedant_killer.database.models.manufacturer_orm import ManufacturerOrm


class ManufacturerRepository(CoreRepository[ManufacturerOrm]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model_orm=ManufacturerOrm)

