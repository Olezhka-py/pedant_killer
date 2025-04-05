from typing import TYPE_CHECKING

from pedant_killer.schemas.common_schema import CoreModel, BaseIdDTO, optional
if TYPE_CHECKING:
    from pedant_killer.schemas.breaking_schemas import BreakingDTO


class ServicePostDTO(CoreModel):
    name: str
    description: str | None = None


class ServiceDTO(BaseIdDTO, ServicePostDTO):
    pass


@optional()
class ServicePartialDTO(ServiceDTO):
    pass


class ServiceBreakingDTO(ServiceDTO):
    breaking: list['BreakingDTO']
