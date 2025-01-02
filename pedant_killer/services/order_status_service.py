import asyncio

from core import CoreMethod
from pedant_killer.database.repository import OrderStatusRepository
from pedant_killer.database.models import OrderStatusOrm
from pedant_killer.database.schemas import OrderStatusDTO


class OrderStatusService(CoreMethod):
    async def save_order_status(self, name: str, description: str | None = None) -> [int | None]:
        sorted_tables_arguments = self.checking_for_empty_attributes(name=name, description=description)

        if (sorted_tables_arguments is not None
                and self.checking_correctness_type_str(*sorted_tables_arguments.values())):
            repository = OrderStatusRepository()
            return await repository.save(OrderStatusOrm, **sorted_tables_arguments)

        return None

    async def get_order_status(self, instance_id: int) -> [OrderStatusDTO | None]:
        if self.checking_correctness_identifier(instance_id):
            repository = OrderStatusRepository()
            result_orm = await repository.get(OrderStatusOrm, instance_id=instance_id)

            if result_orm:
                return [OrderStatusDTO.model_validate(result_orm, from_attributes=True)]

        return None

    @staticmethod
    async def get_all_order_status() -> [list[OrderStatusDTO] | None]:
        repository = OrderStatusRepository()
        result_orm = await repository.get_all(OrderStatusOrm)

        if result_orm:
            return [OrderStatusDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def delete_order_status(self, instance_id: int) -> [OrderStatusDTO | None]:
        if self.checking_correctness_identifier(instance_id):
            repository = OrderStatusRepository()

            async with asyncio.TaskGroup() as tg:
                instance_task = tg.create_task(self.get_order_status(instance_id))
                delete_task = tg.create_task(repository.delete(OrderStatusRepository, instance_id=instance_id))

            instance = await instance_task
            await delete_task

            if instance:
                return [OrderStatusDTO.model_validate(row, from_attributes=True) for row in instance]

        return None