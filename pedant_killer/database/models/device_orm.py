from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from pedant_killer.database.database import Base
from pedant_killer.database.models.annotated import intpk
if TYPE_CHECKING:
    from pedant_killer.database.models.manufacturer_device_type_orm import ManufacturerDeviceTypeOrm


class DeviceOrm(Base):
    __tablename__ = 'device'
    id: Mapped[intpk]
    manufacturer_device_type_id: Mapped[int] = mapped_column(ForeignKey('manufacturer_device_type.id'))
    name_model: Mapped[str]

    manufacturer_device_type: Mapped['ManufacturerDeviceTypeOrm'] = relationship()
