from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped

from pedant_killer.database.database import Base
from pedant_killer.database.models.annotated import intpk


class ServiceBreakingOrm(Base):
    __tablename__ = 'service_breaking'
    __table_args__ = (
        UniqueConstraint(
            'service_id',
            'breaking_id',
            name='indx_uniq_service_breaking'
        ),
    )
    id: Mapped[intpk] = mapped_column(primary_key=True)
    service_id: Mapped[int] = mapped_column(ForeignKey('service.id'))
    breaking_id: Mapped[int] = mapped_column(ForeignKey('breaking.id'))
