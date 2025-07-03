import math
import re
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginationResponse(BaseModel, Generic[T]):
    page: int
    limit: int
    total_pages: int
    total_records: int
    records: list[T]
    previous: str | None = None
    next: str | None = None


class PaginationConfig(BaseModel):
    page: int
    limit: int
    total_records: int
    records: list[T]


def create_pagination_response(
    self, base_url: str, pagination_config: PaginationConfig
) -> PaginationResponse:
    return PaginationResponse(
        page=pagination_config.page,
        limit=pagination_config.limit,
        total_pages=self.get_total_pages(
            pagination_config.limit,
            pagination_config.total_records,
        ),
        total_records=pagination_config.total_records,
        records=pagination_config.records,
        previous=self.get_previous_page(
            base_url,
            pagination_config.page,
            pagination_config.limit,
            pagination_config.total_records,
        ),
        next=self.get_next_page(
            base_url,
            pagination_config.page,
            pagination_config.limit,
            pagination_config.total_records,
        ),
    )


def get_total_pages(limit: int, total_records: int) -> int:
    return math.ceil(total_records / limit)


def get_previous_page(
    base_url: str, page: int, limit: int, total_records: int
) -> str | None:
    if page == 1:
        return None
    if total_records - (page - 1) * limit <= 0:
        return None
    return re.sub(r"(page=)[^&]", rf"\g<1>{page - 1}", base_url)


def get_next_page(
    base_url: str, page: int, limit: int, total_records: int
) -> str | None:
    if total_records - page * limit <= 0:
        return None
    if "page" in base_url:
        return re.sub(r"(page=)[^&]", rf"\g<1>{page + 1}", base_url)
    if "limit" in base_url:
        return base_url + f"&page={page + 1}"
    return base_url + f"?page={page + 1}&limit=1"
