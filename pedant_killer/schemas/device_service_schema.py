from pydantic import Field

from pedant_killer.schemas.common_schema import CoreModel, BaseIdDTO, optional
from pedant_killer.schemas.service_schema import ServiceDTO
from pedant_killer.schemas.device_schema import DeviceManufacturerDeviceTypeRelDTO
from pedant_killer.schemas.order_schema import OrderDTO


class DeviceServicePostDTO(CoreModel):
    device_id: int = Field(ge=1)
    service_id: int = Field(ge=1)
    price: int = Field(ge=0)
    work_duration: int | None = Field(default=None, ge=1)


class DeviceServiceDTO(BaseIdDTO, DeviceServicePostDTO):
    pass


@optional()
class DeviceServicePartialDTO(DeviceServiceDTO):
    pass


class DeviceServiceDeviceRelDTO(DeviceServiceDTO):
    device: DeviceManufacturerDeviceTypeRelDTO


class DeviceServiceServiceRelDTO(DeviceServiceDTO):
    service: ServiceDTO


class DeviceServiceOrderRelDTO(DeviceServiceDTO):
    order: 'list[OrderDTO] | None' = None


class DeviceServiceRelDTO(DeviceServiceDeviceRelDTO, DeviceServiceServiceRelDTO):
    pass
