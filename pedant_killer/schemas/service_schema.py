from pedant_killer.schemas.common_schema import CoreModel, BaseIdDTO, optional


class ServicePostDTO(CoreModel):
    name: str
    description: str | None = None
    warranty: int | None = None


class ServiceDTO(BaseIdDTO, ServicePostDTO):
    pass


@optional()
class ServicePartialDTO(ServiceDTO):
    pass
