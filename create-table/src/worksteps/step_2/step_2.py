import os
import polars as pl
import uuid


def run() -> None:
    rows = []
    step_1_files = os.listdir("./output/worksteps/step_1")
    for file in step_1_files:
        if file.endswith(".csv"):
            df = pl.read_csv(f"./output/worksteps/step_1/{file}")
            for row in df.iter_rows(named=True):
                rows.append(
                    {
                        "enrollment": row["enrollment"],
                        "company_code": row["company_code"],
                    }
                )

    count = 1
    set_size = 3
    for x in range(0, len(rows), set_size):
        set_of_rows = rows[x : x + set_size]
        set_of_enrollments = [row["enrollment"] for row in set_of_rows]
        print(f"set_of_enrollments: {set_of_enrollments}")
        set_of_company_codes = [row["company_code"] for row in set_of_rows]
        print(f"set_of_company_codes: {set_of_company_codes}")

        # Perform request with set of enrollments.

        set_of_person_ids = [str(uuid.uuid4()) for _ in range(len(set_of_rows))]
        rows_by_column = {"person_id": []}
        for person_id in set_of_person_ids:
            rows_by_column["person_id"].append(person_id)
        df = pl.DataFrame(rows_by_column)
        df.write_csv(
            f"./output/worksteps/step_2/partial_result_{count}.csv", separator=","
        )
        count = count + 1
