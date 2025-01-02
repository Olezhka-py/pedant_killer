import asyncio

from core import CoreMethod
from manufacturer_device_type import ManufacturerDeviceTypeService
from pedant_killer.database.repository import DeviceRepository, ManufacturerRepository
from pedant_killer.database.schemas import DeviceDTO, DeviceTypeDTO, ManufacturerDeviceTypeRelDTO
from pedant_killer.database.models import DeviceOrm, ManufacturerOrm


class DeviceService(CoreMethod):
    async def save_device(self, manufacturer_device_type_id: int, name_model: str) -> [int | None]:
        sorted_tables_arguments = self.checking_for_empty_attributes(
            manufacturer_device_type_id=manufacturer_device_type_id,
            name_model=name_model
        )

        if self.checking_correctness_identifier(manufacturer_device_type_id) and sorted_tables_arguments is not None:
            repository = DeviceRepository()
            return await repository.save(DeviceOrm, **sorted_tables_arguments)

        return None

    @staticmethod
    async def save_and_create_device(manufacturer_data: dict[str, str], device_type_data: dict[str, str],
                                     name_model: str) -> [int | None]:
        device = DeviceService()
        manufacturer_device_type = ManufacturerDeviceTypeService()
        manufacturer_device_type_id = await manufacturer_device_type.save_and_create_manufacturer_device_type(
            manufacturer_data,
            device_type_data
        )

        if manufacturer_device_type_id:
            result = await device.save_device(
                manufacturer_device_type_id=manufacturer_device_type_id,
                name_model=name_model
            )

            return result

        return None

    async def get_device(self, instance_id: int) -> [DeviceDTO | None]:
        if self.checking_correctness_identifier(instance_id):
            repository = DeviceRepository()
            result_orm = await repository.get(DeviceOrm, instance_id=instance_id)

            if result_orm:
                return [DeviceDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_relationship_manufacturer_device_type(self, instance_id: int) -> [DeviceDTO | None]:
        if self.checking_correctness_identifier(instance_id):
            repository = DeviceRepository()
            result_orm = await repository.get_manufacturer_device_type(DeviceOrm, instance_id=instance_id)

            if result_orm:
                return [ManufacturerDeviceTypeRelDTO.model_validate(result_orm, from_attributes=True)]

            return None

    @staticmethod
    async def get_all_device() -> [list[DeviceDTO] | None]:
        repository = DeviceRepository()
        result_orm = await repository.get_all(DeviceOrm)

        if result_orm:
            return [DeviceDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def delete_device(self, instance_id: int) -> [DeviceDTO | None]:
        if self.checking_correctness_identifier(instance_id):
            repository = DeviceRepository()

            async with asyncio.TaskGroup() as tg:
                instance_task = tg.create_task(self.get_device(instance_id))
                delete_task = tg.create_task(repository.delete(DeviceOrm, instance_id))

            instance = await instance_task
            await delete_task

            if instance:
                return [DeviceDTO.model_validate(row, from_attributes=True) for row in instance]

        return None

    async def update_device(self, instance_id, manufacturer_device_type_id, name_model) -> [DeviceTypeDTO | None]:
        if (self.checking_correctness_identifier(instance_id)
                and self.checking_correctness_identifier(manufacturer_device_type_id)):

            repository = ManufacturerRepository()
            result_orm = await repository.update(
                ManufacturerOrm,
                instance_id=instance_id,
                manufacturer_device_type_id=manufacturer_device_type_id,
                name_model=name_model
            )

            if result_orm:
                return [DeviceDTO.model_validate(result_orm, from_attributes=True)]

        return None

