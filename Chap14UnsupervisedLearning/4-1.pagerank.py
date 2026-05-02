import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
#使用中文字体
from pylab import mpl
mpl.rcParams['font.sans-serif']="Simsun"
mpl.rcParams['axes.unicode_minus']=False

# ==================== 1. 构建网络（以 5 个网页的链接关系为例） ====================
# 节点：0=A, 1=B, 2=C, 3=D, 4=E
# 有向边：A→B, A→C, B→C, C→A, D→A, D→C, E→D
edges = [(0, 1), (0, 2), (1, 2), (2, 0), (3, 0), (3, 2), (4, 3)]
n = 5
names = ['A', 'B', 'C', 'D', 'E']

# ==================== 2. 构建转移矩阵 M（列随机矩阵） ====================
# M[j, i] 表示从节点 i 跳转到节点 j 的概率
M = np.zeros((n, n))
for i, j in edges:
    M[j, i] = 1.0

# 归一化：每列除以该节点的出度；若出度为0（悬挂节点），则均匀分配
out_degrees = M.sum(axis=0)
for i in range(n):
    if out_degrees[i] > 0:
        M[:, i] /= out_degrees[i]
    else:
        M[:, i] = 1.0 / n

# ==================== 3. 幂迭代计算 PageRank ====================
d = 0.85                     # 阻尼系数
pr = np.ones(n) / n          # 初始化：均匀分布
history = [pr.copy()]        # 记录收敛过程

for it in range(100):
    pr_new = (1 - d) / n + d * M.dot(pr)
    history.append(pr_new.copy())
    if np.max(np.abs(pr_new - pr)) < 1e-6:
        print(f"✓ 第 {it + 1} 次迭代后收敛\n")
        break
    pr = pr_new

# ==================== 4. 输出结果 ====================
print("=== 各节点 PageRank 值 ===")
for name, val in zip(names, pr):
    print(f"  {name}: {val:.4f}")
print(f"\n归一化校验（总和应为 1.0）: {pr.sum():.4f}")

# ==================== 5. 网络结构可视化 ====================
G = nx.DiGraph()
G.add_edges_from(edges)


# 左图：网络拓扑（节点大小 ∝ PageRank）
fig,ax = plt.subplots(1, 1)
pos = nx.spring_layout(G, seed=42, k=1.5)
node_sizes = pr * 4000
node_colors = pr/4
nx.draw(G, pos, with_labels=True, labels={i: names[i] for i in range(n)},
        node_size=node_sizes, node_color=node_colors, cmap=plt.cm.Blues,
        font_size=11, font_weight='bold', arrows=True, arrowsize=15,
        edge_color='gray', width=1.2, alpha=0.9,ax=ax)
ax.set_title("网页链接网络\n（节点越大、颜色越深 = 越重要）", fontsize=12)
fig.tight_layout()

# 右图：收敛曲线
fig,ax = plt.subplots(1, 1)
history = np.array(history)
for i in range(n):
    ax.plot(history[:, i], label=names[i], marker='o', markersize=3)
ax.set_xlabel('迭代次数', fontsize=11)
ax.set_ylabel('PageRank 值', fontsize=11)
ax.set_title('幂迭代收敛过程', fontsize=12)
ax.legend()
ax.grid(True, alpha=0.3)
fig.tight_layout()

plt.show()

plt.tight_layout()
plt.show()