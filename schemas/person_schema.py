from fastapi import Query
from pydantic import BaseModel, Field
from pagination.pagination_schema import PaginationQueryParams


class PersonQueryParams(PaginationQueryParams):
    email: str | None = Query(
        default=None,
        description="The person's email to filter items",
        example="icaroribeiro@hotmail.com",
    )
    query_fields = str | None - Query(
        default=None,
        description="The query fields separated by commas as a string",
        example="name,email,age",
    )


class PersonResponse(BaseModel):
    name: str | None = Field(
        default=None,
        serialization_alias="nome",
        description="It's an optional field that is not necessary to return in the response body",
    )
