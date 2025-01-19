from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from . import intpk
from pedant_killer.database.database import Base
from order import OrderOrm
from access_level import AccessLevelOrm


class UserOrm(Base):
    __tablename__ = 'user'
    id: Mapped[intpk]
    access_level_id: Mapped[int] = mapped_column(ForeignKey('access_level.id'))
    telegram_username: Mapped[str]
    telegram_id: Mapped[str]
    full_name: Mapped[str]
    address: Mapped[str]
    phone: Mapped[str]

    orders_client: Mapped[list['OrderOrm'] | None] = relationship(
        back_populates='user_client',
        foreign_keys=[OrderOrm.client_id],
        viewonly=True
    )

    orders_master: Mapped[list['OrderOrm'] | None] = relationship(
        back_populates='user_master',
        foreign_keys=[OrderOrm.master_id],
        viewonly=True
    )

    access_level: Mapped['AccessLevelOrm'] = relationship()
