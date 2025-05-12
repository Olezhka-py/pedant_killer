from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from pedant_killer.database.repository.core_repository import CoreRepository
from pedant_killer.database.models.order_device_service_orm import OrderDeviceServiceOrm


class OrderDeviceServiceRepository(CoreRepository):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        super().__init__(session_factory=session_factory, model_orm=OrderDeviceServiceOrm)
