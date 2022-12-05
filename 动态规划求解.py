'''
-*- coding: utf-8 -*-
@File  : 贪心算法.py
@Author: mqc
@Time  : 2022/12/1 19:05
'''
import math
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']


# 构造距离矩阵
def build_dist_array(points, dist_array):
    n = len(points)
    for i in range(n):
        for j in range(n):
            dist_array[i][j] = math.sqrt((points[i][0] - points[j][0]) ** 2 + (points[i][1] - points[j][1]) ** 2)
        dist_array[i][i] = float('inf')
    return dist_array


# 绘制最优路径
def draw_bestway(best_way):
    best_x = []
    best_y = []
    names = ['O', 'C', 'E', 'A', 'B', 'D']
    plt.grid(True)
    plt.rcParams['font.sans-serif'] = 'SimHei'
    plt.title("最优路径")
    for i in range(len(best_way)):
        best_x.append(best_way[i][0])
        best_y.append(best_way[i][1])
    plt.plot(best_x, best_y, color="green", linestyle="-", marker="o")
    for i in range(len(best_way) - 1):
        plt.arrow(best_way[i][0], best_way[i][1], best_way[i + 1][0] - best_way[i][0],
                  best_way[i + 1][1] - best_way[i][1], head_width=0.1, lw=0.1,
                  length_includes_head=True)
        plt.text(best_way[i][0], best_way[i][1], s=names[i], fontsize=20, color='red')  # ⽂本
    plt.text(best_way[-1][0], best_way[-1][1], s=names[-1], fontsize=20, color='red')  # ⽂本
    plt.show()


# 贪心算法
def greedy(start_node_idx, dist_array):
    idx = dist_array[start_node_idx].index(min(dist_array[start_node_idx]))  # 计算下一个点对应的index
    # 删除已计算过的点
    for i in range(len(dist_array)):
        dist_array[start_node_idx][i] = dist_array[i][start_node_idx] = float('inf')
    next_node_idx = idx  # 下一个点的位置
    return next_node_idx


if __name__ == "__main__":
    # 初始化坐标
    points = [[0, 0], [1, 1], [1, 3], [2, 2], [3, 1], [3, 3]]
    best_way = []  # 存储最优路径
    n = len(points)
    dist_array = [[0] * n for i in range(n)]  # 初始化距离矩阵
    build_dist_array(points, dist_array)  # 求距离矩阵中的各元素值
    start_node_idx = 0  # 初始点对应的index值
    t = 0
    while t < n:
        print(points[start_node_idx], end='>>>>>')
        best_way.append(points[start_node_idx])
        start_node_idx = greedy(start_node_idx, dist_array)
        t += 1
    draw_bestway(best_way)
