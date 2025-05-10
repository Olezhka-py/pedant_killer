from pedant_killer.database.repository.breaking_service_repository import  BreakingServiceRepository
from pedant_killer.schemas.common_schema import BaseIdDTO


class BreakingServiceService:
    def __init__(self, repository: BreakingServiceRepository) -> None:
        self._repository = repository

    async def save(self, service_dto: BaseIdDTO,
                   breaking_dto: BaseIdDTO) -> list[BaseIdDTO] | None:
        result_orm = await self._repository.save(service_id=service_dto.id,
                                                 breaking_id=breaking_dto.id)

        if result_orm:
            return [BaseIdDTO(id=result_orm)]

        return None
