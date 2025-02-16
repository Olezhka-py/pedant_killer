from pydantic import Field

from pedant_killer.schemas.common_schema import CoreModel, BaseIdDTO, optional


class OrderStatusPostDTO(CoreModel):
    name: str
    description: str | None = None


class OrderStatusDTO(BaseIdDTO, OrderStatusPostDTO):
    pass


@optional()
class OrderStatusPartialDTO(OrderStatusDTO):
    pass
