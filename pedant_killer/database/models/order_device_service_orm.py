from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped

from pedant_killer.database.database import Base
from pedant_killer.database.models.annotated import intpk


class OrderDeviceServiceOrm(Base):
    __tablename__ = 'order_device_service'
    __table_args__ = (
        UniqueConstraint(
            'order_id',
            'device_service_id',
            name='indx_uniq'
        ),
    )
    id: Mapped[intpk] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('order.id'))
    device_service_id: Mapped[int] = mapped_column(ForeignKey('device_service.id'))
