import pandas as pd

result_2023_yield = pd.read_csv("data/结果/result_2023_亩产量.csv")
result_2023_lite = pd.read_csv("data/结果/result_2023_lite.csv")
result_2023_multi = pd.read_csv("data/附件3/result_temple_lite.csv")

multi = result_2023_yield.iloc[:, 1:].values * result_2023_lite.iloc[:, 1:].values

result_2023_multi.iloc[:, 1:] = multi

def add_season_sums(df:pd.DataFrame) -> pd.DataFrame:
    first_season_sum = df.iloc[:6, 1:].sum().to_dict()
    second_season_sum = df.iloc[6:, 1:].sum().to_dict()

    first_season_row = {'土地类型': '第一季之和'}
    second_season_row = {'土地类型': '第二季之和'}

    for col in df.columns[1:]:
        first_season_row[col] = first_season_sum[col]
        second_season_row[col] = second_season_sum[col]

    df = df.append(first_season_row, ignore_index=True)
    df = df.append(second_season_row, ignore_index=True)
    
    return df

# 应用通用函数到现有表格
result_2023_multi = add_season_sums(result_2023_multi)

result_2023_multi.to_csv(
    "data/结果/result_2023_multi.csv", index=False, encoding="utf-8-sig"
)
