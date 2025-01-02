from sqlalchemy.orm import Mapped

from . import intpk
from pedant_killer.database.database import Base


class ServiceOrm(Base):
    __tablename__ = 'service'
    id: Mapped[intpk]
    name: Mapped[str]
    description: Mapped[str]