from typing import Annotated, List
from uuid import uuid4
import pytz
import datetime
from fastapi import APIRouter, Path, Query
from fastapi import Response, status
from models import (
    APIPaginationResponse,
    EmployeeModel,
    FieldEnumModel,
    HealthCheckResponseModel,
    UserPermissionsRequestModel,
    UserPermissionsResponseModel,
    UserRequestModel,
    UserResponseModel,
)


class HealthCheckController(APIRouter):
    def __init__(
        self,
        prefix="/health",
        dependencies=[],
    ):
        super().__init__(prefix=prefix, dependencies=dependencies)
        self.setup_routes()

    def setup_routes(self):
        @APIRouter.api_route(
            self,
            path="",
            methods=["GET"],
            tags=["health-check"],
            summary="""
             Checks if service is healthy.
            """,
            description="""
             It's used to check if service has started up correctly and 
             is ready to accept requests.
            """,
            status_code=status.HTTP_200_OK,
        )
        async def get_health(
            response: Response,
        ) -> HealthCheckResponseModel:
            response.status_code = status.HTTP_200_OK
            health_check_response = HealthCheckResponseModel(healthy=True)
            return health_check_response


class UserController(APIRouter):
    def __init__(
        self,
        prefix="/users",
        dependencies=[],
    ):
        super().__init__(prefix=prefix, dependencies=dependencies)
        self.setup_routes()

    def setup_routes(self):
        @APIRouter.api_route(
            self,
            path="",
            methods=["POST"],
            tags=["users"],
            summary="""
             Creates a new user.
            """,
            description="""
             It's used to create a new user.
            """,
            status_code=status.HTTP_201_CREATED,
        )
        async def create_user(
            response: Response,
            user_request: UserRequestModel,
            admin_id: Annotated[
                str,
                Query(description="The id of the Admin user."),
            ],
        ) -> UserResponseModel:
            user_response = UserResponseModel(
                id=str(uuid4()),
                role=user_request.role,
                created_time=datetime.datetime.now(
                    tz=pytz.timezone("America/Sao_Paulo")
                ),
                updated_time=None,
            )
            response.status_code = status.HTTP_201_CREATED
            return user_response


class UserPermissionsController(APIRouter):
    def __init__(
        self,
        prefix="/permissions",
        dependencies=[],
    ):
        super().__init__(prefix=prefix, dependencies=dependencies)
        self.setup_routes()

    def setup_routes(self):
        @APIRouter.api_route(
            self,
            path="/users/{user_id}",
            methods=["PUT"],
            tags=["permissions"],
            summary="""
             Sets user permissions.
            """,
            description="""
             It's used to set user permissions, replacing existing permissions if they exist.
            """,
            status_code=status.HTTP_200_OK,
        )
        async def set_user_permissions(
            response: Response,
            user_id: Annotated[
                str,
                Path(description="The id of the User."),
            ],
            user_permissions_request: UserPermissionsRequestModel,
            admin_id: Annotated[
                str,
                Query(description="The id of the Admin user."),
            ],
        ) -> UserPermissionsResponseModel:
            user_permissions_response = UserPermissionsResponseModel(
                id=str(uuid4()),
                user_id=user_id,
                access_control_list=user_permissions_request.access_control_list,
                created_time=datetime.datetime.now(
                    tz=pytz.timezone("America/Sao_Paulo")
                ),
                updated_time=datetime.datetime.now(
                    tz=pytz.timezone("America/Sao_Paulo")
                ),
            )
            response.status_code = status.HTTP_200_OK
            return user_permissions_response


class EmployeeController(APIRouter):
    def __init__(
        self,
        prefix="/employees",
        dependencies=[],
    ):
        super().__init__(prefix=prefix, dependencies=dependencies)
        self.setup_routes()

    def setup_routes(self):
        @APIRouter.api_route(
            self,
            path="",
            methods=["GET"],
            tags=["employees"],
            summary="""
             Fetch paginated employees.
            """,
            description="""
             It's used to fetch paginated employees.
            """,
            status_code=status.HTTP_200_OK,
        )
        async def fetch_paginated_employees(
            response: Response,
            user_id: Annotated[
                str,
                Query(description="The id of the User."),
            ],
            fields: Annotated[
                List[FieldEnumModel],
                Query(description="The list of selected fields."),
            ] = None,
            page: Annotated[
                int,
                Query(
                    description="The number of the page. If isn't provided, it will be set to 1.",
                    ge=1,
                ),
            ] = 1,
            limit: Annotated[
                int,
                Query(
                    description="The number of records per page. If isn't provided, it will be set to 50.",
                    le=50,
                ),
            ] = 50,
        ) -> APIPaginationResponse:
            employee_model = EmployeeModel(
                person_id=str(uuid4()),
                salary_value=10.0,
                reference_date=datetime.datetime.now(
                    tz=pytz.timezone("America/Sao_Paulo")
                ),
            )
            api_pagination_response = APIPaginationResponse(
                page=page,
                limit=limit,
                total_pages=1,
                total_records=1,
                records=[employee_model],
                previous=None,
                next=None,
            )
            response.status_code = status.HTTP_200_OK
            return api_pagination_response
