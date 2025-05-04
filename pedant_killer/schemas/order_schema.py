from datetime import datetime

from pydantic import Field

from pedant_killer.schemas.common_schema import CoreModel, BaseIdDTO, optional
from pedant_killer.schemas.order_status_schema import OrderStatusDTO


class OrderPostDTO(CoreModel):
    client_id: int = Field(ge=1)
    master_id: int | None = Field(ge=1, default=None)
    status_id: int = Field(ge=1)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status_updated_at: datetime = Field(default_factory=datetime.utcnow)
    sent_from_address: str | None = None
    return_to_address: str | None = None
    description_model_device: str | None = None
    breaking_id: int | None = Field(ge=1)
    description_breaking: str | None = None
    comment: str | None = None
    rating: int | None = Field(ge=1, le=10, default=None)


class OrderDTO(BaseIdDTO, OrderPostDTO):
    pass


@optional()
class OrderPartialDTO(OrderDTO):
    pass


class OrderOrderStatusRelDTO(OrderDTO):
    status: 'OrderStatusDTO'


class OrderAllRelDTO:
    pass
