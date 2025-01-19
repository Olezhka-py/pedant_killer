from dependency_injector import containers, providers

from example import database
from example import device_repository as device_repository_module
from example import device_use_case as device_use_case_module


class Container(containers.DeclarativeContainer):
    # указываем пути до модулей, в которых нужно будет выполнять инъекцию зависимостей
    wiring_config = containers.WiringConfiguration(
        modules=[
            "example.main",
        ],
    )
    # объект для удобной работы с конфигом приложения
    config = providers.Configuration()

    # создаем синглитон менеджер подключений к базе данных
    db = providers.Singleton(database.Database, db_url=config.db.url)

    # собираем наши объекты для последующего внедрения с хендлеры
    device_repository = providers.Factory(
        device_repository_module.DeviceRepository,
        session=db.provided.session,
    )

    # подставляем в юз кейс (сервис) собранный объект репозитория
    device_use_case = providers.Factory(
        device_use_case_module.DeviceUseCase,
        device_repository=device_repository,
    )
