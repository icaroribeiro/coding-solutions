from typing import List
from pydantic import BaseModel, Field
import datetime
from enum import Enum
from typing import Generic, TypeVar

T = TypeVar("T")


class HealthCheckResponseModel(BaseModel):
    healthy: bool


class RoleEnumModel(str, Enum):
    admin = "admin"
    user = "user"


class UserRequestModel(BaseModel):
    role: RoleEnumModel = Field(default=RoleEnumModel.user)


class UserModel(BaseModel):
    id: str | None = None
    role: RoleEnumModel
    created_time: datetime.datetime | None = None
    updated_time: datetime.datetime | None = None


class UserResponseModel(BaseModel):
    id: str
    role: RoleEnumModel = Field(default=RoleEnumModel.user)
    created_time: datetime.datetime
    updated_time: datetime.datetime | None


class FieldEnumModel(str, Enum):
    pessoa_id = "pessoa_id"
    salario_vl = "salario_vl"


class PermissionLevelEnumModel(str, Enum):
    can_read = "can_read"
    can_write = "can_write"


class AccessControlListItemModel(BaseModel):
    field: FieldEnumModel
    all_permissions: List[PermissionLevelEnumModel]


class UserPermissionsRequestModel(BaseModel):
    access_control_list: List[AccessControlListItemModel]


class UserPermissionsModel(BaseModel):
    id: str | None = None
    user_id: str
    access_control_list: List[AccessControlListItemModel]
    created_time: datetime.datetime | None = None
    updated_time: datetime.datetime | None = None


class UserPermissionsResponseModel(BaseModel):
    id: str
    user_id: str
    access_control_list: List[AccessControlListItemModel]
    created_time: datetime.datetime
    updated_time: datetime.datetime | None


class EmployeeModel(BaseModel):
    person_id: str
    salary_value: float
    reference_date: datetime.datetime


class EmployeeResponseModel(BaseModel):
    person_id: str = Field(..., alias="pessoa_id")
    salary_value: float = Field(..., alias="salario_vl")
    reference_date: datetime.datetime = Field(..., alias="referencia_dt")


class APIPaginationResponse(BaseModel, Generic[T]):
    page: int
    limit: int
    total_pages: int
    total_records: int
    records: list[T]
    previous: str | None = None
    next: str | None = None
