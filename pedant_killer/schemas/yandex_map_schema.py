from typing import Any
from re import sub

from pydantic import BaseModel, field_validator


class YandexMapGeo(BaseModel):
    lat: float
    lon: float


class YandexMapAddress(BaseModel):
    address: str

    @field_validator('address')
    def standardize_address(cls, address: Any) -> str:
        address = sub(r'\s+', ' ', address.strip())
        return address
