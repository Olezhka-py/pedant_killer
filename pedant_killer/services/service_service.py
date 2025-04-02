from typing import TYPE_CHECKING

from pedant_killer.schemas.service_schema import ServiceDTO, BaseIdDTO, ServicePostDTO, ServicePartialDTO
if TYPE_CHECKING:
    from pedant_killer.database.repository import ServiceRepository


class ServiceService:
    def __init__(self, repository: 'ServiceRepository') -> None:
        self._repository = repository

    async def save_service(self, model_dto: ServicePostDTO) -> list[BaseIdDTO] | None:
        result_orm = await self._repository.save(**model_dto.model_dump(exclude_none=True))

        if result_orm:
            return [BaseIdDTO(id=result_orm)]

        return None

    async def get_service(self, model_dto: ServicePartialDTO | BaseIdDTO) -> list[ServiceDTO] | None:
        result_orm = await self._repository.get(**model_dto.model_dump(exclude_none=True))

        if result_orm:
            return [ServiceDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_all_service(self) -> list[ServiceDTO] | None:
        result_orm = await self._repository.get()

        if result_orm:
            return [ServiceDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def delete_service(self, model_dto: BaseIdDTO) -> list[ServiceDTO] | None:
        result_dto = await self.get_service(model_dto)

        if result_dto:
            delete_result = await self._repository.delete(id=model_dto.id)

            if delete_result:
                return result_dto

        return None

    async def update_service(self, model_dto: ServicePartialDTO) -> list[ServiceDTO] | None:
        result_orm = await self._repository.update(**model_dto.model_dump(exclude_none=True))

        if result_orm:
            return [ServiceDTO.model_validate(result_orm, from_attributes=True)]

        return None
