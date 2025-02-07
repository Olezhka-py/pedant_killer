from typing import Any

from datetime import datetime
from phonenumbers import is_valid_number, parse
from pydantic import BaseModel, Field, field_validator, model_validator


class BaseIdDTO(BaseModel):
    id: int = Field(ge=1)


class ManufacturerPostDTO(BaseModel):
    name: str
    description: str | None = None


class ManufacturerDTO(BaseIdDTO, ManufacturerPostDTO):
    pass


class DeviceTypePostDTO(BaseModel):
    name: str
    description: str | None = None


class DeviceTypeDTO(BaseIdDTO, DeviceTypePostDTO):
    pass


class ManufacturerDeviceTypePostDTO(BaseModel):
    manufacturer_id: int = Field(ge=1)
    device_type_id: int = Field(ge=1)


class ManufacturerDeviceTypeDTO(BaseIdDTO, ManufacturerDeviceTypePostDTO):
    pass


class ManufacturerRelDTO(ManufacturerDeviceTypeDTO):
    manufacturer: ManufacturerDTO


class DeviceTypeRelDTO(ManufacturerDeviceTypeDTO):
    device_type: DeviceTypeDTO


class ManufacturerDeviceTypeRelDTO(ManufacturerRelDTO, DeviceTypeRelDTO):
    pass


class DevicePostDTO(BaseModel):
    manufacturer_device_type_id: int = Field(ge=1)
    name_model: str


class DeviceDTO(BaseIdDTO, DevicePostDTO):
    pass


class DeviceManufacturerDeviceTypeRelDTO(DeviceDTO):
    manufacturer_device_type: ManufacturerDeviceTypeRelDTO | None


class ServicePostDTO(BaseModel):
    name: str
    description: str | None = None


class ServiceDTO(BaseIdDTO, ServicePostDTO):
    pass


class DeviceServicePostDTO(BaseModel):
    device_id: int = Field(ge=1)
    service_id: int = Field(ge=1)
    price: int = Field(ge=0)
    work_duration: int | None = Field(default=None, ge=1)


class DeviceServiceDTO(BaseIdDTO, DeviceServicePostDTO):
    pass


class DeviceServiceDeviceRelDTO(DeviceServiceDTO):
    device: DeviceManufacturerDeviceTypeRelDTO


class DeviceServiceServiceRelDTO(DeviceServiceDTO):
    service: ServiceDTO


class DeviceServiceRelDTO(DeviceServiceDeviceRelDTO, DeviceServiceServiceRelDTO):
    pass


class AccessLevelPostDTO(BaseModel):
    name: str
    importance: int


class AccessLevelDTO(BaseIdDTO, AccessLevelPostDTO):
    pass


class UserPostDTO(BaseModel):
    access_level_id: int = Field(ge=1)
    telegram_username: str
    telegram_id: str
    full_name: str
    address: str | None = None
    phone: str

    @field_validator('phone')
    def is_valid_phone_number(cls, phone: Any) -> str | None:
        parsed_number = parse(phone, None)

        if is_valid_number(parsed_number):
            return phone

        raise ValueError(f'Некорректный номер телефона: {phone}')


class UserDTO(BaseIdDTO, UserPostDTO):
    pass


class OrderPostDTO(BaseModel):
    client_id: int = Field(ge=1)
    master_id: int = Field(ge=1)
    status_id: int = Field(ge=1)
    created_at: datetime
    status_updated_at: datetime
    sent_from_address: str | None = None
    return_to_address: str | None = None
    comment: str | None = None
    rating: int | None = Field(ge=1, le=10, default=None)


class OrderDTO(BaseIdDTO, OrderPostDTO):
    pass


class OrderStatusPostDTO(BaseModel):
    name: str
    description: str | None = None


class OrderStatusDTO(BaseIdDTO, OrderStatusPostDTO):
    pass


class DeviceServiceOrderRelDTO(DeviceServiceDTO):
    order: list[OrderDTO] | None = None


class OrderDeviceServiceRelDTO(OrderDTO):
    device_service: list[DeviceServiceDTO] | None = None


class AccessLevelRelDTO(UserDTO):
    access_level: AccessLevelDTO


class UserOrdersClientRelDTO(UserDTO):
    orders_client: list[OrderDTO] | None = None


class UserOrdersMasterRelDTO(UserDTO):
    orders_master: list[OrderDTO] | None = None


class UserAccessLevelRelDTO(UserDTO):
    access_level: AccessLevelDTO


class UserAllRelDTO(UserOrdersClientRelDTO, UserOrdersMasterRelDTO, AccessLevelDTO):
    pass


class OrderMasterRelDTO(OrderDTO):
    user_master: UserDTO | None = None


class OrderClientRelDTO(OrderDTO):
    user_client: UserDTO


class OrderOrderStatusRelDTO(OrderDTO):
    status: OrderStatusDTO


class OrderAllRelDTO:
    pass
