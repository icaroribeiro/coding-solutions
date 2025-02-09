import polars as pl


def func_1():
    df = pl.DataFrame({"a": [0, 1, 0, 2]})
    print(df)


if __name__ == "__main__":
    func_1()
