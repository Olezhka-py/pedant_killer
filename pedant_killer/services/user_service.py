from typing import TYPE_CHECKING

from pedant_killer.schemas.user_schema import (UserDTO,
                                               UserPartialDTO,
                                               UserPostDTO,
                                               UserAccessLevelRelDTO,
                                               BaseIdDTO)
from pedant_killer.schemas.order_user_schema import UserOrdersMasterRelDTO, UserOrdersClientRelDTO
if TYPE_CHECKING:
    from pedant_killer.database.repository import UserRepository


class UserService:
    def __init__(self, repository: 'UserRepository') -> None:
        self._repository = repository

    async def save_user(self, model_dto: UserPostDTO) -> list[BaseIdDTO] | None:
        result_orm = await self._repository.save(**model_dto.model_dump(exclude_none=True))

        if result_orm:
            return [BaseIdDTO(id=result_orm)]

        return None

    async def get_user(self, model_dto: UserPartialDTO | BaseIdDTO) -> list[UserDTO] | None:
        result_orm = await self._repository.get(**model_dto.model_dump(exclude_none=True))

        if result_orm:
            return [UserDTO.model_validate(res, from_attributes=True) for res in result_orm]

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
        result_orm = await self._repository.get()

        if result_orm:
            return [UserDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def delete_user(self, model_dto: BaseIdDTO) -> list[UserDTO] | None:
        result_dto = await self.get_user(model_dto)

        if result_dto:
            delete_result = await self._repository.delete(id=model_dto.id)

            if delete_result:
                return result_dto

        return None

    async def update_user(self, model_dto: UserPartialDTO) -> list[UserDTO] | None:
        result_orm = await self._repository.update(**model_dto.model_dump(exclude_none=True))

        if result_orm:
            return [UserDTO.model_validate(result_orm, from_attributes=True)]

        return None
