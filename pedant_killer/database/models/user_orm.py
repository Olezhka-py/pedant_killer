from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from pedant_killer.database.models.annotated import intpk
from pedant_killer.database.database import Base
if TYPE_CHECKING:
    from pedant_killer.database.models.order_orm import OrderOrm
    from pedant_killer.database.models.access_level_orm import AccessLevelOrm


class UserOrm(Base):
    __tablename__ = 'user'
    id: Mapped[intpk]
    access_level_id: Mapped[int] = mapped_column(ForeignKey('access_level.id'))
    telegram_username: Mapped[str]
    telegram_id: Mapped[int]
    full_name: Mapped[str]
    address: Mapped[str | None] = mapped_column(default=None, nullable=True)
    phone: Mapped[str | None] = mapped_column(default=None, nullable=True)

    orders_client: Mapped[list['OrderOrm'] | None] = relationship(
        back_populates='user_client',
        foreign_keys='OrderOrm.client_id',
        viewonly=True
    )

    orders_master: Mapped[list['OrderOrm'] | None] = relationship(
        back_populates='user_master',
        foreign_keys='OrderOrm.master_id',
        viewonly=True
    )

    access_level: Mapped['AccessLevelOrm'] = relationship()
