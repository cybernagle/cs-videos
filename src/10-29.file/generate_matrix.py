import pickle
import random

# 假设你的二维矩阵是一个名为matrix的变量

column = 100
row = 100
matrix = [[random.choice([0, 1]) for _ in range(column)] for _ in range(row)]  # 生成4x10的矩阵，包含随机的0和1
# 保存二维矩阵
with open('matrix.pkl', 'wb') as file:
    pickle.dump(matrix, file)

