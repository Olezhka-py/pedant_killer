from typing import Any, TYPE_CHECKING

from phonenumbers import is_valid_number, parse
from pydantic import Field, field_validator

from pedant_killer.schemas.common_schema import CoreModel, BaseIdDTO, optional
if TYPE_CHECKING:
    from pedant_killer.schemas.access_level_schema import AccessLevelDTO
    from pedant_killer.schemas.order_schema import OrderDTO


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

        parsed_number = parse(phone, None)

        if is_valid_number(parsed_number):
            return phone

        raise ValueError(f'Некорректный номер телефона: {phone}')


class UserDTO(BaseIdDTO, UserPostDTO):
    pass


@optional()
class UserPartialDTO(UserDTO):
    pass


class UserOrdersClientRelDTO(UserDTO):
    orders_client: 'list[OrderDTO] | None' = None


class UserOrdersMasterRelDTO(UserDTO):
    orders_master: 'list[OrderDTO] | None' = None


class UserAccessLevelRelDTO(UserDTO):
    access_level: 'AccessLevelDTO'


class UserAllRelDTO(UserOrdersClientRelDTO, UserOrdersMasterRelDTO, UserAccessLevelRelDTO):
    pass
