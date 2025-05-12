from typing import Optional, Callable, Any
from copy import deepcopy

from pydantic import BaseModel, create_model, Field


class CoreModel(BaseModel):
    pass


class BaseIdDTO(CoreModel):
    id: int = Field(ge=1)


def optional(without_fields: list[str] | None = None) -> Callable[[type[type[BaseModel]]], type[type[BaseModel]]]:

    if without_fields is None:
        without_fields = []

    def wrapper(model) -> type[type[BaseModel]]:
        base_model = model

        def make_field_optional(
            field, default=None
        ) -> tuple[Any, Field]:

            new = deepcopy(field)
            new.default = default
            new.annotation = Optional[field.annotation]
            return new.annotation, new

        if without_fields:
            base_model = BaseModel

        return create_model(
            model.__name__,
            __base__=base_model,
            __module__=model.__module__,
            **{
                field_name: make_field_optional(field_info)
                for field_name, field_info in model.model_fields.items()
                if field_name not in without_fields
            },
        )

    return wrapper
