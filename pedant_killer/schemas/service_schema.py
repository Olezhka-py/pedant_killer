from pydantic import Field

from pedant_killer.schemas.common_schema import CoreModel, BaseIdDTO, optional, BaseModel
from pedant_killer.schemas.breaking_schemas import BreakingDTO


class ServicePostDTO(CoreModel):
    name: str
    description: str | None = None


class ServiceDTO(BaseIdDTO, ServicePostDTO):
    pass


@optional()
class ServicePartialDTO(ServiceDTO):
    pass


class ServiceIdListDTO(BaseModel):
    service_id: list[int]
