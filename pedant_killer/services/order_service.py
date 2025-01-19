import asyncio

from pedant_killer.services.core_service import CoreMethod
from pedant_killer.database.repository import OrderRepository
from pedant_killer.database.models import OrderOrm, DeviceServiceOrm
from pedant_killer.database.schemas import (DeviceServiceDTO,
                                            OrderDTO,
                                            OrderDeviceServiceRelDTO,
                                            OrderClientRelDTO,
                                            OrderMasterRelDTO,
                                            OrderOrderStatusRelDTO,
                                            UserDTO)
from user_service import UserService


class OrderService(CoreMethod):
    async def save_order(self, client_id: int, master_id: int | None = None,  # TODO: Проверять, есть ли доступ у мастера
                         status_id: int = 1,
                         sent_from_address: str | None = None,
                         return_to_address: str | None = None,
                         comment: str | None = None,
                         rating: str | None = None) -> [int | None]:
        sorted_tables_arguments = self.checking_for_empty_attributes(
            client_id=client_id,
            master_id=master_id,
            status_id=status_id,
            sent_from_address=sent_from_address,
            return_to_address=return_to_address,
            comment=comment,
            rating=rating
        )

        user = UserService()
        master_access_level = await user.get_relationship_access_level(master_id)
        client_access_level = await user.get_relationship_access_level(client_id)

        if (sorted_tables_arguments is not None
                and self.checking_correctness_identifier(client_id)
                and master_access_level.access_level.importance == 30
                and client_access_level.access_level.importance == 10):
            repository = OrderRepository()
            return await repository.save(OrderOrm, **sorted_tables_arguments)

        return None

    async def save_relationship_order_device_service(self, order_id: int,
                                                     device_service_id: int) -> [DeviceServiceDTO | None]:
        if self.checking_correctness_identifier(order_id, device_service_id):

            repository = OrderRepository()
            result_orm = await repository.save_order_device_service(OrderOrm,
                                                                    DeviceServiceOrm,
                                                                    order_id=order_id,
                                                                    device_service_id=device_service_id
                                                                    )

            if result_orm:
                return [DeviceServiceDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_order(self, instance_id: int) -> [OrderDTO | None]:
        if self.checking_correctness_identifier(instance_id):
            repository = OrderRepository()
            result_orm = await repository.get(OrderOrm, instance_id=instance_id)

            if result_orm:
                return [OrderDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_relationship_device_service(self, instance_id: int) -> [OrderDeviceServiceRelDTO | None]:

        if self.checking_correctness_identifier(instance_id):

            repository = OrderRepository()
            result_orm = await repository.get_order_device_service(OrderOrm, instance_id=instance_id)

            if result_orm:
                return [OrderDeviceServiceRelDTO.model_validate(result_orm, from_attributes=True)]

    async def get_relationship_client(self, instance_id: int) -> [OrderClientRelDTO | None]:
        if self.checking_correctness_identifier(instance_id):
            repository = OrderRepository()
            result_orm = await repository.get_client(OrderOrm, instance_id=instance_id)

            if result_orm:
                return [OrderClientRelDTO.model_validate(row, from_attributes=True) for row in result_orm]

            return None

    async def get_relationship_master(self, instance_id: int) -> [OrderMasterRelDTO | None]:
        if self.checking_correctness_identifier(instance_id):
            repository = OrderRepository()
            result_orm = await repository.get_master(OrderOrm, instance_id=instance_id)

            if result_orm:
                return [OrderMasterRelDTO.model_validate(result_orm, from_attributes=True)]

            return None

    async def get_relationship_status(self, instance_id: int) -> [OrderOrderStatusRelDTO | None]:
        if self.checking_correctness_identifier(instance_id):
            repository = OrderRepository()
            result_orm = await repository.get_status(OrderOrm, instance_id)

            if result_orm:
                return [OrderOrderStatusRelDTO.model_validate(result_orm, from_attributes=True)]

    @staticmethod
    async def get_all_orders() -> [list[UserDTO] | None]:
        repository = OrderRepository()
        result_orm = await repository.get_all(OrderOrm)

        if result_orm:
            return [OrderDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def delete_order(self, instance_id: int) -> [OrderDTO | None]:
        if self.checking_correctness_identifier(instance_id):
            repository = OrderRepository()

            async with asyncio.TaskGroup() as tg:
                instance_task = tg.create_task(self.get_order(instance_id))
                delete_task = tg.create_task(repository.delete(OrderOrm, instance_id))

            result_orm = await instance_task
            await delete_task

            if result_orm:
                return [OrderDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def update_order(self, instance_id: int,
                           client_id: int,
                           master_id: int | None = None,
                           status_id: int = 1,
                           sent_from_address: str | None = None,
                           return_to_address: str | None = None,
                           comment: str | None = None,
                           rating: str | None = None
                           ) -> [OrderDTO | None]:  # TODO: Нужно сделать нормальную проверку
        sorted_tables_arguments = self.checking_for_empty_attributes(
            client_id=client_id,
            master_id=master_id,
            status_id=status_id,
            sent_from_address=sent_from_address,
            return_to_address=return_to_address,
            comment=comment,
            rating=rating
        )

        if sorted_tables_arguments is not None and self.checking_correctness_identifier(instance_id):
            repository = OrderRepository()
            result_orm = await repository.update(OrderOrm, instance_id, **sorted_tables_arguments)

            if result_orm:
                return [OrderDTO.model_validate(result_orm, from_attributes=True)]

        return None

