from sqlalchemy.ext.asyncio import AsyncSession

from pedant_killer.database.models.access_level_orm import AccessLevelOrm
from pedant_killer.database.repository.core_repository import CoreRepository


class AccessLevelRepository(CoreRepository[AccessLevelOrm]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model_orm=AccessLevelOrm)
