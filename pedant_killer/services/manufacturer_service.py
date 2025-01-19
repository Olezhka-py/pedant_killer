import asyncio

from pedant_killer.services.core_service import CoreMethod
from pedant_killer.database.repository import ManufacturerRepository
from pedant_killer.database.models import ManufacturerOrm
from pedant_killer.database.schemas import ManufacturerDTO


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

