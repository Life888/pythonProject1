import pandas as pd
import numpy as np


def read_data():

    file_name_contains = ['a', 'b', 'e', 'f', 'h']
    for fn in file_name_contains:
        file_path = "data/"
        file_name = fn + "_lvr_land_a.csv"
        df_temp = pd.read_csv(file_path + file_name)

        if file_name.index(fn) == 0:
            df_all = pd.DataFrame(columns=df_temp.columns)

        df_all = df_all.append(df_temp.iloc[1:, :], ignore_index=True)

    # df_all.to_csv("output/df_all.csv", index=False, encoding="utf-8-sig")

    return df_all


def filter_a(df_all_data):

    # 主要用途: 住家用
    column_name = "主要用途"
    value = "住家用"
    df_all_data = df_all_data[(df_all_data[column_name] == value)]

    # 建物型態: 住宅大樓
    column_name = "建物型態"
    contains_value = "住宅大樓"
    df_all_data = df_all_data[df_all_data[column_name].str.contains(contains_value)]

    # 總樓層數: 大於等於十三層
    column_name = "總樓層數"
    df_all_data = df_all_data[(df_all_data[column_name].apply(len) > 2)]
    exclude_value = ["十一層", "十二層"]
    for v in exclude_value:
        df_all_data = df_all_data[df_all_data[column_name] != v]

    df_all_data.to_csv("output/filter_a.csv", index=False, encoding="utf-8-sig")


def filter_b(df_all_data):

    columns_name = ["總件數", "總車位數", "平均總價元", "平均車位總價元"]
    # df_filter_b = pd.DataFrame(columns=columns_name)
    add_df_data = {}
    for cn in columns_name:

        value = 0
        if cn == "總件數":
            value = df_all_data.shape[0]

        elif cn == "總車位數":
            for item in df_all_data["交易筆棟數"]:
                value = value + int(item[item.index('車')+2:])

        elif cn == "平均總價元":
            value = np.asarray(df_all_data["總價元"], dtype=int).mean()

        elif cn == "平均車位總價元":
            value = np.asarray(df_all_data["車位總價元"], dtype=int).mean()

        add_df_data[cn] = value
        df_filter_b = pd.DataFrame(add_df_data, index=[0])

    df_filter_b.to_csv("output/filter_b.csv", index=False, encoding="utf-8-sig")


if __name__ == '__main__':

    all_data = read_data()

    filter_a(all_data)

    filter_b(all_data)

