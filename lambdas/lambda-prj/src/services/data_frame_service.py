import logging

import polars as pl
from botocore.response import StreamingBody

logger = logging.getLogger()


class DataFrameService:
    def load_data_frame(self, body: StreamingBody, region: str) -> pl.DataFrame:
        try:
            return pl.read_parquet(source=body, storage_options={"region": region})
        except Exception as err:
            print(err)
            raise

    def format_data_frame(self, x: str, data_frame: pl.DataFrame) -> pl.DataFrame:
        try:
            case_function = self.__format_switcher.get(x, self.__default_format)
            return case_function(data_frame)
        except Exception as err:
            print(err)
            raise

    def __default_format(data_frame: pl.DataFrame) -> pl.DataFrame:
        return data_frame

    def __first_format(data_frame: pl.DataFrame) -> pl.DataFrame:
        columns_to_remove = ["X"]
        data_frame = data_frame.drop(columns_to_remove)

        for col_name, col_type in data_frame.schema.items():
            if col_type == pl.Decimal:
                data_frame = data_frame.with_columns(pl.col(col_name).cast(pl.Int64))
            elif col_type == pl.Datetime:
                data_frame = data_frame.with_columns(
                    pl.col(col_name).dt.timestamp() // 10**3
                )

        return data_frame

    __format_switcher = {
        "A": __first_format,
    }
