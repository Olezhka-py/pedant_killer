from pedant_killer.schemas.service_breaking_schema import (ServiceDTO,
                                                           BaseIdDTO,
                                                           ServicePostDTO,
                                                           ServicePartialDTO,
                                                           ServiceIdListDTO, ServiceBreakingRelDTO)
from pedant_killer.database.repository import ServiceRepository


class ServiceService:
    def __init__(self, repository: 'ServiceRepository') -> None:
        self._repository = repository

    async def save(self, model_dto: ServicePostDTO) -> list[BaseIdDTO] | None:
        result_orm = await self._repository.save(**model_dto.model_dump(exclude_none=True))

        if result_orm:
            return [BaseIdDTO(id=result_orm)]

        return None

    async def get(self, model_dto: ServicePartialDTO | BaseIdDTO | ServiceIdListDTO
                  ) -> list[ServiceBreakingRelDTO] | None:
        result_orm = await self._repository.get(**model_dto.model_dump(exclude_none=True))

        if result_orm:
            return [ServiceBreakingRelDTO.model_validate(res, from_attributes=True) for res in result_orm]

        return None

    async def get_by_id_list(self, model_dto: BaseIdDTO | ServiceIdListDTO) -> list[ServiceBreakingRelDTO] | None:
        result_orm = await self._repository.get(specification_filter=IdInListServicesSpecification,
                                                **model_dto.model_dump(exclude_none=True))

        if result_orm:
            return [ServiceBreakingRelDTO.model_validate(res, from_attributes=True) for res in result_orm]

    async def get_all(self) -> list[ServiceDTO] | None:
        result_orm = await self._repository.get()

        if result_orm:
            return [ServiceDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def delete(self, model_dto: BaseIdDTO) -> list[ServiceDTO] | None:
        result_dto = await self.get(model_dto)

        if result_dto:
            delete_result = await self._repository.delete(id=model_dto.id)

            if delete_result:
                return result_dto

        return None

    async def update(self, model_dto: ServicePartialDTO) -> list[ServiceDTO] | None:
        result_orm = await self._repository.update(**model_dto.model_dump(exclude_none=True))

        if result_orm:
            return [ServiceDTO.model_validate(result_orm, from_attributes=True)]

        return None
