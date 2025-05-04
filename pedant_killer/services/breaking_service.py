from typing import TYPE_CHECKING

from pedant_killer.schemas.breaking_schemas import (BaseIdDTO,
                                                    BreakingPostDTO,
                                                    BreakingDTO,
                                                    BreakingPartialDTO)
from pedant_killer.schemas.service_breaking_schema import BreakingServiceRelDTO
from pedant_killer.database.specification import DeleteSpaceAndLowerCaseSpecification

if TYPE_CHECKING:
    from pedant_killer.database.repository.breaking_repository import BreakingRepository


class BreakingService:
    def __init__(self, repository: 'BreakingRepository') -> None:
        self._repository = repository

    async def save_breaking(self, model_dto: BreakingPostDTO) -> list[BaseIdDTO] | None:
        result_orm = await self._repository.save(**model_dto.model_dump(exclude_none=True))

        if result_orm:
            return [BaseIdDTO(id=result_orm)]

        return None

    async def save_relationship_breaking_service(self, service_dto: BaseIdDTO,
                                                 breaking_dto: BaseIdDTO) -> list[BaseIdDTO] | None:
        result_orm = await self._repository.save_breaking_service(service_id=service_dto.id,
                                                                  breaking_id=breaking_dto.id)

        if result_orm:
            return [BaseIdDTO(id=result_orm)]

        return None

    async def get_breaking(self, model_dto: BaseIdDTO | BreakingPartialDTO) -> list[BreakingDTO] | None:
        result_orm = await self._repository.get(**model_dto.model_dump(exclude_none=True))

        if result_orm:
            return [BreakingDTO.model_validate(res, from_attributes=True) for res in result_orm]

        return None

    async def get_breaking_standardize(self, model_dto: BaseIdDTO | BreakingPartialDTO) -> list[BreakingDTO] | None:
        result_orm = await self._repository.get(specification_filter=DeleteSpaceAndLowerCaseSpecification,
                                                **model_dto.model_dump(exclude_none=True))
        if result_orm:
            return [BreakingDTO.model_validate(res, from_attributes=True) for res in result_orm]

        return None

    async def get_relationship_service(self, model_dto: BaseIdDTO) -> list[BreakingServiceRelDTO] | None:
        result_orm = await self._repository.get_service(instance_id=model_dto.id)

        if result_orm:
            return [BreakingServiceRelDTO.model_validate(res, from_attributes=True) for res in result_orm]

    async def get_all_breaking(self) -> list[BreakingDTO] | None:
        result_orm = await self._repository.get()

        if result_orm:
            return [BreakingDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def delete_breaking(self, model_dto: BaseIdDTO) -> list[BreakingDTO] | None:
        result_dto = await self.get_breaking(model_dto)

        if result_dto:
            delete_result = await self._repository.delete(id=model_dto.id)

            if delete_result:
                return result_dto

        return None

    async def update_breaking(self, model_dto: BreakingPartialDTO) -> list[BreakingDTO] | None:
        result_orm = await self._repository.update(**model_dto.model_dump(exclude_none=True))

        if result_orm:
            return [BreakingDTO.model_validate(result_orm, from_attributes=True)]

        return None
