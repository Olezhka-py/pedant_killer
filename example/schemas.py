import pydantic


# здесь нет связанных объектов, поэтому модель можно не разделять на две
# (данные при создании и чтении объекта будут в одинаковом формате)
class ManufacturerDTO(pydantic.BaseModel):
    id: int
    name: str
    description: str | None = None


class DeviceTypeDTO(pydantic.BaseModel):
    id: int
    name: str
    description: str | None = None


# Идея в том, что при создании или обновлении объекта указывается только id связанных объектов
# а при чтении возвращается связанный объект целиком
class CreateManufacturerDeviceTypeDTO(pydantic.BaseModel):
    id: int
    manufacturer_id: int
    device_type_id: int


class ReadManufacturerDeviceTypeDTO(pydantic.BaseModel):
    id: int
    manufacturer: ManufacturerDTO
    device_type: DeviceTypeDTO


class CreateDeviceDTO(pydantic.BaseModel):
    manufacturer_device_type_id: int
    model_name: str


# здесь модели одинаковые, но в других случая создание и изменение могут иметь разные поля
class UpdateDeviceDTO(CreateDeviceDTO):
    pass


class ReadDeviceDTO(pydantic.BaseModel):
    id: int
    manufacturer_device_type: ReadManufacturerDeviceTypeDTO
    model_name: str
