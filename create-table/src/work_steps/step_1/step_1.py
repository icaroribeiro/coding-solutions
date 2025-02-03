import uuid

import zeep

from work_steps.step_1.obj_1 import Obj_1


def run(client: zeep.Client, auth_header: dict[str, str]) -> list[Obj_1]:
    list_of_obj1_s = []

    # Perform the first request and get data.

    for _ in range(5):
        list_of_obj1_s.append(
            Obj_1(enrollment=str(uuid.uuid4()), company_code=str(uuid.uuid4()))
        )

    # Perform the remaining requests and loop through data.

    total_of_pages = 3
    for current_page in range(1, total_of_pages):
        current_page = current_page + 1

        for _ in range(5):
            list_of_obj1_s.append(
                Obj_1(enrollment=str(uuid.uuid4()), company_code=str(uuid.uuid4()))
            )

    return list_of_obj1_s
