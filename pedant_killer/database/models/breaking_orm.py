# from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, relationship, mapped_column

from pedant_killer.database.models.annotated import intpk
from pedant_killer.database.database import Base
if TYPE_CHECKING:
    from pedant_killer.database.models.service_orm import ServiceOrm


class BreakingOrm(Base):
    __tablename__ = 'breaking'
    id: Mapped[intpk]
    name: Mapped[str]
    description: Mapped[str | None] = mapped_column(default=None)

    service: Mapped[list['ServiceOrm']] = relationship(secondary='service_breaking', back_populates='breaking')
