from sqlalchemy.ext.asyncio import AsyncSession

from pedant_killer.database.repository.core_repository import CoreRepository
from pedant_killer.database.models.service_orm import ServiceOrm


class ServiceRepository(CoreRepository[ServiceOrm]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model_orm=ServiceOrm)

