import pandas as pd
import random
import numpy as np

random.seed(114514)
np.random.seed(1919810)

mean = 0.075
std_dev = 0.025
num_samples = 1000

random_numbers = np.random.normal(loc=mean, scale=std_dev, size=num_samples)

sale_data = pd.read_csv("data/结果/full_预期销售量.csv")

sale_data_sims = []
for t in range(0, 100):
    sale_data_sim = sale_data.copy()
    for year in range(2024, 2031):
        sale_data_sim.loc[sale_data_sim["年份"] == year, sale_data_sim.columns[2:7]] = (
            sale_data_sim.loc[
                sale_data_sim["年份"] == 2023, sale_data_sim.columns[2:7]
            ].values
            * (1 + 0.05 * (random.random() - 0.5))
        )
        sale_data_sim.loc[sale_data_sim["年份"] == year, sale_data_sim.columns[7:]] = (
            sale_data_sim.loc[
                sale_data_sim["年份"] == 2023, sale_data_sim.columns[7:]
            ].values
            * (1 + 0.05 * (random.random() - 0.5))
        )
        sale_data_sim.loc[sale_data_sim["年份"] == year, sale_data_sim.columns[7:9]] = (
            sale_data_sim.loc[
                sale_data_sim["年份"] == year - 1, sale_data_sim.columns[7:9]
            ].values
            * (1 + random_numbers[t])
        )
    sale_data_sims.append(sale_data_sim)
    
simulated_columns_list = []

for sim in sale_data_sims:
    simulated_columns = sim.iloc[:, 2:]
    simulated_columns_list.append(simulated_columns)

simulated_mean = pd.concat(simulated_columns_list).groupby(level=0).mean()

sale_data.iloc[:, 2:] = simulated_mean.values

sale_data.round(2).to_csv("data/结果/full_预期销售量_sim.csv", index=False)