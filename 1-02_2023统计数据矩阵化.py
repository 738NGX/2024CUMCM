import pandas as pd

land_type_dict = {
    "平旱地": "A",
    "梯田": "B",
    "山坡地": "C",
    "水浇地": "D",
    "普通大棚": "E",
    "智慧大棚": "F",
}

tasks = {
    "亩产量": "亩产量/斤",
    "种植成本": "种植成本/(元/亩)",
    "销售单价下界": "销售单价下界/(元/斤)",
    "销售单价上界": "销售单价上界/(元/斤)",
    "销售单价均值": "销售单价均值/(元/斤)",
}

data_2023 = pd.read_csv("data/2023年统计的相关数据.csv")

result_2023 = pd.read_csv("data/附件3/result_temple_lite.csv")

for task, task_val in tasks.items():
    for index, row in data_2023.iterrows():
        land_names = result_2023[
            result_2023["土地类型"] == land_type_dict[row["地块类型"]]
        ].index.tolist()
        row_idx = land_names[0] if row["种植季次"] != "第二季" else land_names[1]
        col_idx = row["作物名称"]
        result_2023.loc[row_idx, col_idx] = row[task_val]
        result_2023.fillna(0).to_csv(
            f"data/结果/result_2023_{task}.csv", index=False, encoding="utf-8-sig"
        )
