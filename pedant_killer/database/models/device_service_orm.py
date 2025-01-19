from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from pedant_killer.database.database import Base
from . import intpk
from device import DeviceOrm
from service import ServiceOrm
from order import OrderOrm


class DeviceServiceOrm(Base):
    __tablename__ = 'device_service'
    id: Mapped[intpk]
    device_id: Mapped[int] = mapped_column(ForeignKey('device.id'))
    service_id: Mapped[int] = mapped_column(ForeignKey('service.id'))
    price: Mapped[int]
    work_duration: Mapped[int | None] = None

    device: Mapped['DeviceOrm'] = relationship()
    service: Mapped['ServiceOrm'] = relationship()

    order: Mapped[list['OrderOrm']] = relationship(
        secondary='order_device_service',
        back_populates='device_service'
    )
