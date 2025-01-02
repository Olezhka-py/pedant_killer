import asyncio

from core import CoreMethod
from pedant_killer.database.repository import UserRepository, ManufacturerRepository
from pedant_killer.database.models import UserOrm
from pedant_killer.database.schemas import (UserDTO,
                                            UserOrdersMasterRelDTO,
                                            UserOrdersClientRelDTO,
                                            UserAccessLevelRelDTO)


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

    async def get_relationship_master_orders(self, instance_id: int) -> [list[UserOrdersMasterRelDTO] | None]:  # TODO: Проверить работоспособность
        if self.checking_correctness_identifier(instance_id):
            repository = UserRepository()
            result_orm = await repository.get_master(UserOrm, instance_id=instance_id)

            if result_orm:
                return [UserOrdersMasterRelDTO.model_validate(row, from_attributes=True) for row in result_orm]

            return None

    async def get_relationship_client_orders(self, instance_id: int) -> [list[UserOrdersClientRelDTO] | None]:
        if self.checking_correctness_identifier(instance_id):
            repository = UserRepository()
            result_orm = await repository.get_client(UserOrm, instance_id=instance_id)

            if result_orm:
                return [UserOrdersMasterRelDTO.model_validate(row, from_attributes=True) for row in result_orm]

            return None

    async def get_relationship_access_level(self, instance_id: int) -> [UserAccessLevelRelDTO | None]:
        if self.checking_correctness_identifier(instance_id):
            repository = UserRepository()
            result_orm = await repository.get_access_level(UserOrm, instance_id=instance_id)

            if result_orm:
                return UserAccessLevelRelDTO.model_validate(result_orm, from_attributes=True)

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

