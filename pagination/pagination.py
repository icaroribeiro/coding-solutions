from typing import Annotated, Generic, TypeVar

from fastapi import Query
from pydantic import BaseModel

from schemas.person_schema import PersonQueryParams, PersonResponse

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

def get_people(
        person_query_params: Annotated[PersonQueryParams, Query()],
        ...
)
...
pagination = Pagination.create(
    page=1,
    ...
    items=[PersonResponse.model_validate(obj=item.model_dump()) for item in list[PersonModel]]
)

# model
class PersonModel(BaseModel):
    name: str | None = None