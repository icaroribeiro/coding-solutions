import polars as pl
import os


def run() -> None:
    rows_by_column = {"new_person_id": []}
    step_2_files = os.listdir("./output/worksteps/step_2")
    for file in step_2_files:
        if file.endswith(".csv"):
            df = pl.read_csv(f"./output/worksteps/step_2/{file}")
            for row in df.iter_rows(named=True):
                rows_by_column["new_person_id"].append(row["person_id"])

    path = "./output/worksteps/step_3/result.csv"
    df = pl.DataFrame(rows_by_column)
    df.write_csv(path, separator=",")
