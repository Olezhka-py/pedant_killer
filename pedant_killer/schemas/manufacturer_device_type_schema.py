from pydantic import Field

from pedant_killer.schemas.common_schema import CoreModel, BaseIdDTO, optional
from pedant_killer.schemas.manufacturer_schema import ManufacturerDTO
from pedant_killer.schemas.device_type_schema import DeviceTypeDTO


class ManufacturerDeviceTypePostDTO(CoreModel):
    manufacturer_id: int = Field(ge=1)
    device_type_id: int = Field(ge=1)


class ManufacturerDeviceTypeDTO(BaseIdDTO, ManufacturerDeviceTypePostDTO):
    manufacturer: ManufacturerDTO | None
    device_type: DeviceTypeDTO | None


@optional()
class ManufacturerDeviceTypePartialDTO(ManufacturerDeviceTypeDTO):
    pass

