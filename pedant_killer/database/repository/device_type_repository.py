from sqlalchemy.ext.asyncio import AsyncSession

from pedant_killer.database.repository.core_repository import CoreRepository
from pedant_killer.database.models.device_type_orm import DeviceTypeOrm


class DeviceTypeRepository(CoreRepository[DeviceTypeOrm]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model_orm=DeviceTypeOrm)
