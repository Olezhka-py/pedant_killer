from typing import Annotated

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from pedant_killer.database.database import Base

intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]


class DeviceORM(Base):
    __tablename__ = 'device'
    id: Mapped[intpk]
    manufacturer_device_type_id: Mapped[int] = mapped_column(ForeignKey('manufacturer_device_type.id'))
    model_name: Mapped[str]

    manufacturer_device_type: Mapped[...] = relationship()
