from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from pedant_killer.database.database import Base
from . import intpk, updated_at, created_at
from user import UserOrm
from order_status import OrderStatusOrm
from device_service import DeviceServiceOrm


class OrderOrm(Base):
    __tablename__ = 'order'
    id: Mapped[intpk]
    client_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    master_id: Mapped[int | None] = mapped_column(ForeignKey('user.id'), nullable=True)
    status_id: Mapped[int] = mapped_column(ForeignKey('order_status.id'))
    created_at: Mapped[created_at]
    status_updated_at: Mapped[updated_at]
    sent_from_address: Mapped[str | None] = None
    return_to_address: Mapped[str | None] = None
    comment: Mapped[str | None] = None
    rating: Mapped[str | None] = None

    user_client: Mapped['UserOrm'] = relationship(
        back_populates='orders_client',
        foreign_keys=[client_id]
    )

    user_master: Mapped['UserOrm'] = relationship(
        back_populates='orders_master',
        foreign_keys=[master_id]
    )

    status: Mapped['OrderStatusOrm'] = relationship(
        back_populates='order',
        foreign_keys=[status_id]
    )

    device_service: Mapped[list['DeviceServiceOrm']] = relationship(
        secondary='order_device_service',
        back_populates='order'
    )
