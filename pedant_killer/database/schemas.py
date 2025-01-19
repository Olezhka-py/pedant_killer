from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ManufacturerPostDTO(BaseModel):
    name: str
    description: str | None


class ManufacturerDTO(ManufacturerPostDTO):
    id: int


class DeviceTypePostDTO(BaseModel):
    name: str
    description: str | None


class DeviceTypeDTO(DeviceTypePostDTO):
    id: int


class ManufacturerDeviceTypePostDTO(BaseModel):
    manufacturer_id: int
    device_type_id: int


class ManufacturerDeviceTypeDTO(ManufacturerDeviceTypePostDTO):
    id: int


class ManufacturerRelDTO(ManufacturerDeviceTypeDTO):
    manufacturer: ManufacturerDTO


class DeviceTypeRelDTO(ManufacturerDeviceTypeDTO):
    device_type: DeviceTypeDTO


class ManufacturerAndDeviceTypeRelDTO(ManufacturerRelDTO, DeviceTypeRelDTO):
    pass


class DevicePostDTO(BaseModel):
    manufacturer_device_type_id: int
    name_model: str


class DeviceDTO(DevicePostDTO):
    id: int


class ManufacturerDeviceTypeRelDTO(DeviceDTO):
    manufacturer_device_type: ManufacturerAndDeviceTypeRelDTO | None


class ServicePostDTO(BaseModel):
    name: str
    description: str | None = None


class ServiceDTO(ServicePostDTO):
    id: int


class DeviceServicePostDTO(BaseModel):
    device_id: int
    service_id: int
    price: int
    work_duration: int | None = None


class DeviceServiceDTO(DeviceServicePostDTO):
    id: int


class DeviceRelDTO(DeviceServiceDTO):
    device: ManufacturerDeviceTypeRelDTO


class ServiceRelDTO(DeviceServiceDTO):
    service: ServiceDTO


class DeviceAndServiceRelDTO(DeviceRelDTO, ServiceRelDTO):
    pass


class AccessLevelPostDTO(BaseModel):
    name: str
    importance: int


class AccessLevelDTO(AccessLevelPostDTO):
    id: int


class UserPostDTO(BaseModel):
    access_level_id: int
    telegram_username: str
    telegram_id: str
    full_name: str
    address: str
    phone: str


class UserDTO(UserPostDTO):
    id: int


class OrderPostDTO(BaseModel):
    client_id: int
    master_id: int
    status_id: int
    created_at: datetime
    status_updated_at: datetime
    sent_from_address: str
    return_to_address: str
    comment: str
    rating: int


class OrderDTO(OrderPostDTO):
    id: int


class OrderStatusPostDTO(BaseModel):
    name: str
    description: str | None = None


class OrderStatusDTO(OrderStatusPostDTO):
    id: int


class OrderDeviceServicePostDTO(BaseModel):
    order_id: int
    device_service_id: int


class AccessLevelRelDTO(UserDTO):
    access_level: AccessLevelDTO


class UserOrdersClientRelDTO(UserDTO):
    orders_client: list[OrderDTO] | None = None


class UserOrdersMasterRelDTO(UserDTO):
    orders_master: list[OrderDTO] | None = None


class UserAllRelDTO(UserOrdersClientRelDTO, UserOrdersMasterRelDTO):
    pass





