from pydantic import Field

from pedant_killer.schemas.common_schema import CoreModel, BaseIdDTO, optional


class ManufacturerPostDTO(CoreModel):
    name: str
    description: str | None = None


class ManufacturerDTO(BaseIdDTO, ManufacturerPostDTO):
    pass


@optional()
class ManufacturerPartialDTO(ManufacturerDTO):
    pass
