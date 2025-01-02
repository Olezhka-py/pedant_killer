from sqlalchemy.orm import Mapped

from pedant_killer.database.database import Base
from . import intpk


class DeviceTypeOrm(Base):
    __tablename__ = 'device_type'
    id: Mapped[intpk]
    name: Mapped[str]
    description: Mapped[str | None] = None

