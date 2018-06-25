# -*- coding: utf-8 -*-
from random import random
import matplotlib.pyplot as plt
import math
"""
2次元ランダムウォーク
"""

N_calc_list = [10]
x, y, r = 0, 0, 0
R_list = []

N = 100000

x_list = [0]
y_list = [0]
for n in range(N):
    '''
    角度θ(2pi単位)をランダムにするため，
    random()を使って[0,1]の一様乱数を発生させる。
    '''
    theta = 2.0*math.pi*random()
    x = x+math.cos(theta)  # x方向への移動。cos(θ)。
    y = y+math.sin(theta)  # y方向への移動。sin(θ)
    x_list.append(x)  # xの値をx_listに格納していく
    y_list.append(y)  # yの値をx_listに格納していく

# for plot
plt.plot(x_list, y_list)  # (x,y)のプロット
plt.xlabel('X ')  # ｘ軸のラベル
plt.ylabel('Y')  # y軸のラベル
plt.xlim([-120, 120])  # x軸の範囲
plt.ylim([-120, 120])  # y軸の範囲
plt.show()
