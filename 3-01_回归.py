import pandas as pd
import numpy as np

price_data = pd.read_csv("data/结果/full_销售单价.csv").iloc[:, 4:-1].values
mask = price_data > 0

price_means = np.sum(price_data * mask, axis=0) / np.sum(mask, axis=0).ravel()

sale_data = (
    pd.read_csv("data/结果/result_2023_multi.csv")
    .iloc[-1:, 1:]
    .values.reshape(-1)
    .ravel()
)

sale_data_regress = pd.read_csv("data/结果/full_预期销售量_sim - 副本.csv")

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression

plt.rcParams["font.family"] = "Microsoft YaHei"

data = pd.DataFrame({"平均售价": price_means[:5], "销售量": sale_data[:5]})

sns.regplot(
    x="平均售价",
    y="销售量",
    data=data,
    scatter_kws={"color": "blue"},
    line_kws={"color": "red"},
)

model = LinearRegression()
model.fit(price_means[:5].reshape(-1, 1), sale_data[:5])

slope = model.coef_[0]
intercept = model.intercept_

print(f"回归系数（斜率）: {slope}")
print(f"回归截距: {intercept}")

sale_data_regress.iloc[:, 2:7] = sale_data_regress.iloc[:, 2:7].applymap(
    lambda x: slope * x + intercept if x > 0 else 0
)

plt.title("粮食（豆类）")
plt.xlabel("平均售价")
plt.ylabel("销售量")

plt.show()

data = pd.DataFrame({"平均售价": price_means[5:16], "销售量": sale_data[5:16]})

sns.regplot(
    x="平均售价",
    y="销售量",
    data=data,
    scatter_kws={"color": "blue"},
    line_kws={"color": "red"},
)

model = LinearRegression()
model.fit(price_means[5:16].reshape(-1, 1), sale_data[5:16])

slope = model.coef_[0]
intercept = model.intercept_

print(f"回归系数（斜率）: {slope}")
print(f"回归截距: {intercept}")

sale_data_regress.iloc[:, 7:19] = sale_data_regress.iloc[:, 7:19].applymap(
    lambda x: slope * x + intercept if x > 0 else 0
)

plt.title("粮食")
plt.xlabel("平均售价")
plt.ylabel("销售量")

plt.show()

data = pd.DataFrame({"平均售价": price_means[16:19], "销售量": sale_data[16:19]})

sns.regplot(
    x="平均售价",
    y="销售量",
    data=data,
    scatter_kws={"color": "blue"},
    line_kws={"color": "red"},
)

model = LinearRegression()
model.fit(price_means[16:19].reshape(-1, 1), sale_data[16:19])

slope = model.coef_[0]
intercept = model.intercept_

print(f"回归系数（斜率）: {slope}")
print(f"回归截距: {intercept}")

sale_data_regress.iloc[:, 18:21] = sale_data_regress.iloc[:, 18:21].applymap(
    lambda x: slope * x + intercept if x > 0 else 0
)

plt.title("蔬菜（豆类）")
plt.xlabel("平均售价")
plt.ylabel("销售量")

plt.show()

data = pd.DataFrame({"平均售价": price_means[19:37], "销售量": sale_data[19:37]})

sns.regplot(
    x="平均售价",
    y="销售量",
    data=data,
    scatter_kws={"color": "blue"},
    line_kws={"color": "red"},
)

model = LinearRegression()
model.fit(price_means[19:37].reshape(-1, 1), sale_data[19:37])

slope = model.coef_[0]
intercept = model.intercept_

print(f"回归系数（斜率）: {slope}")
print(f"回归截距: {intercept}")

sale_data_regress.iloc[:, 21:39] = sale_data_regress.iloc[:, 21:39].applymap(
    lambda x: slope * x + intercept if x > 0 else 0
)

plt.show()

data = pd.DataFrame({"平均售价": price_means[37:], "销售量": sale_data[37:]})

sns.regplot(
    x="平均售价",
    y="销售量",
    data=data,
    scatter_kws={"color": "blue"},
    line_kws={"color": "red"},
)

model = LinearRegression()
model.fit(price_means[37:].reshape(-1, 1), sale_data[37:])

slope = model.coef_[0]
intercept = model.intercept_

print(f"回归系数（斜率）: {slope}")
print(f"回归截距: {intercept}")

sale_data_regress.iloc[:, 39:] = sale_data_regress.iloc[:, 39:].applymap(
    lambda x: slope * x + intercept if x > 0 else 0
)

plt.title("食用菌")
plt.xlabel("平均售价")
plt.ylabel("销售量")

plt.show()

sale_data_regress.clip(lower=0).to_csv(
    "data/结果/full_预期销售量_regress.csv", index=False, encoding="utf-8-sig"
)
