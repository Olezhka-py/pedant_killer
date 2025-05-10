from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from pedant_killer.database.models.annotated import intpk
from pedant_killer.database.database import Base

if TYPE_CHECKING:
    from pedant_killer.database.models.breaking_orm import BreakingOrm


class ServiceOrm(Base):
    __tablename__ = 'service'
    id: Mapped[intpk]
    name: Mapped[str]
    description: Mapped[str | None] = mapped_column(default=None)

    breakings: Mapped[list['BreakingOrm']] = relationship(secondary='service_breaking', back_populates='services')
