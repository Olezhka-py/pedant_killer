from pedant_killer.database.database import Base
from typing import Any, Coroutine, TYPE_CHECKING

if TYPE_CHECKING:
    from pedant_killer.database.repository.core_repository import CoreRepository


class Specification:
    @classmethod
    def is_satisfied(cls, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, dict[str, int]]:
        raise NotImplementedError

    # def __and__(self):
    #     pass
    #
    # def __or__(self):
    #     pass
    #
    # def __eq__(self, other):
    #     pass


class ObjectExistsByIdSpecification(Specification):
    @classmethod
    async def is_satisfied(cls, repository: Any, model: Base, instance_id: int) -> dict[str, int]:
        instance = await repository.get_without_checks(model, instance_id)
        if instance:
            return {'id': instance_id}

        return {'id': -1}


