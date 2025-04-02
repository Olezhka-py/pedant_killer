from typing import TYPE_CHECKING

from pedant_killer.schemas.common_schema import CoreModel, BaseIdDTO, optional
if TYPE_CHECKING:
    from pedant_killer.schemas.user_schema import UserDTO


class AccessLevelPostDTO(CoreModel):
    name: str
    importance: int


class AccessLevelDTO(BaseIdDTO, AccessLevelPostDTO):
    pass


@optional()
class AccessLevelPartialDTO(AccessLevelDTO):
    pass


class AccessLevelUserRelDTO(AccessLevelDTO):
    user: 'list[UserDTO] | None' = None
