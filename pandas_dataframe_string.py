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

    df_dict = df.to_dict(orient="records")
    df_str = json.dumps(df_dict)
    print("パターン1")
    print("json.dumpsの文字列:")
    print(df_str)
    print(f"サイズ: {sys.getsizeof(df_str)} Bytes")
    print()

    df_load = json.loads(df_str)
    df_restore1 = pd.DataFrame(df_load)
    print("復元されたDataFrame:")
    print(df_restore1)
    print()
    assert_frame_equal(df, df_restore1)

    print("パターン2")
    # DataFrameをCSV形式の文字列に変換
    csv_string = df.to_csv(index=False)
    print("CSV形式の文字列:")
    print(csv_string)
    print(f"サイズ: {sys.getsizeof(csv_string)} Bytes")
    print()

    # 文字列からDataFrameを復元
    csv_string_io = StringIO(csv_string)
    df_restore2 = pd.read_csv(csv_string_io)
    print("復元されたDataFrame:")
    print(df_restore2)
    assert_frame_equal(df, df_restore2)
