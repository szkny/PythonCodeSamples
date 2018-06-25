"""
3次元曲面のプロット例
z=exp(-(x^2+y^2))
"""
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()  # プロット領域の作成
ax = fig.gca(projection='3d')  # プロット中の軸の取得。gca は"Get Current Axes" の略。

x = np.arange(-2, 2, 0.05)  # x点として[-2, 2]まで0.05刻みでサンプル
y = np.arange(-2, 2, 0.05)  # y点として[-2, 2]まで0.05刻みでサンプル
x, y = np.meshgrid(x, y)  # 上述のサンプリング点(x,y)を使ったメッシュ生成

z = np.exp(-(x**2 + y**2))  # exp(-(x^2+y^2))  を計算してzz座標へ格納する。

# 曲面のプロット。rstrideとcstrideはステップサイズ，cmapは彩色，linewidthは曲面のメッシュの線の太さ，をそれぞれ表す。
ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap='hsv', linewidth=0.3)

plt.show()  # 絵の出力。
