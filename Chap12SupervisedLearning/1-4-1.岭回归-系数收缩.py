import numpy as np
import matplotlib.pyplot as plt

import matplotlib as mpl
mpl.rcParams['font.family']=['Microsoft Yahei', 'sans-serif']
mpl.rcParams['axes.unicode_minus']=False

# 模拟两个高度相关的特征（如房屋面积和房间数）
np.random.seed(42)
n = 50
x1 = np.random.normal(100, 20, n)  # 房屋面积
x2 = x1 / 20 + np.random.normal(0, 1, n)  # 房间数（与面积高度相关）
y = 2 * x1 + 3 + np.random.normal(0, 10, n)  # 真实关系：y = 2*面积 + 3

# 标准化
x1_std = (x1 - x1.mean()) / x1.std(ddof=1)
x2_std = (x2 - x2.mean()) / x2.std(ddof=1)
X = np.column_stack([x1_std, x2_std])
y = (y - y.mean()) / y.std(ddof=1)

# 计算不同alpha下的岭回归系数
from sklearn.linear_model import Ridge
alphas = [0, 0.1, 0.5, 1, 5, 10, 20, 40, 60, 80, 100]
coefs = []

for alpha in alphas:
    model = Ridge(alpha=alpha)
    model.fit(X, y)
    coefs.append(model.coef_)

coefs = np.array(coefs)

# 绘制系数路径
plt.plot(alphas, coefs[:, 0], 'bo-', linewidth=2, markersize=8, label='自变量 1 (面积)')
plt.plot(alphas, coefs[:, 1], 'rs-', linewidth=2, markersize=8, label='自变量 2 (房间数)')

# 标注
plt.axhline(y=0, color='gray', linestyle='--', alpha=0.7)
plt.xlabel('正则化强度 (α)', fontsize=16)
plt.ylabel('回归系数值', fontsize=16)
plt.title('岭回归：系数收缩', fontsize=18, fontweight='bold')
plt.legend(loc='upper right', fontsize=16)
plt.tick_params(labelsize=16)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()