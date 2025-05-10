from pedant_killer.schemas.service_breaking_schema import (BaseIdDTO,
                                                           BreakingPostDTO,
                                                           BreakingDTO,
                                                           BreakingPartialDTO,
                                                           BreakingServiceRelDTO)
from pedant_killer.database.specification import DeleteSpaceAndLowerCaseSpecification

from pedant_killer.database.repository.breaking_repository import BreakingRepository


class BreakingService:
    def __init__(self, repository: BreakingRepository) -> None:
        self._repository = repository

    async def save(self, model_dto: BreakingPostDTO) -> list[BaseIdDTO] | None:
        result_orm = await self._repository.save(**model_dto.model_dump(exclude_none=True))

        if result_orm:
            return [BaseIdDTO(id=result_orm)]

        return None

    async def get(self, model_dto: BaseIdDTO | BreakingPartialDTO) -> list[BreakingServiceRelDTO] | None:
        result_orm = await self._repository.get(**model_dto.model_dump(exclude_none=True))

        if result_orm:
            return [BreakingServiceRelDTO.model_validate(res, from_attributes=True) for res in result_orm]

        return None

    async def get_breaking_standardize(self, model_dto: BaseIdDTO | BreakingPartialDTO) -> list[BreakingDTO] | None:
        result_orm = await self._repository.get(specification_filter=DeleteSpaceAndLowerCaseSpecification,
                                                **model_dto.model_dump(exclude_none=True))
        if result_orm:
            return [BreakingDTO.model_validate(res, from_attributes=True) for res in result_orm]

        return None

    async def get_all(self) -> list[BreakingDTO] | None:
        result_orm = await self._repository.get()

        if result_orm:
            return [BreakingDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def delete(self, model_dto: BaseIdDTO) -> list[BreakingDTO] | None:
        result_dto = await self.get(model_dto)

        if result_dto:
            delete_result = await self._repository.delete(id=model_dto.id)

            if delete_result:
                return result_dto

        return None

    async def update(self, model_dto: BreakingPartialDTO) -> list[BreakingDTO] | None:
        result_orm = await self._repository.update(**model_dto.model_dump(exclude_none=True))

        if result_orm:
            return [BreakingDTO.model_validate(result_orm, from_attributes=True)]

        return None
