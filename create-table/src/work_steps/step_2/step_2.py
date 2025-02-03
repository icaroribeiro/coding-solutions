import uuid

import zeep

from work_steps.step_1.obj_1 import Obj_1
from work_steps.step_2.obj_2 import Obj_2


def run(
    client: zeep.Client, auth_header: dict[str, str], list_of_obj_1s: list[Obj_1]
) -> list[Obj_2]:
    list_of_obj_2s = []

    set_size = 3
    for x in range(0, len(list_of_obj_1s), set_size):
        sublist_of_obj_1s = list_of_obj_1s[x : x + set_size]

        sublist_of_obj_1s_enrollments = [
            obj_1.enrollment for obj_1 in sublist_of_obj_1s
        ]
        # print(f"sublist_of_obj_1s_enrollments: {sublist_of_obj_1s_enrollments}")

        # sublist_of_obj_1s_company_codes = [
        #     obj_1.company_code for obj_1 in sublist_of_obj_1s
        # ]
        # print(f"sublist_of_obj_1s_company_codes: {sublist_of_obj_1s_company_codes}")

        # Perform the request and loop through data.

        for _ in range(len(sublist_of_obj_1s_enrollments)):
            list_of_obj_2s.append(Obj_2(person_id=str(uuid.uuid4())))

    return list_of_obj_2s
