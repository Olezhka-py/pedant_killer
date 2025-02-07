from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from pedant_killer.database.database import Base
from pedant_killer.database.models.annotated import intpk
if TYPE_CHECKING:
    from pedant_killer.database.models.device_orm import DeviceOrm
    from pedant_killer.database.models.service_orm import ServiceOrm
    from pedant_killer.database.models.order_orm import OrderOrm


class DeviceServiceOrm(Base):
    __tablename__ = 'device_service'
    id: Mapped[intpk]
    device_id: Mapped[int] = mapped_column(ForeignKey('device.id'))
    service_id: Mapped[int] = mapped_column(ForeignKey('service.id'))
    price: Mapped[int]
    work_duration: Mapped[int | None] = mapped_column(default=None)

    device: Mapped['DeviceOrm'] = relationship()
    service: Mapped['ServiceOrm'] = relationship()

    order: Mapped[list['OrderOrm']] = relationship(
        secondary='order_device_service',
        back_populates='device_service'
    )
