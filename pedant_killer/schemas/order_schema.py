from typing import Any, TYPE_CHECKING
from datetime import datetime

from pydantic import Field

from pedant_killer.schemas.common_schema import CoreModel, BaseIdDTO, optional
if TYPE_CHECKING:
    from pedant_killer.schemas.device_service_schema import DeviceServiceDTO
    from pedant_killer.schemas.user_schema import UserDTO
    from pedant_killer.schemas.order_status_schema import OrderStatusDTO


class OrderPostDTO(CoreModel):
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


@optional()
class OrderPartialDTO(OrderDTO):
    pass


class OrderMasterRelDTO(OrderDTO):
    user_master: 'UserDTO | None' = None


class OrderClientRelDTO(OrderDTO):
    user_client: 'UserDTO'


class OrderOrderStatusRelDTO(OrderDTO):
    status: 'OrderStatusDTO'


class OrderDeviceServiceRelDTO(OrderDTO):
    device_service: 'list[DeviceServiceDTO] | None' = None


class OrderAllRelDTO:
    pass

