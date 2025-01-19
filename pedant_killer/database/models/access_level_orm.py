from . import intpk
from sqlalchemy.orm import Mapped
from pedant_killer.database.database import Base


class AccessLevelOrm(Base):
    __tablename__ = 'access_level'
    id: Mapped[intpk]
    name: Mapped[str]
    importance: Mapped[int]
