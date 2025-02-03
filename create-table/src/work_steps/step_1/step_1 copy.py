import logging
import threading
import uuid

import zeep

from work_steps.step_1.obj_1 import Obj_1

logging.basicConfig(
    format="%(asctime)s: %(message)s", datefmt="%Y-%m-%d %H:%M", level=logging.INFO
)


def thread_function(
    index: int, list_of_obj_1s: list[Obj_1], lock: threading.Lock
) -> None:
    index = index + 1
    for _ in range(5):
        with lock:
            list_of_obj_1s.append(
                Obj_1(enrollment=str(uuid.uuid4()), company_code=str(uuid.uuid4()))
            )


def run(client: zeep.Client, auth_header: dict[str, str]) -> list[Obj_1]:
    list_of_obj_1s = list()

    # Perform the first request and get data.

    for _ in range(5):
        list_of_obj_1s.append(
            Obj_1(enrollment=str(uuid.uuid4()), company_code=str(uuid.uuid4()))
        )

    # Perform the remaining requests and loop through data.

    threads = list()
    lock = threading.Lock()
    total_of_pages = 3
    for index in range(1, total_of_pages):
        x = threading.Thread(target=thread_function, args=(index, list_of_obj_1s, lock))
        # logging.info(f"Thread {index} created and started")
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        # logging.info(f"Before joining thread {index + 1}")
        thread.join()
        # logging.info(f"Thread {index + 1} done")

    return list_of_obj_1s


# def run(client: zeep.Client, auth_header: dict[str, str]) -> list[Obj_1]:
#     list_of_obj1_s = []

#     # Perform the first request and get data.

#     for _ in range(5):
#         list_of_obj1_s.append(
#             Obj_1(enrollment=str(uuid.uuid4()), company_code=str(uuid.uuid4()))
#         )

#     # Perform the remaining requests and loop through data.

#     total_of_pages = 3
#     for current_page in range(1, total_of_pages):
#         current_page = current_page + 1

#         for _ in range(5):
#             list_of_obj1_s.append(
#                 Obj_1(enrollment=str(uuid.uuid4()), company_code=str(uuid.uuid4()))
#             )

#     return list_of_obj1_s
