import asyncio
from typing import TYPE_CHECKING

from pedant_killer.database.schemas import (BaseIdDTO,
                                            OrderDTO,
                                            OrderDeviceServiceRelDTO,
                                            OrderClientRelDTO,
                                            OrderMasterRelDTO,
                                            OrderOrderStatusRelDTO,
                                            OrderPostDTO)
if TYPE_CHECKING:
    from pedant_killer.database.repository import OrderRepository


class OrderService:
    def __init__(self, repository: 'OrderRepository') -> None:
        self._repository = repository

    async def save_order(self, model_dto: OrderPostDTO) -> list[BaseIdDTO] | None:
        result_orm = await self._repository.save(**model_dto.dict())

        if result_orm:
            return [BaseIdDTO(id=result_orm)]

    # async def save_relationship_order_device_service(self, order_id: int,
    #                                                  device_service_id: int) -> [DeviceServiceDTO | None]:
    #     if self.checking_correctness_identifier(order_id, device_service_id):
    #
    #         repository = OrderRepository()
    #         result_orm = await repository.save_order_device_service(OrderOrm,
    #                                                                 DeviceServiceOrm,
    #                                                                 order_id=order_id,
    #                                                                 device_service_id=device_service_id
    #                                                                 )
    #
    #         if result_orm:
    #             return [DeviceServiceDTO.model_validate(result_orm, from_attributes=True)]
    #
    #     return None

    async def get_order(self, model_dto: BaseIdDTO) -> list[OrderDTO] | None:
        result_orm = await self._repository.get(instance_id=model_dto.id)

        if result_orm:
            return [OrderDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_relationship_device_service(self, model_dto: BaseIdDTO) -> list[OrderDeviceServiceRelDTO] | None:
        result_orm = await self._repository.get_order_device_service(instance_id=model_dto.id)

        if result_orm:
            return [OrderDeviceServiceRelDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_relationship_client(self, model_dto: BaseIdDTO) -> list[OrderClientRelDTO] | None:
        result_orm = await self._repository.get_client(instance_id=model_dto.id)

        if result_orm:
            return [OrderClientRelDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_relationship_master(self, model_dto: BaseIdDTO) -> list[OrderMasterRelDTO] | None:
        result_orm = await self._repository.get_master(instance_id=model_dto.id)

        if result_orm:
            return [OrderMasterRelDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_relationship_status(self, model_dto: BaseIdDTO) -> list[OrderOrderStatusRelDTO] | None:
        result_orm = await self._repository.get_status(instance_id=model_dto.id)

        if result_orm:
            return [OrderOrderStatusRelDTO.model_validate(result_orm, from_attributes=True)]

    async def get_all_orders(self) -> list[OrderDTO] | None:
        result_orm = await self._repository.get_all()

        if result_orm:
            return [OrderDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def delete_order(self, model_dto: BaseIdDTO) -> list[OrderDTO] | None:
        async with asyncio.TaskGroup() as tg:
            instance_task = tg.create_task(self.get_order(model_dto=model_dto))
            delete_task = tg.create_task(self._repository.delete(instance_id=model_dto.id))

        result_orm = await instance_task
        await delete_task

        if result_orm:
            return [OrderDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def update_order(self, model_dto: OrderDTO) -> list[OrderDTO] | None:
        result_orm = await self._repository.update(instance_id=model_dto.id,
                                                   client_id=model_dto.client_id,
                                                   master_id=model_dto.master_id,
                                                   status_id=model_dto.status_id,
                                                   sent_from_address=model_dto.sent_from_address,
                                                   return_to_address=model_dto.return_to_address,
                                                   comment=model_dto.comment,
                                                   rating=model_dto.rating)

        if result_orm:
            return [OrderDTO.model_validate(result_orm, from_attributes=True)]

        return None

