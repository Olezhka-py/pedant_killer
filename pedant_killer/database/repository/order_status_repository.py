from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from pedant_killer.database.repository.core_repository import CoreRepository
from pedant_killer.database.models.order_status_orm import OrderStatusOrm


class OrderStatusRepository(CoreRepository[OrderStatusOrm]):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        super().__init__(session_factory=session_factory, model_orm=OrderStatusOrm)
