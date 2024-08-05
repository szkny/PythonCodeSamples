import json
import pandas as pd
from pandas.testing import assert_frame_equal
from io import StringIO
import sys

if __name__ == "__main__":
    # サンプルデータフレームを作成
    data = {
        "name": ["Alice", "Bob", "Charlie"],
        "age": [25, 30, 35],
        "city": ["New York", "Los Angeles", "Chicago"],
        "time": [1.2, 2.3, 4.5],
        "flag": [True, False, True],
    }
    df = pd.DataFrame(data)
    df2 = pd.DataFrame(
        {
            "name": ["Alice", "Bob", "Charlie"],
            "age": [25, 30, 35],
            "city": ["New York", "Los Angeles", "Chicago"],
            "time": [1.2, 2.3, "4.5"],
            "flag": ["True", "False", "True"],
        }
    )
    print("元のDataFrame:")
    print(df)
    print()

    df_dtypes = df.dtypes.apply(lambda x: x.name).to_dict()
    df_dict = df.to_dict(orient="records")
    df_str = json.dumps({"data": df_dict, "dtypes": df_dtypes})
    print("パターン1")
    print("json.dumpsの文字列:")
    print(df_str)
    print(f"サイズ: {sys.getsizeof(df_str)} Bytes")
    print()

    df_load = json.loads(df_str)
    df_dtypes = {k: v for k, v in df_load["dtypes"].items()}
    df_restore1 = pd.DataFrame(df_load["data"]).astype(df_dtypes)
    print("復元されたDataFrame:")
    print(df_restore1)
    print(df_restore1.dtypes)
    print(df_restore1.index)
    print()
    assert_frame_equal(df, df_restore1)

    df_dtypes = df.dtypes.apply(lambda x: x.name).to_dict()
    df_dict = df.to_dict(orient="list")
    df_str = json.dumps({"data": df_dict, "dtypes": df_dtypes})
    print("パターン2")
    print("json.dumpsの文字列:")
    print(df_str)
    print(f"サイズ: {sys.getsizeof(df_str)} Bytes")
    print()

    df_load = json.loads(df_str)
    df_dtypes = {k: v for k, v in df_load["dtypes"].items()}
    df_restore2 = pd.DataFrame.from_dict(df_load["data"]).astype(df_dtypes)
    print("復元されたDataFrame:")
    print(df_restore2)
    print(df_restore2.dtypes)
    print(df_restore2.index)
    print()
    assert_frame_equal(df, df_restore2)

    df_dtypes = df.dtypes.apply(lambda x: x.name).to_dict()
    df_dict = df.to_dict(orient="split")
    df_str = json.dumps({"data": df_dict, "dtypes": df_dtypes})
    print("パターン3")
    print("json.dumpsの文字列:")
    print(df_str)
    print(f"サイズ: {sys.getsizeof(df_str)} Bytes")
    print()

    df_load = json.loads(df_str)
    df_dtypes = {k: v for k, v in df_load["dtypes"].items()}
    df_restore3 = pd.DataFrame(
        df_load["data"]["data"], columns=df_load["data"]["columns"]
    ).astype(df_dtypes)
    print("復元されたDataFrame:")
    print(df_restore3)
    print(df_restore3.dtypes)
    print(df_restore3.index)
    print()
    assert_frame_equal(df, df_restore3)

    print("パターン4")
    # DataFrameをCSV形式の文字列に変換
    csv_string = df.to_csv(index=False)
    df_dtypes = df.dtypes.apply(lambda x: x.name).to_dict()
    str_data = json.dumps({"data": csv_string, "dtypes": df_dtypes})
    print("CSV形式の文字列:")
    print(str_data)
    print(f"サイズ: {sys.getsizeof(str_data)} Bytes")
    print()

    # 文字列からDataFrameを復元
    dict_data = json.loads(str_data)
    csv_string_io = StringIO(dict_data["data"])
    df_restore4 = pd.read_csv(csv_string_io).astype(dict_data["dtypes"])
    print("復元されたDataFrame:")
    print(df_restore4)
    print(df_restore4.dtypes)
    print(df_restore4.index)
    assert_frame_equal(df, df_restore4)
