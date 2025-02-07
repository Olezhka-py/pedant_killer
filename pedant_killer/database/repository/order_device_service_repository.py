from sqlalchemy.ext.asyncio import AsyncSession

from pedant_killer.database.repository.core_repository import CoreRepository
from pedant_killer.database.models.order_device_service_orm import OrderDeviceServiceOrm


class OrderDeviceServiceRepository(CoreRepository[OrderDeviceServiceOrm]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model_orm=OrderDeviceServiceOrm)
