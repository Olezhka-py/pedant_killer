from pedant_killer.database.database import Base


class Specification:
    def is_satisfied(self, *args, **kwargs):
        raise NotImplementedError

    def __and__(self):
        pass

    def __or__(self):
        pass

    def __eq__(self, other: "Specification"):
        pass


class ObjectExistsByIdSpecification(Specification):
    # @classmethod
    # async def is_satisfied(cls, repository, model: Base, instance_id: int) -> dict:
    #     instance = await repository.get_without_checks(model, instance_id)
    #     if instance:
    #         return {'id': instance_id}

    #     return {'id': -1}

    def is_satisfied(self, instance_id: int) -> dict[str, int]:
        return {"id": instance_id}
