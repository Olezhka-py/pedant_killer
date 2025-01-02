import asyncio

from pedant_killer.database.repository import AccessLevelRepository
from pedant_killer.database.models import AccessLevelOrm
from pedant_killer.database.schemas import AccessLevelDTO
from core import CoreMethod


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

