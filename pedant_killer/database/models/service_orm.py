from sqlalchemy.orm import Mapped, mapped_column

from pedant_killer.database.models.annotated import intpk
from pedant_killer.database.database import Base


class ServiceOrm(Base):
    __tablename__ = 'service'
    id: Mapped[intpk]
    name: Mapped[str]
    description: Mapped[str | None] = mapped_column(default=None)
