from __future__ import annotations
from datetime import datetime, UTC
from typing import Any

from pydantic import Field, field_validator
from phonenumbers import is_valid_number, parse

from pedant_killer.schemas.common_schema import BaseIdDTO, optional, CoreModel
from pedant_killer.schemas.service_breaking_schema import ServiceBreakingRelDTO
from pedant_killer.schemas.device_schema import DeviceDTO
from pedant_killer.schemas.order_status_schema import OrderStatusDTO
from pedant_killer.schemas.access_level_schema import AccessLevelDTO
from pedant_killer.schemas.service_breaking_schema import BreakingDTO


class DeviceServicePostDTO(CoreModel):
    device_id: int = Field(ge=1)
    service_id: int = Field(ge=1)
    price: int = Field(ge=0)
    work_duration: int | None = Field(default=None, ge=1)
    warranty: int | None = Field(default=0)


class DeviceServiceDTO(BaseIdDTO, DeviceServicePostDTO):
    pass


class DeviceServiceRelDTO(DeviceServiceDTO):
    service: ServiceBreakingRelDTO | None
    device: DeviceDTO | None
    order: list[OrderDTO] | None = None


@optional()
class DeviceServicePartialDTO(DeviceServiceDTO):
    pass


class DeviceServiceDeviceIdAndListServiceId(CoreModel):
    device_id: int = Field(ge=1)
    service_id: list[int]


class OrderPostDTO(CoreModel):
    client_id: int = Field(ge=1)
    master_id: int | None = Field(ge=1, default=None)
    status_id: int = Field(ge=1)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    status_updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    sent_from_address: str | None = None
    return_to_address: str | None = None
    description_model_device: str | None = None
    breaking_id: int | None = Field(ge=1)
    description_breaking: str | None = None
    comment: str | None = None
    rating: int | None = Field(ge=1, le=10, default=None)


class OrderDTO(BaseIdDTO, OrderPostDTO):
    pass


class OrderRelDTO(OrderDTO):
    user_client: UserDTO | None = None
    user_master: UserDTO | None = None
    status: OrderStatusDTO | None = None
    device_service: DeviceServiceDTO | None = None
    breaking: BreakingDTO | None = None


@optional()
class OrderPartialDTO(OrderDTO):
    pass


class UserPostDTO(CoreModel):
    access_level_id: int = Field(ge=1)
    telegram_username: str
    telegram_id: int
    full_name: str
    address: str | None = None
    phone: str | None = None

    @field_validator('phone')
    def is_valid_phone_number(cls, phone: Any) -> str | None:
        if phone is None:
            return None

        parsed_number = parse(phone, "RU")

        if is_valid_number(parsed_number):
            return phone

        raise ValueError(f'Некорректный номер телефона: {phone}')


class UserDTO(BaseIdDTO, UserPostDTO):
    pass


class UserRelDTO(UserDTO):
    orders_client: list[OrderDTO] | None = None
    order_master: list[OrderDTO] | None = None
    access_level: AccessLevelDTO | None = None


@optional()
class UserPartialDTO(UserDTO):
    pass


UserRelDTO.update_forward_refs()
OrderRelDTO.update_forward_refs()
DeviceServiceRelDTO.update_forward_refs()

