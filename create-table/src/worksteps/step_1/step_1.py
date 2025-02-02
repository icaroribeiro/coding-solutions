import polars as pl
import uuid


def run() -> None:
    current_page = 1
    total_of_pages = 3
    rows_by_column = {"enrollment": [], "company_code": []}
    for _ in range(5):
        rows_by_column["enrollment"].append(str(uuid.uuid4()))
        rows_by_column["company_code"].append(str(uuid.uuid4()))
    output_path = f"./output/worksteps/step_1/partial_result_{current_page}.csv"
    df = pl.DataFrame(rows_by_column)
    df.write_csv(output_path, separator=",")

    for current_page in range(1, total_of_pages):
        current_page = current_page + 1
        rows_by_column = {"enrollment": [], "company_code": []}
        for _ in range(5):
            rows_by_column["enrollment"].append(str(uuid.uuid4()))
            rows_by_column["company_code"].append(str(uuid.uuid4()))
        output_path = f"./output/worksteps/step_1/partial_result_{current_page}.csv"
        df = pl.DataFrame(rows_by_column)
        df.write_csv(output_path, separator=",")
