from typing import Generic, TypeVar

from pydantic import BaseModel

Model = TypeVar("Model", bound=BaseModel)


class Pagination(BaseModel, Generic[Model]):
    page: int
    size: int
    total_pages: int
    total: int
    items: list[Model]

    @classmethod
    def create(
        cls, page: int, size: int, total: int, items: list[Model]
    ) -> "Pagination":
        return cls(
            page=page,
            size=size,
            total_pages=(total + size - 1) // size,
            total=total,
            items=items,
        )
