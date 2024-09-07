import pandas as pd

data_2023 = pd.read_csv("data/2023年的农作物种植情况.csv")

result_2023 = pd.read_csv("data/附件3/result_temple.csv")

for index, row in data_2023.iterrows():
    land_names = result_2023[result_2023["地块名"] == row["种植地块"]].index.tolist()
    row_idx = land_names[0] if row["种植季次"] != "第二季" else land_names[1]
    col_idx = row["作物名称"]
    result_2023.loc[row_idx, col_idx] = row["种植面积/亩"]

result_2023.fillna(0).to_csv(
    "data/结果/result_2023.csv", index=False, encoding="utf-8-sig"
)
