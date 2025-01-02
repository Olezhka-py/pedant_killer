import asyncio

from core import CoreMethod
from pedant_killer.database.repository import ServiceRepository
from pedant_killer.database.models import ServiceOrm
from pedant_killer.database.schemas import ServiceDTO


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
            repository = ServiceRepository()
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
