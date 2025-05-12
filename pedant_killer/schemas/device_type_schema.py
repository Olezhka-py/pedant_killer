from pedant_killer.schemas.common_schema import CoreModel, BaseIdDTO, optional


class DeviceTypePostDTO(CoreModel):
    name: str
    description: str | None = None


class DeviceTypeDTO(BaseIdDTO, DeviceTypePostDTO):
    pass


@optional()
class DeviceTypePartialDTO(DeviceTypeDTO):
    pass
