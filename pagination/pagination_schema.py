from fastapi import Query
from pydantic import BaseModel, field_validator


def get_settings():
    pass


class PaginationQueryParams(BaseModel):
    page: int = Query(
        default=int(get_settings().default_page_number),
        description=f"The page number that should start at {get_settings().min_page_number}",
    )
    size: int = Query(
        default=int(get_settings().default_page_size),
        description=f"The number of items per page limited to {get_settings().max_page_size}",
    )

    @field_validator("page")
    def validate_page(cls, page):
        if page <= 0:
            raise ValueError("The page query param must be greater than 0")
        return page

    @field_validator("size")
    def validate_size(cls, size):
        if size <= 0:
            raise ValueError("The size query param must be greater than 0")
        if size > int(get_settings().max_page_size):
            raise ValueError(
                f"The size query param must be less than {get_settings().max_page_size}"
            )
        return size
