import pandas as pd
import numpy as np
import coptpy as copt

result_full = pd.read_csv("data/附件3/result_temple_full.csv", header=1)

# 用掩码来标记缺失值,只对缺失值进行规划
mask = ~np.isnan(result_full.iloc[:, 4:-1].values)
known_values = np.nan_to_num(result_full.iloc[:, 4:-1].values)

# 创建模型
env = copt.Envr()
model = env.createModel()

# X:种植量矩阵;D:种植决策矩阵
X = model.addVars(656, 41, vtype=copt.COPT.CONTINUOUS, lb=0)
D = model.addVars(656, 41, vtype=copt.COPT.BINARY)

# 约束1:只规划未知的值
for i in range(656):
    for j in range(41):
        if mask[i, j]:
            model.addConstr(X[i, j] == known_values[i, j])

# 约束2:种植量不能超过上限
for i in range(656):
    model.addConstr(
        copt.quicksum(X[i, j] for j in range(41)) <= result_full["种植上限"][i]
    )

# 约束3:如果种植,种植量不能低于下限
for i in range(656):
    for j in range(41):
        model.addConstr(X[i, j] <= result_full["种植上限"][i] * D[i, j])
        model.addConstr(X[i, j] >= 0.2 * result_full["种植上限"][i] * D[i, j])

# 约束4:水稻约束
water_lands = [
    (
        i,
        result_full[(result_full["地块名"] == f"D{j}") & (result_full["季度"] == 1)][
            "种植上限"
        ].values[0],
    )
    for j in range(1, 9)
    for i in result_full[
        (result_full["地块名"] == f"D{j}") & (result_full["季度"] == 1)
    ].index[1:]
]

for x, u in water_lands:
    l = 0.2 * u
    for i in range(16, 34):
        delta = model.addVar(vtype=copt.COPT.BINARY)
        model.addConstr(X[x, 15] <= u * (1 - delta))
        model.addConstr(X[x, i] <= u * delta)
    for i in range(34, 37):
        delta = model.addVar(vtype=copt.COPT.BINARY)
        model.addConstr(X[x, 15] <= u * (1 - delta))
        model.addConstr(X[x + 28, i] <= u * delta)

# 约束5:重茬约束
for index, row in result_full[["地块名", "种植上限"]].drop_duplicates().iterrows():
    land_indices = result_full[result_full["地块名"] == row["地块名"]].index.tolist()

    u = row["种植上限"]
    l = 0

    for j in range(41):
        for i in range(len(land_indices) - 1):
            idx_1 = land_indices[i]
            idx_2 = land_indices[i + 1]
            delta = model.addVar(vtype=copt.COPT.BINARY)
            model.addConstr(X[idx_1, j] <= u * (1 - delta))
            model.addConstr(X[idx_2, j] <= u * delta)

dry_lands = [
    "A1",
    "A2",
    "A3",
    "A4",
    "A5",
    "A6",
    "B1",
    "B2",
    "B3",
    "B4",
    "B5",
    "B6",
    "B7",
    "B8",
    "B9",
    "B10",
    "B11",
    "B12",
    "B13",
    "B14",
    "C1",
    "C2",
    "C3",
    "C4",
    "C5",
    "C6",
]
wet_lands = [
    "D1",
    "D2",
    "D3",
    "D4",
    "D5",
    "D6",
    "D7",
    "D8",
    "E1",
    "E2",
    "E3",
    "E4",
    "E5",
    "E6",
    "E7",
    "E8",
    "E9",
    "E10",
    "E11",
    "E12",
    "E13",
    "E14",
    "E15",
    "E16",
    "F1",
    "F2",
    "F3",
    "F4",
]

# 约束6:三年豆类约束
for land in dry_lands:
    land_indices = result_full[result_full["地块名"] == land].index

    for i in range(0, 6):
        expr = copt.quicksum(
            X[idx, col] for idx in land_indices[i : i + 3] for col in range(0, 5)
        )  # sum over 0:5 columns
        model.addConstr(
            expr >= 0.2 * result_full["种植上限"][land_indices[0]],
            name=f"dry_land_{land}_constraint_{i}",
        )

for land in wet_lands:
    land_indices = result_full[result_full["地块名"] == land].index

    for i in range(0, 11):
        expr = copt.quicksum(
            X[idx, col] for idx in land_indices[i : i + 6] for col in range(16, 19)
        )
        model.addConstr(
            expr >= 0.2 * result_full["种植上限"][land_indices[0]],
            name=f"wet_land_{land}_constraint_{i}",
        )

yield_data = pd.read_csv("data/结果/full_亩产量_sim.csv").iloc[:, 4:-1].values
cost_data = pd.read_csv("data/结果/full_种植成本_sim.csv").iloc[:, 4:-1].values
price_data = pd.read_csv("data/结果/full_销售单价_sim.csv").iloc[:, 4:-1].values
sale_data = pd.read_csv("data/结果/full_预期销售量_regress.csv")
sale_data_mean1 = sale_data[sale_data["季度"] == 1].mean().values[2:]
sale_data_mean2 = sale_data[sale_data["季度"] == 2].mean().values[2:]

# S:实际销售量矩阵
S = model.addVars(656, 41, vtype=copt.COPT.CONTINUOUS, lb=0)

model.addConstrs(
    S[i, j] <= X[i, j] * yield_data[i, j] for i in range(656) for j in range(41)
)
model.addConstrs(
    copt.quicksum(
        S[i, j] for i in result_full[(result_full["季度"] == 1)].index.tolist()
    )
    <= sale_data_mean1[j] * 432
    for j in range(41)
)
model.addConstrs(
    copt.quicksum(
        S[i, j] for i in result_full[(result_full["季度"] == 2)].index.tolist()
    )
    <= sale_data_mean2[j] * 224
    for j in range(41)
)
model.addConstr(
    copt.quicksum(
        S[i, j] * price_data[i, j] - X[i, j] * cost_data[i, j]
        for i in result_full[result_full["季度"] == 1].index.tolist()
        for j in range(0,5)
    )
    + copt.quicksum(
        S[i, j] * price_data[i, j] - X[i, j] * cost_data[i, j]
        for i in result_full[result_full["季度"] == 2].index.tolist()
        for j in range(0,5)
    ) <= 10000000
)
model.addConstr(
    copt.quicksum(
        S[i, j] * price_data[i, j] - X[i, j] * cost_data[i, j]
        for i in result_full[result_full["季度"] == 1].index.tolist()
        for j in range(5,16)
    )
    + copt.quicksum(
        S[i, j] * price_data[i, j] - X[i, j] * cost_data[i, j]
        for i in result_full[result_full["季度"] == 2].index.tolist()
        for j in range(5,16)
    ) <= 40000000
)
model.addConstr(
    copt.quicksum(
        S[i, j] * price_data[i, j] - X[i, j] * cost_data[i, j]
        for i in result_full[result_full["季度"] == 1].index.tolist()
        for j in range(16,19)
    )
    + copt.quicksum(
        S[i, j] * price_data[i, j] - X[i, j] * cost_data[i, j]
        for i in result_full[result_full["季度"] == 2].index.tolist()
        for j in range(16,19)
    ) <= 30000000
)
model.addConstr(
    copt.quicksum(
        S[i, j] * price_data[i, j] - X[i, j] * cost_data[i, j]
        for i in result_full[result_full["季度"] == 1].index.tolist()
        for j in range(19,37)
    )
    + copt.quicksum(
        S[i, j] * price_data[i, j] - X[i, j] * cost_data[i, j]
        for i in result_full[result_full["季度"] == 2].index.tolist()
        for j in range(19,37)
    ) <= 10000000
)
model.addConstr(
    copt.quicksum(
        S[i, j] * price_data[i, j] - X[i, j] * cost_data[i, j]
        for i in result_full[result_full["季度"] == 1].index.tolist()
        for j in range(37,41)
    )
    + copt.quicksum(
        S[i, j] * price_data[i, j] - X[i, j] * cost_data[i, j]
        for i in result_full[result_full["季度"] == 2].index.tolist()
        for j in range(37,41)
    ) <= 10000000
)

# 目标函数
objective = copt.quicksum(
    S[i, j] * price_data[i, j] - X[i, j] * cost_data[i, j]
    for i in result_full[result_full["季度"] == 1].index.tolist()
    for j in range(41)
) + copt.quicksum(
    S[i, j] * price_data[i, j] - X[i, j] * cost_data[i, j]
    for i in result_full[result_full["季度"] == 2].index.tolist()
    for j in range(41)
)

# 求解
model.setObjective(objective, copt.COPT.MAXIMIZE)
model.solve()

if model.status == copt.COPT.OPTIMAL:
    optimized_X = np.zeros((656, 41))
    for i in range(656):
        for j in range(41):
            optimized_X[i, j] = X[i, j].x
else:
    print("未找到最优解！")

# 保存结果
result_full.iloc[:, 4:-1] = optimized_X.round(2)
result_full.to_csv(
    "data/结果/result_full_regress.csv", index=False, encoding="utf-8-sig"
)
