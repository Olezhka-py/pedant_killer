from typing import TYPE_CHECKING
import asyncio

from pedant_killer.database.schemas import ServiceDTO, BaseIdDTO, ServicePostDTO
if TYPE_CHECKING:
    from pedant_killer.database.repository import ServiceRepository


class ServiceService:
    def __init__(self, repository: 'ServiceRepository') -> None:
        self._repository = repository

    async def save_service(self, model_dto: ServicePostDTO) -> list[BaseIdDTO] | None:
        result_orm = await self._repository.save(**model_dto.dict())

        if result_orm:
            return [BaseIdDTO(id=result_orm)]

        return None

    async def get_service(self, model_dto: BaseIdDTO) -> list[ServiceDTO] | None:
        result_orm = await self._repository.get(instance_id=model_dto.id)

        if result_orm:
            return [ServiceDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_all_service(self) -> list[ServiceDTO] | None:
        result_orm = await self._repository.get_all()

        if result_orm:
            return [ServiceDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def delete_service(self, model_dto: BaseIdDTO) -> list[ServiceDTO] | None:
        async with asyncio.TaskGroup() as tg:
            instance_task = tg.create_task(self.get_service(model_dto))
            delete_task = tg.create_task(self._repository.delete(instance_id=model_dto.id))

            result_orm = await instance_task
            await delete_task

            if result_orm:
                return [ServiceDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def update_service(self, model_dto: ServiceDTO) -> list[ServiceDTO] | None:
        result_orm = await self._repository.update(instance_id=model_dto.id,
                                                   name=model_dto.name,
                                                   description=model_dto.description)

        if result_orm:
            return [ServiceDTO.model_validate(result_orm, from_attributes=True)]

        return None
