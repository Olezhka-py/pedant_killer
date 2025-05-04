from pedant_killer.schemas.common_schema import CoreModel, BaseIdDTO, optional


class BreakingPostDTO(CoreModel):
    name: str
    description: str | None = None


class BreakingDTO(BaseIdDTO, BreakingPostDTO):
    pass


@optional()
class BreakingPartialDTO(BreakingDTO):
    pass
