from typing import TYPE_CHECKING

from pedant_killer.schemas.common_schema import CoreModel, BaseIdDTO, optional

from pedant_killer.schemas.service_schema import ServiceDTO
if TYPE_CHECKING:
    pass


class BreakingPostDTO(CoreModel):
    name: str
    description: str


class BreakingDTO(BaseIdDTO, CoreModel):
    pass


@optional()
class BreakingPartialDTO(BreakingDTO):
    pass


class BreakingServiceRelDTO(BreakingDTO):
    service: list[ServiceDTO]
