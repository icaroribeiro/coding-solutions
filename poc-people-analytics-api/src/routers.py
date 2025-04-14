from controllers import HealthCheckController
from controllers import UserController
from controllers import UserPermissionsController
from controllers import EmployeeController


health_check_router = HealthCheckController()
user_router = UserController()
permission_router = UserPermissionsController()
employee_router = EmployeeController()
