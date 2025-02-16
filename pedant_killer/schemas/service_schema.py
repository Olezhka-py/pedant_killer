from pydantic import Field

from pedant_killer.schemas.common_schema import CoreModel, BaseIdDTO, optional


class ServicePostDTO(CoreModel):
    name: str
    description: str | None = None


class ServiceDTO(BaseIdDTO, ServicePostDTO):
    pass


@optional()
class ServicePartialDTO(ServiceDTO):
    pass
