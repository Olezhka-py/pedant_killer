from pedant_killer.schemas.device_service_schema import DeviceServiceDTO
from pedant_killer.schemas.order_schema import OrderDTO
from pedant_killer.schemas.user_schema import UserDTO


class DeviceServiceOrderRelDTO(DeviceServiceDTO):
    order: list['OrderDTO'] | None = None


class OrderDeviceServiceRelDTO(OrderDTO):
    device_service: list['DeviceServiceDTO'] | None = None


class UserOrdersClientRelDTO(UserDTO):
    orders_client: list['OrderDTO'] | None = None


class UserOrdersMasterRelDTO(UserDTO):
    orders_master: list['OrderDTO'] | None = None
