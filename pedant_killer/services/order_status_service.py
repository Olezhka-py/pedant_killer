import asyncio
from typing import TYPE_CHECKING

from pedant_killer.schemas.order_status_schema import (OrderStatusPostDTO,
                                                       OrderStatusPartialDTO,
                                                       OrderStatusDTO,
                                                       BaseIdDTO)
if TYPE_CHECKING:
    from pedant_killer.database.repository import OrderStatusRepository


class OrderStatusService:
    def __init__(self, repository: 'OrderStatusRepository') -> None:
        self._repository = repository

    async def save_order_status(self, model_dto: OrderStatusPostDTO) -> list[BaseIdDTO] | None:
        result_orm = await self._repository.save(**model_dto.model_dump(exclude_none=True))

        if result_orm:
            return [BaseIdDTO(id=result_orm)]

        return None

    async def get_order_status(self, model_dto: OrderStatusPartialDTO | BaseIdDTO) -> list[OrderStatusDTO] | None:
        result_orm = await self._repository.get(**model_dto.model_dump(exclude_none=True))

        if result_orm:
            return [OrderStatusDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_all_order_status(self) -> list[OrderStatusDTO] | None:
        result_orm = await self._repository.get_all()

        if result_orm:
            return [OrderStatusDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def delete_order_status(self, model_dto: BaseIdDTO) -> list[OrderStatusDTO] | None:

        async with asyncio.TaskGroup() as tg:
            instance_task = tg.create_task(self.get_order_status(model_dto))
            delete_task = tg.create_task(self._repository.delete(instance_id=model_dto.id))

        result_orm = await instance_task
        delete_orm = delete_task

        if result_orm and delete_orm:
            return [OrderStatusDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None
