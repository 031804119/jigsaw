import numpy as np


class Prediction:
    def __init__(self):
        self.n = 3
        self.N = self.n * self.n
        self.bk = 9
        q_tab = np.load('./q_tab_9.npz')
        k = q_tab['k']
        v = q_tab['v']
        self.q_tab = dict(zip(k, v))  # 构建Q表
        self.X = [-1, 0, 1, 0]
        self.Y = [0, -1, 0, 1]

    def pre_step(self, x):  # 预测状态 x 对应的步数
        x = x.reshape(1, -1)
        k = ""
        for i in range(self.N):
            k += str(x[0, i])
        v = self.q_tab.get(k, -1)
        return v

    def pre_next(self, sta, bk_x, bk_y):  # 预测下一步往哪个方向走
        step = [10000, 10000, 10000, 10000]
        direction = np.random.permutation(4)  # 生成0~3的随机排列
        for i in direction:
            x = bk_x + self.X[i]
            y = bk_y + self.Y[i]
            if x < 0 or x >= self.n or y < 0 or y >= self.n:
                continue
            t = sta[x][y]
            sta[x][y] = self.bk
            sta[bk_x][bk_y] = t
            step[i] = self.pre_step(sta)
            sta[x][y] = t
            sta[bk_x][bk_y] = self.bk
        return np.argmin(step)