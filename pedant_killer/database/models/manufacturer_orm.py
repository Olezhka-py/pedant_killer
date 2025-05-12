from sqlalchemy.orm import Mapped, mapped_column

from pedant_killer.database.database import Base
from pedant_killer.database.models.annotated import intpk


class ManufacturerOrm(Base):
    __tablename__ = 'manufacturer'

    id: Mapped[intpk]
    name: Mapped[str]
    description: Mapped[str | None] = mapped_column(default=None)
