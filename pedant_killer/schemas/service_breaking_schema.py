from pedant_killer.schemas.breaking_schemas import BreakingDTO
from pedant_killer.schemas.service_schema import ServiceDTO


class ServiceBreakingRelDTO(ServiceDTO):
    breaking: list['BreakingDTO']


class BreakingServiceRelDTO(BreakingDTO):
    service: list['ServiceDTO']
