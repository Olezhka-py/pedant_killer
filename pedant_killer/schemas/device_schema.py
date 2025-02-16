from pydantic import Field

from pedant_killer.schemas.common_schema import CoreModel, BaseIdDTO, optional
from pedant_killer.schemas.manufacturer_device_type_schema import ManufacturerDeviceTypeRelDTO


class DevicePostDTO(CoreModel):
    manufacturer_device_type_id: int = Field(ge=1)
    name_model: str


class DeviceDTO(BaseIdDTO, DevicePostDTO):
    pass


@optional()
class DevicePartialDTO(DeviceDTO):
    pass


class DeviceManufacturerDeviceTypeRelDTO(DeviceDTO):
    manufacturer_device_type: ManufacturerDeviceTypeRelDTO | None
