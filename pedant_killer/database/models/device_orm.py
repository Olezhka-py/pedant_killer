from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from pedant_killer.database.database import Base

from manufacturer_device_type import ManufacturerDeviceTypeOrm
from . import intpk


class DeviceOrm(Base):
    __tablename__ = 'device'
    id: Mapped[intpk]
    manufacturer_device_type_id: Mapped[int] = mapped_column(ForeignKey('manufacturer_device_type.id'))
    name_model: Mapped[str]

    manufacturer_device_type: Mapped[ManufacturerDeviceTypeOrm] = relationship()
