from pedant_killer.schemas.order_schema import OrderDTO
from pedant_killer.schemas.user_schema import UserDTO


class OrderMasterRelDTO(OrderDTO):
    user_master: 'UserDTO | None' = None


class OrderClientRelDTO(OrderDTO):
    user_client: 'UserDTO'


class UserOrdersClientRelDTO(UserDTO):
    orders_client: list['OrderDTO'] | None = None


class UserOrdersMasterRelDTO(UserDTO):
    orders_master: list['OrderDTO'] | None = None
