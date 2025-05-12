from __future__ import annotations
from pedant_killer.schemas.common_schema import CoreModel, BaseIdDTO, optional


class BreakingPostDTO(CoreModel):
    name: str
    description: str | None = None


class BreakingDTO(BaseIdDTO, BreakingPostDTO):
    pass


class BreakingServiceRelDTO(BreakingDTO):
    services: list[ServiceDTO] | None = None


@optional()
class BreakingPartialDTO(BreakingDTO):
    pass


class ServicePostDTO(CoreModel):
    name: str
    description: str | None = None


class ServiceDTO(BaseIdDTO, ServicePostDTO):
    pass


class ServiceBreakingRelDTO(ServiceDTO):
    breakings: list[BreakingDTO] | None = None


@optional()
class ServicePartialDTO(ServiceDTO):
    pass


class ServiceIdListDTO(CoreModel):
    id: list[int]


ServiceBreakingRelDTO.update_forward_refs()
BreakingServiceRelDTO.update_forward_refs()
