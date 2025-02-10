import polars as pl


def run() -> None:
    df = pl.DataFrame({"a": [3, 4]})
    print(df)
    return None
