# from data_access_object import CoreDAO
import asyncio

from models import *
from database import database_logger
from repository import ManufacturerRepository, DeviceTypeRepository
from specification import ObjectExistsByIdSpecification
import sys


class ManufacturerService:

    async def save_manufacturer(self, name, description):
        repository = ManufacturerRepository()
        return await repository.save(ManufacturerOrm, name=name, description=description)

    async def get_manufacturer(self, instance_id):
        repository = ManufacturerRepository()
        return await repository.get(ManufacturerOrm, instance_id=instance_id, specification=ObjectExistsByIdSpecification)

    async def get_all_manufacturer(self):
        repository = ManufacturerRepository()
        return await repository.get_all(ManufacturerOrm)

    async def delete_manufacturer(self, instance_id):
        repository = ManufacturerRepository()
        result = await repository.delete(ManufacturerOrm, instance_id=instance_id, specifications=ObjectExistsByIdSpecification)
        return result

    async def update_manufacturer(self, instance_id, name, description):
        repository = ManufacturerRepository()
        return await repository.update(ManufacturerOrm, instance_id, name=name,
                                description=description, specification=ObjectExistsByIdSpecification)

class DeviceTypeService:
    def save_device_type(self, name, description):
        repository = DeviceTypeRepository()
        return repository.save(DeviceTypeOrm, name=name, description=description)

    def get_device_type(self, instance_id):
        repository = DeviceTypeRepository()
        return repository.get(DeviceTypeOrm, instance_id=instance_id, specification=ObjectExistsByIdSpecification)

    def delete_device_type(self, instance_id, data):
        repository = ManufacturerRepository()
        repository.delete(DeviceTypeOrm, instance_id=instance_id, data=data, specifications=ObjectExistsByIdSpecification)
# async def ggvp():
#     s = ManufacturerService()
#     #await s.save_manufacturer('asdas', 'asdasd')
#     g = await s.update_manufacturer(9, 'e', 'd')
#     print(g)
#
# asyncio.run(ggvp())


class ManufacturerDeviceTypeService:
    def save_manufacturer(self, manufacturer_id, device_type_id):
        pass