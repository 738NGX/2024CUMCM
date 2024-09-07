import pandas as pd

result_full = pd.read_csv("data/附件3/result_temple_full.csv", header=1)
data_2023=pd.read_csv("data/2023年统计的相关数据.csv")

land_type_dict = {
    "A": "平旱地",
    "B": "梯田",
    "C": "山坡地",
    "D": "水浇地",
    "E": "普通大棚",
    "F": "智慧大棚",
}

yield_data = result_full.copy()
cost_data = result_full.copy()
price_data = result_full.copy()

for i in range(0, 656):
    for j in range(4, 45):
        crop = yield_data.columns[j]
        land_type = land_type_dict[yield_data["地块名"][i][0]]
        season = yield_data["季度"][i]
        
        search=data_2023[
            (data_2023["作物名称"] == crop)
            & (data_2023["地块类型"] == land_type)
            & (data_2023["种植季次"] == season)
        ]["亩产量/斤"].values
        yield_data.iloc[i, j] = 0 if search.size == 0 else search[0]
        
        search=data_2023[
            (data_2023["作物名称"] == crop)
            & (data_2023["地块类型"] == land_type)
            & (data_2023["种植季次"] == season)
        ]["种植成本/(元/亩)"].values
        cost_data.iloc[i, j] = 0 if search.size == 0 else search[0]
        
        search=data_2023[
            (data_2023["作物名称"] == crop)
            & (data_2023["地块类型"] == land_type)
            & (data_2023["种植季次"] == season)
        ]["销售单价均值/(元/斤)"].values
        price_data.iloc[i, j] = 0 if search.size == 0 else search[0]
        
yield_data.to_csv("data/结果/full_亩产量.csv", index=False, encoding="utf-8-sig")
cost_data.to_csv("data/结果/full_种植成本.csv", index=False, encoding="utf-8-sig")
price_data.to_csv("data/结果/full_销售单价.csv", index=False, encoding="utf-8-sig")