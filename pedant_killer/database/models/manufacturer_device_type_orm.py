from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from pedant_killer.database.database import Base
from pedant_killer.database.models.annotated import intpk
from pedant_killer.database.models.manufacturer_orm import ManufacturerOrm
from pedant_killer.database.models.device_type_orm import DeviceTypeOrm


class ManufacturerDeviceTypeOrm(Base):
    __tablename__ = 'manufacturer_device_type'
    id: Mapped[intpk]
    manufacturer_id: Mapped[int] = mapped_column(ForeignKey('manufacturer.id'))
    device_type_id: Mapped[int] = mapped_column(ForeignKey('device_type.id'))

    manufacturer: Mapped[ManufacturerOrm] = relationship()
    device_type: Mapped[DeviceTypeOrm] = relationship()
