from __future__ import annotations

from pedant_killer.gateway.api_yandex_map import YandexMapApi
from pedant_killer.schemas.yandex_map_schema import YandexMapGeo, YandexMapAddress


class YandexMapService:
    def __init__(self, yandex_map_api: YandexMapApi) -> None:
        self.yandex_map_api = yandex_map_api

    async def get_address_by_coords(self, model_dto: YandexMapGeo) -> list[YandexMapAddress] | None:
        address = await self.yandex_map_api.get_address_by_coords(lat=model_dto.lat, lon=model_dto.lon)

        if address:
            return [YandexMapAddress(address=address)]

        return None

    async def validate_address(self, model_dto: YandexMapAddress) -> bool | None:
        result = await self.yandex_map_api.validate_address(address=model_dto.address)

        if result:

            return result

        return None
