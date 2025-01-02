from sqlalchemy.orm import Mapped, relationship

from . import intpk
from pedant_killer.database.database import Base
from order import OrderOrm


class OrderStatusOrm(Base):
    __tablename__ = 'order_status'
    id: Mapped[intpk]
    name: Mapped[str]
    description: Mapped[str | None] = None

    order: Mapped['OrderOrm'] = relationship(
        back_populates='status',
        foreign_keys=[OrderOrm.status_id]
    )
