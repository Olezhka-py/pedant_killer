import asyncio

from core import CoreMethod
from pedant_killer.database.repository import DeviceTypeRepository, DeviceRepository
from pedant_killer.database.models import DeviceTypeOrm
from pedant_killer.database.schemas import DeviceTypeDTO


class DeviceTypeService(CoreMethod):
    async def save_device_type(self, name: str, description: str | None = None) -> [int | None]:
        sorted_tables_arguments = self.checking_for_empty_attributes(name=name, description=description)

        if (sorted_tables_arguments is not None
                and self.checking_correctness_type_str(*sorted_tables_arguments.values())):
            repository = DeviceTypeRepository()
            return await repository.save(DeviceTypeOrm, **sorted_tables_arguments)

        return None

    async def get_device_type(self, instance_id: int) -> [DeviceTypeDTO | None]:
        if self.checking_correctness_identifier(instance_id):
            repository = DeviceTypeRepository()
            result_orm = await repository.get(DeviceTypeOrm, instance_id=instance_id)

            if result_orm:
                return [DeviceTypeDTO.model_validate(result_orm, from_attributes=True)]

        return None

    @staticmethod
    async def get_all_device_type() -> [list[DeviceTypeDTO] | None]:
        repository = DeviceTypeRepository()
        result_orm = await repository.get_all(DeviceTypeOrm)

        if result_orm:
            return [DeviceTypeDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def delete_device_type(self, instance_id: int) -> [DeviceTypeDTO | None]:
        if self.checking_correctness_identifier(instance_id):
            repository = DeviceRepository()

            async with asyncio.TaskGroup() as tg:
                instance_task = tg.create_task(self.get_device_type(instance_id))
                delete_task = tg.create_task(repository.delete(DeviceTypeOrm, instance_id=instance_id))

            instance = await instance_task
            await delete_task

            if instance:
                return [DeviceTypeDTO.model_validate(row, from_attributes=True) for row in instance]

        return None

    async def update_device_type(self, instance_id: int, name: str | None = None,
                                  description: str | None = None) -> [DeviceTypeDTO | None]:
        sorted_tables_arguments = self.checking_for_empty_attributes(name=name, description=description)

        if (sorted_tables_arguments is not None and self.checking_correctness_identifier(instance_id)
                and self.checking_correctness_type_str(*sorted_tables_arguments.values())):
            repository = DeviceTypeRepository()
            result_orm = await repository.update(DeviceTypeOrm, instance_id, **sorted_tables_arguments)

            if result_orm:
                return [DeviceTypeDTO.model_validate(result_orm, from_attributes=True)]

        return None

