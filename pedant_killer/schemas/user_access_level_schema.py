from pedant_killer.schemas.user_schema import UserDTO
from pedant_killer.schemas.access_level_schema import AccessLevelDTO


class UserAccessLevelRelDTO(UserDTO):
    access_level: 'AccessLevelDTO'


class AccessLevelUserRelDTO(AccessLevelDTO):
    user: list['UserDTO'] | None = None
