from dependency_injector import containers, providers

from pedant_killer.database.database import Database
from pedant_killer.database.repository import *
from pedant_killer.services import *
from pedant_killer import config


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(
        modules=[
        ],
    )

    config = providers.Configuration()

    db = providers.Singleton(
        Database,
        db_url=config.database_url_asyncpg
    )

    manufacturer_repository = providers.Factory(
        ManufacturerRepository,
        session_factory=db.provided.session
    )
    manufacturer_service = providers.Factory(
        ManufacturerService,
        repository=manufacturer_repository
    )

    device_type_repository = providers.Factory(
        DeviceTypeRepository,
        session_factory=db.provided.session
    )
    device_type_service = providers.Factory(
        DeviceTypeService,
        repository=device_type_repository
    )

    manufacturer_device_type_repository = providers.Factory(
        ManufacturerDeviceTypeRepository,
        session_factory=db.provided.session
    )
    manufacturer_device_type_service = providers.Factory(
        ManufacturerDeviceTypeService,
        repository=manufacturer_device_type_repository
    )

    device_repository = providers.Factory(
        DeviceRepository,
        session_factory=db.provided.session
    )
    device_service = providers.Factory(
        DeviceService,
        repository=device_repository
    )

    service_repository = providers.Factory(
        ServiceRepository,
        session_factory=db.provided.session
    )
    service_service = providers.Factory(
        ServiceService,
        repository=service_repository
    )

    device_service_repository = providers.Factory(
        DeviceServiceRepository,
        session_factory=db.provided.session
    )
    device_service_service = providers.Factory(
        DeviceServiceService,
        repository=device_service_repository
    )

    access_level_repository = providers.Factory(
        AccessLevelRepository,
        session_factory=db.provided.session
    )
    access_level_service = providers.Factory(
        AccessLevelService,
        repository=access_level_repository
    )

    user_repository = providers.Factory(
        UserRepository,
        session_factory=db.provided.session
    )
    user_service = providers.Factory(
        UserService,
        repository=user_repository
    )

    order_repository = providers.Factory(
        OrderRepository,
        session_factory=db.provided.session
    )
    order_service = providers.Factory(
        OrderService,
        repository=order_repository
    )

    order_status_repository = providers.Factory(
        OrderStatusRepository,
        session_factory=db.provided.session
    )
    order_status_service = providers.Factory(
        OrderStatusService,
        repository=order_status_repository
    )


container = Container()
container.config.from_pydantic(config.Config())
