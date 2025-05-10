import aiohttp
import logging

yandex_api_logger = logging.getLogger('yandex_api_logger')


class YandexMapApi:
    def __init__(self, yandex_api_key: str, session: aiohttp.ClientSession) -> None:
        self.api_key = yandex_api_key
        self.session = session
        self.url = "https://geocode-maps.yandex.ru/1.x"

    async def get_address_by_coords(self, lat: float, lon: float) -> str | None:
        params = {
            "apikey": self.api_key,
            "geocode": f"{lon},{lat}",
            "format": "json",
            "lang": "ru_RU",
            "kind": "house"
        }

        async with self.session.get(self.url, params=params) as response:
            if response.status != 200:
                return None
            data = await response.json()
            try:
                return (
                    data["response"]["GeoObjectCollection"]["featureMember"][0]
                    ["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["text"]
                )
            except (KeyError, IndexError):
                return None

    async def validate_address(self, address: str) -> bool:
        params = {
            "apikey": self.api_key,
            "format": "json",
            "geocode": address,
        }

        async with self.session.get(self.url, params=params) as response:
            if response.status != 200:
                return False
            data = await response.json()
            try:
                collection = data["response"]["GeoObjectCollection"]
                found = int(collection["metaDataProperty"]["GeocoderResponseMetaData"]["found"])
                if found == 0:
                    return False

                geo_object = collection["featureMember"][0]["GeoObject"]
                kind = geo_object["metaDataProperty"]["GeocoderMetaData"].get("kind", "")
                precision = geo_object["metaDataProperty"]["GeocoderMetaData"].get("precision", "")

                return kind in {"house", "street", "locality"} and precision in {"exact", "number", "near"}
            except (KeyError, ValueError, IndexError):
                return False
