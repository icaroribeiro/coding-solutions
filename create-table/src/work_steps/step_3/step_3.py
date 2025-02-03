import polars as pl

from work_steps.step_2.obj_2 import Obj_2


def run(list_of_obj_2s: list[Obj_2]) -> None:
    rows_by_column = {"new_person_id": []}

    for obj_2 in list_of_obj_2s:
        rows_by_column["new_person_id"].append(obj_2.person_id)

    df = pl.DataFrame(rows_by_column)
    df.write_csv("./output/resul.csv", separator=",")
