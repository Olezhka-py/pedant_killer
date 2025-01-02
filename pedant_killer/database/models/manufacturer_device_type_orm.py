from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from pedant_killer.database.database import Base
from . import intpk
from manufacturer import ManufacturerOrm
from device_type import DeviceTypeOrm


class ManufacturerDeviceTypeOrm(Base):
    __tablename__ = 'manufacturer_device_type'
    id: Mapped[intpk]
    manufacturer_id: Mapped[int] = mapped_column(ForeignKey('manufacturer.id'))
    device_type_id: Mapped[int] = mapped_column(ForeignKey('device_type.id'))

    manufacturer: Mapped[ManufacturerOrm] = relationship(foreign_keys=[manufacturer_id])
    device_type: Mapped[DeviceTypeOrm] = relationship()