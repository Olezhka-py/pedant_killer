# from data_access_object import CoreDAO
from typing import Any
import asyncio
import inspect

from pedant_killer.database.models import *
from pedant_killer.database.database import database_logger
from pedant_killer.database.repository import *
from pedant_killer.database.specification import ObjectExistsByIdSpecification
from pedant_killer.database.schemas import *
import sys


class CoreMethod:
    @staticmethod
    def checking_for_empty_attributes(**kwargs: Any) -> [dict[Any, Any] | None]:
        sorted_dictionary = {key: value for key, value in kwargs.items() if value is not None}

        frame = inspect.currentframe()
        caller_frame = frame.f_back
        caller_name = caller_frame.f_code.co_name

        if not sorted_dictionary:
            database_logger.info(f'В метод {caller_name} не переданы аргументы')
            return None

        database_logger.info(f'В метод {caller_name} передано {len(sorted_dictionary)} аргументов')
        return sorted_dictionary

    @staticmethod
    def checking_correctness_identifier(*values: Any) -> bool:
        frame = inspect.currentframe()
        caller_frame = frame.f_back
        caller_name = caller_frame.f_code.co_name

        if not all(isinstance(identifier, int) and identifier > 0 for identifier in values):
            database_logger.error(f'Некорректный идентификатор: {values} переданный в функцию {caller_name}')
            return False

        return True

    @staticmethod
    def checking_correctness_type_str(*values: Any) -> bool:
        frame = inspect.currentframe()
        caller_frame = frame.f_back
        caller_name = caller_frame.f_code.co_name
        result = all(isinstance(value, str) for value in values)

        if not result:
            database_logger.info(f'Некорректные данные: {values} переданные в функцию {caller_name}')
            return False

        return True

    @staticmethod
    def checking_correctness_type_int(*values: Any) -> bool:
        frame = inspect.currentframe()
        caller_frame = frame.f_back
        caller_name = caller_frame.f_code.co_name
        result = all(isinstance(value, int) for value in values)

        if not result:
            database_logger.info(f'Некорректные данные: {values} переданные в функцию {caller_name}')
            return False

        return True


class ManufacturerService(CoreMethod):

    async def save_manufacturer(self, name: str, description: str | None = None) -> [int | None]:
        sorted_tables_arguments = self.checking_for_empty_attributes(name=name, description=description)
        if (sorted_tables_arguments is not None
                and self.checking_correctness_type_str(*sorted_tables_arguments.values())):
            repository = ManufacturerRepository()
            return await repository.save(ManufacturerOrm, **sorted_tables_arguments)

        return None

    async def get_manufacturer(self, instance_id: int) -> [ManufacturerDTO | None]:
        if self.checking_correctness_identifier(instance_id):
            repository = ManufacturerRepository()
            result_orm = await repository.get(ManufacturerOrm, instance_id=instance_id)

            if result_orm:
                return [ManufacturerDTO.model_validate(result_orm, from_attributes=True)]

        return None

    @staticmethod
    async def get_all_manufacturer() -> [list[ManufacturerDTO] | None]:
        repository = ManufacturerRepository()
        result_orm = await repository.get_all(ManufacturerOrm)

        if result_orm:
            return [ManufacturerDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def delete_manufacturer(self, instance_id: int) -> [ManufacturerDTO | None]:
        if self.checking_correctness_identifier(instance_id):
            repository = ManufacturerRepository()

            async with asyncio.TaskGroup() as tg:
                instance_task = tg.create_task(self.get_manufacturer(instance_id))
                delete_task = tg.create_task(repository.delete(ManufacturerOrm, instance_id))

            result_orm = await instance_task
            await delete_task

            if result_orm:
                return [ManufacturerDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def update_manufacturer(self, instance_id: int, name: str | None = None,
                                  description: str | None = None) -> [ManufacturerDTO | None]:
        sorted_tables_arguments = self.checking_for_empty_attributes(name=name, description=description)

        if (sorted_tables_arguments is not None and self.checking_correctness_identifier(instance_id)
                and self.checking_correctness_type_str(*sorted_tables_arguments.values())):
            repository = ManufacturerRepository()
            result_orm = await repository.update(ManufacturerOrm, instance_id, **sorted_tables_arguments)

            if result_orm:
                return [ManufacturerDTO.model_validate(result_orm, from_attributes=True)]

        return None


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
                return [ManufacturerDTO.model_validate(row, from_attributes=True) for row in instance]

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


class ManufacturerDeviceTypeService(CoreMethod):
    async def save_manufacturer_device_type(self, manufacturer_id: int, device_type_id: int) -> [int | None]:
        sorted_tables_arguments = self.checking_for_empty_attributes(
            manufacturer_id=manufacturer_id,
            device_type_id=device_type_id
        )

        if (sorted_tables_arguments is not None
                and self.checking_correctness_identifier(manufacturer_id, device_type_id)):
            repository = ManufacturerDeviceTypeRepository()
            return await repository.save(ManufacturerDeviceTypeOrm, **sorted_tables_arguments)

        return None

    async def save_and_create_manufacturer_device_type(self, manufacturer_data: dict[str, str],
                                                       device_type_data: dict[str, str]
                                                       ) -> [int | None]:
        sorted_tables_arguments_manufacturer = self.checking_for_empty_attributes(**manufacturer_data)
        sorted_tables_arguments_device_type = self.checking_for_empty_attributes(**device_type_data)

        if sorted_tables_arguments_manufacturer is not None and sorted_tables_arguments_device_type is not None:
            repository = ManufacturerDeviceTypeRepository()
            manufacturer = ManufacturerService()
            device_type = DeviceTypeService()

            async with asyncio.TaskGroup() as tg:
                manufacturer_task = tg.create_task(manufacturer.save_manufacturer(**sorted_tables_arguments_manufacturer))
                device_type_task = tg.create_task(device_type.save_device_type(**sorted_tables_arguments_device_type))

            return await repository.save(
                ManufacturerDeviceTypeOrm,
                manufacturer_id=manufacturer_task.result(),
                device_type_id=device_type_task.result()
            )

        return None

    async def get_manufacturer_device_type(self, instance_id: int) -> [ManufacturerDeviceTypeDTO | None]:
        if self.checking_correctness_identifier(instance_id):
            repository = ManufacturerDeviceTypeRepository()
            result_orm = await repository.get(ManufacturerDeviceTypeOrm, instance_id=instance_id)

            if result_orm:
                return [ManufacturerDeviceTypeDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_relationship_manufacturer(self, instance_id: int) -> [ManufacturerRelDTO | None]:
        if self.checking_correctness_identifier(instance_id):
            repository = ManufacturerDeviceTypeRepository()
            result_orm = await repository.get_manufacturer(ManufacturerDeviceTypeOrm, instance_id=instance_id)

            if result_orm:
                return [ManufacturerRelDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_relationship_device_type(self, instance_id: int) -> [DeviceTypeRelDTO | None]:
        if self.checking_correctness_identifier(instance_id):
            repository = ManufacturerDeviceTypeRepository()
            result_orm = await repository.get_device_type(ManufacturerDeviceTypeOrm, instance_id=instance_id)

            if result_orm:
                return [DeviceTypeRelDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_relationship_manufacturer_device_type(self, instance_id: int
                                                        ) -> [ManufacturerAndDeviceTypeRelDTO | None]:
        if self.checking_correctness_identifier(instance_id):
            repository = ManufacturerDeviceTypeRepository()
            result_orm = await repository.get_manufacturer_device_type(
                ManufacturerDeviceTypeOrm,
                instance_id=instance_id
            )

            if result_orm:
                return [ManufacturerAndDeviceTypeRelDTO.model_validate(result_orm, from_attributes=True)]

        return None

    @staticmethod
    async def get_all_manufacturer_device_types() -> [list[ManufacturerDeviceTypeDTO] | None]:
        repository = ManufacturerDeviceTypeRepository()
        result_orm = await repository.get_all(ManufacturerDeviceTypeOrm)

        if result_orm:
            return [ManufacturerDeviceTypeDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def delete_manufacturer_device_type(self, instance_id: int) -> [ManufacturerDeviceTypeDTO | None]:
        if self.checking_correctness_identifier(instance_id):
            repository = DeviceTypeRepository()

            async with asyncio.TaskGroup() as tg:
                instance_task = tg.create_task(self.get_manufacturer_device_type(instance_id))
                delete_task = tg.create_task(repository.delete(ManufacturerDeviceTypeOrm, instance_id))

            instance = await instance_task
            await delete_task

            if instance:
                return [ManufacturerDeviceTypeDTO.model_validate(row, from_attributes=True) for row in instance]

        return None

    async def update_manufacturer_device_type_id(self, instance_id: int, manufacturer_id: int,
                                                 device_type_id: int) -> [ManufacturerDeviceTypeDTO | None]:
        if (self.checking_correctness_identifier(instance_id)
                and self.checking_correctness_identifier(manufacturer_id)
                or self.checking_correctness_identifier(device_type_id)):
            repository = ManufacturerDeviceTypeRepository()
            result_orm = await repository.update(
                ManufacturerDeviceTypeOrm,
                instance_id=instance_id,
                manufacturer_id=manufacturer_id,
                device_type_id=device_type_id
            )

            if result_orm:
                return [ManufacturerDeviceTypeDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def update_relationship_manufacturer(self, instance_id: int, name: str = None,
                                               description: str = None) -> [ManufacturerRelDTO | None]:
        sorted_tables_arguments = self.checking_for_empty_attributes(name=name, description=description)

        if sorted_tables_arguments is not None and self.checking_correctness_identifier(instance_id):
            manufacturer = ManufacturerService()
            repository = ManufacturerDeviceTypeRepository()
            instance = await repository.get_manufacturer(ManufacturerDeviceTypeOrm, instance_id)

            if instance:
                return await manufacturer.update_manufacturer(instance.manufacturer_id, **sorted_tables_arguments)

        return None

    async def update_relationship_device_type(self, instance_id: int, name: str = None,
                                              description: str = None) -> [DeviceTypeOrm | None]:
        sorted_tables_arguments = self.checking_for_empty_attributes(name=name, description=description)

        if sorted_tables_arguments is not None and self.checking_correctness_identifier(instance_id):
            device_type = DeviceTypeService()
            repository = ManufacturerDeviceTypeRepository()
            instance = await repository.get_device_type(ManufacturerDeviceTypeOrm, instance_id)

            if instance:
                return await device_type.update_device_type(instance.device_type_id, **sorted_tables_arguments)

        return None


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


class ServiceService(CoreMethod):
    async def save_service(self, name: str, description: str | None = None) -> [int | None]:
        sorted_tables_arguments = self.checking_for_empty_attributes(name=name, description=description)
        if (sorted_tables_arguments is not None
                and self.checking_correctness_type_str(*sorted_tables_arguments.values())):
            repository = ServiceRepository()
            return await repository.save(ServiceOrm, **sorted_tables_arguments)

        return None

    async def get_service(self, instance_id: int) -> [ServiceDTO | None]:
        if self.checking_correctness_identifier(instance_id):
            repository = ManufacturerRepository()
            result_orm = await repository.get(ServiceOrm, instance_id=instance_id)

            if result_orm:
                return [ServiceDTO.model_validate(result_orm, from_attributes=True)]

        return None

    @staticmethod
    async def get_all_service() -> [list[ServiceDTO] | None]:
        repository = ServiceRepository()
        result_orm = await repository.get_all(ServiceOrm)

        if result_orm:
            return [ServiceDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def delete_service(self, instance_id: int) -> [ServiceDTO | None]:
        if self.checking_correctness_identifier(instance_id):
            repository = ServiceRepository()

            async with asyncio.TaskGroup() as tg:
                instance_task = tg.create_task(self.get_service(instance_id))
                delete_task = tg.create_task(repository.delete(ServiceOrm, instance_id))

            result_orm = await instance_task
            await delete_task

            if result_orm:
                return [ServiceDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def update_service(self, instance_id: int, name: str | None = None,
                             description: str | None = None) -> [ServiceDTO | None]:
        sorted_tables_arguments = self.checking_for_empty_attributes(name=name, description=description)

        if (sorted_tables_arguments is not None and self.checking_correctness_identifier(instance_id)
                and self.checking_correctness_type_str(*sorted_tables_arguments.values())):
            repository = ServiceRepository()
            result_orm = await repository.update(ServiceOrm, instance_id, **sorted_tables_arguments)

            if result_orm:
                return [ServiceDTO.model_validate(result_orm, from_attributes=True)]

        return None


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


class AccessLevelService(CoreMethod):
    async def save_access_level(self, name: str, importance: int) -> [int | None]:
        sorted_tables_arguments = self.checking_for_empty_attributes(name=name, importance=importance)
        if (len(sorted_tables_arguments) == 2
                and isinstance(name, str)
                and isinstance(importance, int)):
            repository = AccessLevelRepository()
            return await repository.save(AccessLevelOrm, **sorted_tables_arguments)

        return None

    async def get_access_level(self, instance_id: int) -> [AccessLevelDTO | None]:
        if self.checking_correctness_identifier(instance_id):
            repository = AccessLevelRepository()
            result_orm = await repository.get(AccessLevelOrm, instance_id=instance_id)

            if result_orm:
                return [AccessLevelDTO.model_validate(result_orm, from_attributes=True)]

        return None

    @staticmethod
    async def get_all_access_level() -> [list[AccessLevelDTO] | None]:
        repository = AccessLevelRepository()
        result_orm = await repository.get_all(AccessLevelOrm)

        if result_orm:
            return [AccessLevelDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def delete_access_level(self, instance_id: int) -> [AccessLevelDTO | None]:
        if self.checking_correctness_identifier(instance_id):
            repository = AccessLevelRepository()

            async with asyncio.TaskGroup() as tg:
                instance_task = tg.create_task(self.get_access_level(instance_id))
                delete_task = tg.create_task(repository.delete(AccessLevelOrm, instance_id))

            result_orm = await instance_task
            await delete_task

            if result_orm:
                return [AccessLevelDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None


class UserService(CoreMethod):

    async def save_user(self, access_level_id: int, telegram_username: str, telegram_id: str,
                        full_name: str, address: str, phone: str) -> [int | None]:
        sorted_tables_arguments = self.checking_for_empty_attributes(
            access_level_id=access_level_id,
            telegram_username=telegram_username,
            telegram_id=telegram_id,
            full_name=full_name,
            address=address,
            phone=phone
        )

        if (len(sorted_tables_arguments) == 6
                and self.checking_correctness_type_str(*[*sorted_tables_arguments.values()][1:])
                and self.checking_correctness_type_int(*[*sorted_tables_arguments.values()][:1])):
            repository = UserRepository()
            return await repository.save(UserOrm, **sorted_tables_arguments)

        return None

    async def get_user(self, instance_id: int) -> [UserDTO | None]:
        if self.checking_correctness_identifier(instance_id):
            repository = UserRepository()
            result_orm = await repository.get(UserOrm, instance_id=instance_id)

            if result_orm:
                return [UserDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_relationship_orders(self, instance_id: int) -> [list[UserAllRelDTO] | None]:  # TODO: Проверить работоспособность
        if self.checking_correctness_identifier(instance_id):
            repository = UserRepository()
            result_orm = await repository.get_orders(UserOrm, instance_id=instance_id)

            if result_orm:
                return [UserAllRelDTO.model_validate(row, from_attributes=True) for row in result_orm]

            return None

    @staticmethod
    async def get_all_user() -> [list[UserDTO] | None]:
        repository = UserRepository()
        result_orm = await repository.get_all(UserOrm)

        if result_orm:
            return [UserDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def delete_user(self, instance_id: int) -> [UserDTO | None]:
        if self.checking_correctness_identifier(instance_id):
            repository = UserRepository()

            async with asyncio.TaskGroup() as tg:
                instance_task = tg.create_task(self.get_user(instance_id))
                delete_task = tg.create_task(repository.delete(UserOrm, instance_id))

            result_orm = await instance_task
            await delete_task

            if result_orm:
                return [UserDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def update_user(self, instance_id: int, access_level_id: int | None = None,
                          telegram_username: str | None = None, telegram_id: str | None = None,
                          full_name: str | None = None, address: str | None = None, phone: str | None = None
                          ) -> [UserDTO | None]:  # TODO: Нужно сделать нормальную проверку
        sorted_tables_arguments = self.checking_for_empty_attributes(
            access_level_id=access_level_id,
            telegram_username=telegram_username,
            telegram_id=telegram_id,
            full_name=full_name,
            address=address,
            phome=phone
        )

        if (sorted_tables_arguments is not None and self.checking_correctness_identifier(instance_id)
                and self.checking_correctness_type_str(*sorted_tables_arguments.values())):
            repository = ManufacturerRepository()
            result_orm = await repository.update(UserOrm, instance_id, **sorted_tables_arguments)

            if result_orm:
                return [UserDTO.model_validate(result_orm, from_attributes=True)]

        return None


class OrderService(CoreMethod):
    async def save_order(self, client_id: int, master_id: int | None = None,
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

        if (sorted_tables_arguments is not None
                and self.checking_correctness_identifier(client_id)):
            repository = OrderRepository()
            return await repository.save(OrderOrm, **sorted_tables_arguments)

        return None

    async def get_order(self, instance_id: int) -> [OrderDTO | None]:
        if self.checking_correctness_identifier(instance_id):
            repository = OrderRepository()
            result_orm = await repository.get(OrderOrm, instance_id=instance_id)

            if result_orm:
                return [OrderDTO.model_validate(result_orm, from_attributes=True)]

        return None

    @staticmethod
    async def get_all_user() -> [list[UserDTO] | None]:
        repository = UserRepository()
        result_orm = await repository.get_all(UserOrm)

        if result_orm:
            return [UserDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def delete_user(self, instance_id: int) -> [UserDTO | None]:
        if self.checking_correctness_identifier(instance_id):
            repository = UserRepository()

            async with asyncio.TaskGroup() as tg:
                instance_task = tg.create_task(self.get_user(instance_id))
                delete_task = tg.create_task(repository.delete(UserOrm, instance_id))

            result_orm = await instance_task
            await delete_task

            if result_orm:
                return [UserDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def update_user(self, instance_id: int, access_level_id: int | None = None,
                          telegram_username: str | None = None, telegram_id: str | None = None,
                          full_name: str | None = None, address: str | None = None, phone: str | None = None
                          ) -> [UserDTO | None]:  # TODO: Нужно сделать нормальную проверку
        sorted_tables_arguments = self.checking_for_empty_attributes(
            access_level_id=access_level_id,
            telegram_username=telegram_username,
            telegram_id=telegram_id,
            full_name=full_name,
            address=address,
            phome=phone
        )

        if (sorted_tables_arguments is not None and self.checking_correctness_identifier(instance_id)
                and self.checking_correctness_type_str(*sorted_tables_arguments.values())):
            repository = ManufacturerRepository()
            result_orm = await repository.update(UserOrm, instance_id, **sorted_tables_arguments)

            if result_orm:
                return [UserDTO.model_validate(result_orm, from_attributes=True)]

        return None








async def ggvp():
    m = UserService()
    #g = await m.save_order(2, 3, 1, 'cherepovets', 'moscow', 'nice', '10')
    #m = await s.save_user(27, 'i_am_gg', 'sdfsdf', 'dima', 'cherepovets', '9000000000')
    g = await m.get_relationship_orders(3)
    print(g)

asyncio.run(ggvp())
