from typing import TYPE_CHECKING
import asyncio

from pedant_killer.database.schemas import (UserDTO,
                                            UserPostDTO,
                                            UserOrdersMasterRelDTO,
                                            UserOrdersClientRelDTO,
                                            UserAccessLevelRelDTO,
                                            BaseIdDTO)
if TYPE_CHECKING:
    from pedant_killer.database.repository import UserRepository


class UserService:
    def __init__(self, repository: 'UserRepository') -> None:
        self._repository = repository

    async def save_user(self, model_dto: UserPostDTO) -> list[BaseIdDTO] | None:
        result_orm = await self._repository.save(**model_dto.dict())

        if result_orm:
            return [BaseIdDTO(id=result_orm)]

        return None

    async def get_user(self, model_dto: BaseIdDTO) -> list[UserDTO] | None:
        result_orm = await self._repository.get(instance_id=model_dto.id)

        if result_orm:
            return [UserDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_relationship_master_orders(self, model_dto: BaseIdDTO) -> list[UserOrdersMasterRelDTO] | None:  # TODO: Проверить работоспособность
        result_orm = await self._repository.get_master(instance_id=model_dto.id)

        if result_orm:
            return [UserOrdersMasterRelDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def get_relationship_client_orders(self, model_dto: BaseIdDTO) -> list[UserOrdersClientRelDTO] | None:
        result_orm = await self._repository.get_client(instance_id=model_dto.id)

        if result_orm:
            return [UserOrdersClientRelDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def get_relationship_access_level(self, model_dto: BaseIdDTO) -> list[UserAccessLevelRelDTO] | None:
        result_orm = await self._repository.get_access_level(instance_id=model_dto.id)

        if result_orm:
            return [UserAccessLevelRelDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_all_user(self) -> list[UserDTO] | None:
        result_orm = await self._repository.get_all()

        if result_orm:
            return [UserDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def delete_user(self, model_dto: BaseIdDTO) -> list[UserDTO] | None:
        async with asyncio.TaskGroup() as tg:
            instance_task = tg.create_task(self.get_user(model_dto))
            delete_task = tg.create_task(self._repository.delete(instance_id=model_dto.id))

        result_orm = await instance_task
        await delete_task

        if result_orm:
            return [UserDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def update_user(self, model_dto: UserDTO) -> list[UserDTO] | None:
        result_orm = await self._repository.update(instance_id=model_dto.id,
                                                   access_level_id=model_dto.access_level_id,
                                                   telegram_username=model_dto.telegram_username,
                                                   telegram_id=model_dto.telegram_id,
                                                   full_name=model_dto.full_name,
                                                   address=model_dto.address,
                                                   phone=model_dto.phone)

        if result_orm:
            return [UserDTO.model_validate(result_orm, from_attributes=True)]

        return None
