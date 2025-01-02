import asyncio

from pedant_killer.services.core import CoreMethod
from pedant_killer.database.repository import ManufacturerRepository, DeviceServiceRepository
from pedant_killer.database.models import DeviceServiceOrm, OrderOrm
from pedant_killer.database.schemas import (DeviceServiceOrderRelDTO,
                                            DeviceServiceDTO,
                                            DeviceRelDTO,
                                            ServiceRelDTO,
                                            DeviceAndServiceRelDTO)


class DeviceServiceService(CoreMethod):
    async def save_device_service(self, device_id: int, service_id: int, price: int,
                                  work_duration: int | None = None) -> [int | None]:
        sorted_tables_arguments = self.checking_for_empty_attributes(
            device_id=device_id,
            service_id=service_id,
            price=price,
            work_duration=work_duration
        )
        if (sorted_tables_arguments is not None
                and self.checking_correctness_type_int(*sorted_tables_arguments.values())):
            repository = ManufacturerRepository()
            return await repository.save(DeviceServiceOrm, **sorted_tables_arguments)

        return None

    async def save_relationship_device_service(self, device_service_id, order_id
                                                ) -> [DeviceServiceOrderRelDTO | None]:
        if self.checking_correctness_identifier(order_id, device_service_id):

            repository = DeviceServiceRepository()
            return await repository.save_device_service_order(OrderOrm,
                                                              DeviceServiceOrm,
                                                              order_id=order_id,
                                                              device_service_id=device_service_id
                                                              )

        return None

    async def get_relationship_order(self, instance_id: int) -> [DeviceServiceDTO | None]:
        if self.checking_correctness_identifier(instance_id):
            repository = DeviceServiceRepository()
            result_orm = await repository.get_order(DeviceServiceOrm, instance_id=instance_id)

            if result_orm:
                return [DeviceServiceOrderRelDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_device_service(self, instance_id: int) -> [DeviceServiceDTO | None]:
        if self.checking_correctness_identifier(instance_id):
            repository = DeviceServiceRepository()
            result_orm = await repository.get(DeviceServiceOrm, instance_id=instance_id)

            if result_orm:
                return [DeviceServiceDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_relationship_device(self, instance_id: int) -> [DeviceRelDTO | None]:
        if self.checking_correctness_identifier(instance_id):
            repository = DeviceServiceRepository()
            result_orm = await repository.get_device(DeviceServiceOrm, instance_id=instance_id)

            if result_orm:
                return [DeviceRelDTO.model_validate(result_orm, from_attributes=True)]

            return None

    async def get_relationship_service(self, instance_id: int) -> [ServiceRelDTO | None]:
        if self.checking_correctness_identifier(instance_id):
            repository = DeviceServiceRepository()
            result_orm = await repository.get_service(DeviceServiceOrm, instance_id=instance_id)

            if result_orm:
                return [ServiceRelDTO.model_validate(result_orm, from_attributes=True)]

            return None

    async def get_relationship_device_service(self, instance_id: int) -> [DeviceAndServiceRelDTO | None]:
        if self.checking_correctness_identifier(instance_id):
            repository = DeviceServiceRepository()
            result_orm = await repository.get_device_service(DeviceServiceOrm, instance_id=instance_id)

            if result_orm:
                return [DeviceAndServiceRelDTO.model_validate(result_orm, from_attributes=True)]

            return None

    @staticmethod
    async def get_all_manufacturer() -> [list[DeviceServiceDTO] | None]:
        repository = DeviceServiceRepository()
        result_orm = await repository.get_all(DeviceServiceOrm)

        if result_orm:
            return [DeviceServiceDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def delete_device_service(self, instance_id: int) -> [DeviceServiceDTO | None]:
        if self.checking_correctness_identifier(instance_id):
            repository = DeviceServiceRepository()

            async with asyncio.TaskGroup() as tg:
                instance_task = tg.create_task(self.get_device_service(instance_id))
                delete_task = tg.create_task(repository.delete(DeviceServiceOrm, instance_id))

            result_orm = await instance_task
            await delete_task

            if result_orm:
                return [DeviceServiceDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def update_device_service(self, instance_id: int, device_id: int | None = None, service_id: int | None = None,
                                    price: int | None = None, work_duration: int | None = None
                                    ) -> [DeviceServiceDTO | None]:
        sorted_tables_arguments = self.checking_for_empty_attributes(
            device_id=device_id,
            service_id=service_id,
            price=price,
            work_duration=work_duration
        )

        if (sorted_tables_arguments is not None and self.checking_correctness_identifier(instance_id)
                and self.checking_correctness_type_int(*sorted_tables_arguments.values())):
            repository = DeviceServiceRepository()
            result_orm = await repository.update(DeviceServiceOrm, instance_id, **sorted_tables_arguments)

            if result_orm:
                return [DeviceServiceDTO.model_validate(result_orm, from_attributes=True)]

        return None

