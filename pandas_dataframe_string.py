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

    df_dtypes1 = df.dtypes.apply(lambda x: x.name).to_dict()
    df_dict1 = df.to_dict(orient="records")
    df_str1 = json.dumps({"data": df_dict1, "dtypes": df_dtypes1})
    print("パターン1")
    print("json.dumpsの文字列:")
    print(df_str1)
    print(f"サイズ: {sys.getsizeof(df_str1)} Bytes")
    print()

    df_load1 = json.loads(df_str1)
    df_dtypes1 = {k: v for k, v in df_load1["dtypes"].items()}
    df_restore1 = pd.DataFrame(df_load1["data"]).astype(df_dtypes1)
    print("復元されたDataFrame:")
    print(df_restore1)
    print(df_restore1.dtypes)
    print(df_restore1.index)
    print()
    assert_frame_equal(df, df_restore1)

    df_dtypes2 = df.dtypes.apply(lambda x: x.name).to_dict()
    df_dict2 = df.to_dict(orient="list")
    df_str2 = json.dumps({"data": df_dict2, "dtypes": df_dtypes2})
    print("パターン2")
    print("json.dumpsの文字列:")
    print(df_str2)
    print(f"サイズ: {sys.getsizeof(df_str2)} Bytes")
    print()

    df_load2 = json.loads(df_str2)
    df_dtypes2 = {k: v for k, v in df_load2["dtypes"].items()}
    df_restore2 = pd.DataFrame.from_dict(df_load2["data"]).astype(df_dtypes2)
    print("復元されたDataFrame:")
    print(df_restore2)
    print(df_restore2.dtypes)
    print(df_restore2.index)
    print()
    assert_frame_equal(df, df_restore2)

    df_dtypes3 = df.dtypes.apply(lambda x: x.name).to_dict()
    df_dict3 = df.to_dict(orient="split")
    df_str3 = json.dumps({"data": df_dict3, "dtypes": df_dtypes3})
    print("パターン3")
    print("json.dumpsの文字列:")
    print(df_str3)
    print(f"サイズ: {sys.getsizeof(df_str3)} Bytes")
    print()

    df_load3 = json.loads(df_str3)
    df_dtypes3 = {k: v for k, v in df_load3["dtypes"].items()}
    df_restore3 = pd.DataFrame(
        df_load3["data"]["data"], columns=df_load3["data"]["columns"]
    ).astype(df_dtypes3)
    print("復元されたDataFrame:")
    print(df_restore3)
    print(df_restore3.dtypes)
    print(df_restore3.index)
    print()
    assert_frame_equal(df, df_restore3)

    print("パターン4")
    # DataFrameをCSV形式の文字列に変換
    csv_string = df.to_csv(index=False)
    df_dtypes4 = df.dtypes.apply(lambda x: x.name).to_dict()
    str_data = json.dumps({"data": csv_string, "dtypes": df_dtypes4})
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
