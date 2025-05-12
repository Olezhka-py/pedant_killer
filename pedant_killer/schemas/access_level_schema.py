from pedant_killer.schemas.common_schema import CoreModel, BaseIdDTO, optional


class AccessLevelPostDTO(CoreModel):
    name: str
    importance: int


class AccessLevelDTO(BaseIdDTO, AccessLevelPostDTO):
    pass


@optional()
class AccessLevelPartialDTO(AccessLevelDTO):
    pass
