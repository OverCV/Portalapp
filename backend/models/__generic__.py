from typing import Type, TypeVar, TypedDict


T = TypeVar('T', bound=TypedDict)


def get_typed_dict_fields(model: Type[T]) -> list[str]:
    return list(model.__annotations__.keys())
