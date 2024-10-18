from datetime import datetime
from typing import Annotated

from sqlalchemy import ForeignKey, NUMERIC, func, and_
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base, async_session_factory, config


intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)]


class ManufacturerOrm(Base):
    __tablename__ = 'manufacturer'

    id: Mapped[intpk]
    name: Mapped[str]
    description: Mapped[str]


class DeviceTypeOrm(Base):
    __tablename__ = 'device_type'
    id: Mapped[intpk]
    name: Mapped[str]
    description: Mapped[str]


class ManufacturerDeviceTypeOrm(Base):
    __tablename__ = 'manufacturer_device_type'
    id: Mapped[intpk]
    manufacturer_id: Mapped[int] = mapped_column(ForeignKey('manufacturer.id'))
    device_type_id: Mapped[int] = mapped_column(ForeignKey('device_type.id'))

    manufacturer: Mapped[ManufacturerOrm] = relationship()
    device_type: Mapped[DeviceTypeOrm] = relationship()


class DeviceOrm(Base):
    __tablename__ = 'device'
    id: Mapped[intpk]
    manufacturer_device_type_id: Mapped[int] = mapped_column(ForeignKey('manufacturer_device_type.id'))
    model: Mapped[str]


class ServiceOrm(Base):
    __tablename__ = 'service'
    id: Mapped[intpk]
    name: Mapped[str]
    description: Mapped[str]


class OrderDeviceServiceOrm(Base):
    __tablename__ = 'order_device_service'
    id: Mapped[intpk]
    order_id: Mapped[int] = mapped_column(ForeignKey('order.id'))
    device_service_id: Mapped[int] = mapped_column(ForeignKey('device_service.id'))
    order: Mapped['OrderOrm'] = relationship(
        back_populates='order_device_service',
        foreign_keys=[order_id]
    )

    device_service: Mapped['DeviceServiceOrm'] = relationship(
        back_populates='order_device_service',
        foreign_keys=[device_service_id]
    )


class DeviceServiceOrm(Base):
    __tablename__ = 'device_service'
    id: Mapped[intpk]
    device_id: Mapped[int] = mapped_column(ForeignKey('device.id'))
    service_id: Mapped[int] = mapped_column(ForeignKey('service.id'))
    price: Mapped[int]
    work_duration: Mapped[int]

    device: Mapped['DeviceOrm'] = relationship()
    service: Mapped['ServiceOrm'] = relationship()

    order_device_service: Mapped['OrderDeviceServiceOrm'] = relationship(
        back_populates='device_service',
        foreign_keys=[OrderDeviceServiceOrm.device_service_id]
    )


class OrderOrm(Base):
    __tablename__ = 'order'
    id: Mapped[intpk]
    client_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    master_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    status_id: Mapped[int] = mapped_column(ForeignKey('order_status.id'))
    created_add: Mapped[created_at]
    status_updated_at: Mapped[updated_at]
    sent_from_address: Mapped[str]
    return_to_address: Mapped[str]
    comment: Mapped[str]
    rating: Mapped[str]

    user_client: Mapped['UserOrm'] = relationship(
        back_populates='order_client',
        foreign_keys=[client_id],
        remote_side='UserOrm.id'

    )

    user_master: Mapped['UserOrm'] = relationship(
        back_populates='order_master',
        foreign_keys=[master_id],
        remote_side='UserOrm.id'
    )

    status: Mapped['OrderStatusOrm'] = relationship(
        back_populates='order',
        foreign_keys=[status_id]
    )

    order_device_service: Mapped['OrderDeviceServiceOrm'] = relationship(
        back_populates='order',
        foreign_keys=[OrderDeviceServiceOrm.order_id]
    )


class OrderStatusOrm(Base):
    __tablename__ = 'order_status'
    id: Mapped[intpk]
    name: Mapped[str]
    description: Mapped[str]

    order: Mapped['OrderOrm'] = relationship(
        back_populates='status',
        foreign_keys=[OrderOrm.status_id]
    )


class UserOrm(Base):
    __tablename__ = 'user'
    id: Mapped[intpk]
    access_level_id: Mapped[int] = mapped_column(ForeignKey('access_level.id'))
    telegram_username: Mapped[str]
    telegram_id: Mapped[str]
    full_name: Mapped[str]
    address: Mapped[str]
    phone: Mapped[str]

    order_client: Mapped['OrderOrm'] = relationship(
        back_populates='user_client',
        foreign_keys=[OrderOrm.client_id],
        primaryjoin='and_('
                    'UserOrm.id == foreign(OrderOrm.client_id),'
                    ' UserOrm.access_level_id == AccessLevelOrm.id,'
                    ' AccessLevelOrm.importance == 10)',
        viewonly=True
    )

    order_master: Mapped['OrderOrm'] = relationship(
        back_populates='user_master',
        foreign_keys=[OrderOrm.master_id],
        primaryjoin='and_('
                    'UserOrm.id == foreign(OrderOrm.master_id),'
                    ' UserOrm.access_level_id == AccessLevelOrm.id,'
                    ' AccessLevelOrm.importance == 30)',
        viewonly=True
    )

    access_level: Mapped['AccessLevelOrm'] = relationship(
        back_populates='user',
        foreign_keys=[access_level_id]
    )


class AccessLevelOrm(Base):
    __tablename__ = 'access_level'
    id: Mapped[intpk]
    name: Mapped[str]
    importance: Mapped[int]

    user: Mapped['UserOrm'] = relationship(
        back_populates='access_level',
        foreign_keys=[UserOrm.access_level_id]
    )


