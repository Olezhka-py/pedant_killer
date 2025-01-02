from sqlalchemy.orm import Mapped

from pedant_killer.database.database import Base
from . import intpk


class ManufacturerOrm(Base):
    __tablename__ = 'manufacturer'

    id: Mapped[intpk]
    name: Mapped[str]
    description: Mapped[str | None] = None
