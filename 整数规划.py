'''
-*- coding: utf-8 -*-
@File  : 整数规划.py
@Author: mqc
@Time  : 2022/12/2 18:31
'''
# 0-1整数规划求解有返回的TSP问题

from gurobipy import *
import numpy as np


def get_dist_array(coord):
    coord = np.array(coord)
    w, h = coord.shape
    coordinates = np.zeros((w, h), float)
    for i in range(w):
        for j in range(h):
            coordinates[i, j] = float(coord[i, j])
    # x点坐标
    data_x = coordinates[:, 0]
    # y点坐标
    data_y = coordinates[:, 1]
    data_num = len(data_x)
    dist_array = np.zeros((data_num, data_num))
    for i in range(0, data_num):
        for j in range(0, data_num):
            if (i == j):
                dist_array[i, j] = 100000
            else:
                dist_array[i, j] = math.sqrt((data_x[i] - data_x[j]) ** 2 + (data_y[i] - data_y[j]) ** 2)
    return dist_array


# 构造0-1整数规划模型
def bulid_model(dist_array):
    model = Model("TSP")
    data_num = dist_array.shape[0]
    # 定义变量
    x = model.addMVar((data_num, data_num), lb=0, ub=1, vtype=GRB.BINARY)  # lb变量下限， ub变量上限
    u = model.addMVar((data_num), vtype=GRB.CONTINUOUS)  # lb变量下限， ub变量上限
    # 构造目标函数
    objsum = 0
    for i in range(0, data_num):
        for j in range(0, data_num):
            objsum = objsum + x[i, j] * dist_array[i, j]
    model.setObjective(objsum, GRB.MINIMIZE)
    # 构造约束条件
    for i in range(0, data_num):
        constrsum = sum(x[i, :])
        model.addConstr(constrsum == 1)
    for j in range(0, data_num):
        constrsum1 = sum(x[:, j])
        model.addConstr(constrsum1 == 1)
    # 防止形成子回路
    for i in range(1, data_num):
        for j in range(1, data_num):
            if (i != j):
                model.addConstr((u[i] - u[j] + data_num * x[i, j]) <= data_num - 1)
    model.optimize()
    best = (x.X).astype(int)
    return model, best


if __name__ == '__main__':
    points = [[0, 0], [1, 1], [1, 3], [2, 2], [3, 1], [3, 3]]
    dist_array = get_dist_array(points)
    model, best = bulid_model(dist_array)
    print(f"最优目标值为：{model.ObjVal}")
    print(f"最优分配为：{best}")
