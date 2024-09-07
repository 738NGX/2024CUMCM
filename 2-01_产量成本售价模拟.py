import pandas as pd
import random

random.seed(114514)

yield_data = pd.read_csv("data/结果/full_亩产量.csv")
cost_data = pd.read_csv("data/结果/full_种植成本.csv")
price_data = pd.read_csv("data/结果/full_销售单价.csv")

# 农作物的种植成本平均每年增长5%左右
for year in range(2024, 2031):
    cost_data.loc[cost_data["年份"] == year, cost_data.columns[4:]] = cost_data.loc[
        cost_data["年份"] == 2023, cost_data.columns[4:]
    ].values * (1.05 ** (year - 2023))
    
cost_data.to_csv("data/结果/full_种植成本_sim.csv", index=False)

# 蔬菜类作物的销售价格有增长的趋势，平均每年增长5%左右
for year in range(2024, 2031):
    price_data.loc[price_data["年份"] == year, price_data.columns[20:41]] = price_data.loc[
        price_data["年份"] == 2023, price_data.columns[20:41]
    ].values * (1.05 ** (year - 2023))
    
# 食用菌的销售价格稳中有降，大约每年可下降1%~5%，特别是羊肚菌的销售价格每年下降幅度为5%
for year in range(2024, 2031):
    price_data.loc[price_data["年份"] == year, price_data.columns[-2:-1]] = (
        price_data.loc[price_data["年份"] == 2023, price_data.columns[-2:-1]].values
        * (0.95 ** (year - 2023))
    )
    
price_data_sims = []
for t in range(0, 100):
    price_data_sim = price_data.copy()
    for year in range(2024, 2031):
        price_data_sim.loc[
            price_data_sim["年份"] == year, price_data_sim.columns[41:-2]
        ] = price_data_sim.loc[
            price_data_sim["年份"] == year - 1, price_data_sim.columns[41:-2]
        ].values * (
            1 - 0.01 * random.randint(0, 5)
        )
    price_data_sims.append(price_data_sim)
    
simulated_columns_list = []

for sim in price_data_sims:
    simulated_columns = sim.iloc[:, 41:-2]
    simulated_columns_list.append(simulated_columns)

simulated_mean = pd.concat(simulated_columns_list).groupby(level=0).mean()

price_data.iloc[:, 41:-2] = simulated_mean.values

price_data.to_csv("data/结果/full_销售单价_sim.csv", index=False)

# 农作物的亩产量往往会受气候等因素的影响，每年会有±10%的变化。
yield_data_sims = []
for t in range(0, 100):
    yield_data_sim = yield_data.copy()
    for year in range(2024, 2031):
        yield_data_sim.loc[
            yield_data_sim["年份"] == year, yield_data_sim.columns[4:-1]
        ] = yield_data_sim.loc[
            yield_data_sim["年份"] == year - 1, yield_data_sim.columns[4:-1]
        ].values * (
            1 + 0.1 * (random.random() - 0.5)
        )
    yield_data_sims.append(yield_data_sim)
    
simulated_columns_list = []

for sim in yield_data_sims:
    simulated_columns = sim.iloc[:, 4:-1]
    simulated_columns_list.append(simulated_columns)

simulated_mean = pd.concat(simulated_columns_list).groupby(level=0).mean()

yield_data.iloc[:, 4:-1] = simulated_mean.values

yield_data.to_csv("data/结果/full_亩产量_sim.csv", index=False)