from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from pedant_killer.database.database import Base
from pedant_killer.database.models.annotated import intpk, updated_at, created_at
if TYPE_CHECKING:
    from pedant_killer.database.models.user_orm import UserOrm
    from pedant_killer.database.models.order_status_orm import OrderStatusOrm
    from pedant_killer.database.models.device_service_orm import DeviceServiceOrm


class OrderOrm(Base):
    __tablename__ = 'order'
    id: Mapped[intpk]
    client_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    master_id: Mapped[int | None] = mapped_column(ForeignKey('user.id'), nullable=True)
    status_id: Mapped[int] = mapped_column(ForeignKey('order_status.id'))
    created_at: Mapped[created_at]
    status_updated_at: Mapped[updated_at]
    sent_from_address: Mapped[str | None] = mapped_column(default=None)
    return_to_address: Mapped[str | None] = mapped_column(default=None)
    description_model_device: Mapped[str | None] = mapped_column(default=None)
    breaking_id: Mapped[int | None] = mapped_column(ForeignKey('breaking.id'), default=None)
    description_breaking: Mapped[str | None] = mapped_column(default=None)
    comment: Mapped[str | None] = mapped_column(default=None)
    rating: Mapped[str | None] = mapped_column(default=None)

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