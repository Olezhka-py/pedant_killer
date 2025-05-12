from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship, mapped_column

from pedant_killer.database.models.annotated import intpk
from pedant_killer.database.database import Base
if TYPE_CHECKING:
    from pedant_killer.database.models.order_orm import OrderOrm


class OrderStatusOrm(Base):
    __tablename__ = 'order_status'
    id: Mapped[intpk]
    name: Mapped[str]
    description: Mapped[str | None] = mapped_column(default=None)

