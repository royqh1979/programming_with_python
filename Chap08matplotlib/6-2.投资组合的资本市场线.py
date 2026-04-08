import numpy as np
import pandas as pd
import cvxpy as cp
import matplotlib.pyplot as plt
import scipy as sp

#使用中文字体
import matplotlib as mpl
mpl.rcParams['font.family']=['Microsoft Yahei', 'sans-serif']
mpl.rcParams['axes.unicode_minus']=False

data = pd.read_csv("5只A股股票的收盘价（2018年至2020年）.csv",encoding="GBK",index_col=0)

print(data.head())

#计算日对数投资回报率
R=np.log(data/data.shift(1))
R=R.dropna()
print(R.describe() )
#计算年化投资回报率
R_mean=R.mean()*252
print(R_mean)
#年化波动率
R_vol=R.std()*np.sqrt(252)
print(R_vol)
#协方差矩阵并做年化处理
R_cov = R.cov()*252
print(R_cov)
#相关系数矩阵
R_corr = R.corr()
print(R_corr)

#绘制n个投资组合的可行集
n=2000
Rp_lst = np.zeros(n)
Vp_lst = np.zeros(n)
for i in range(n):
    w=np.random.uniform(0,1,5)
    w=w/np.sum(w)
    Rp_lst[i] = w @ R_mean
    Vp_lst[i] = np.sqrt(w @ R_cov @ w.T)

plt.figure(figsize=(9,6))
plt.scatter(Vp_lst,Rp_lst)
plt.xlabel("波动率",fontsize=18)
plt.ylabel("预期收益率",fontsize=18)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.title("五种股票投资组合有效前沿",fontsize=18)
plt.grid()


#求解全局最小波动组合
w_mv = cp.Variable(5)
prob_mv = cp.Problem(
    cp.Minimize(cp.quad_form(w_mv, R_cov)),
    [cp.sum(w_mv) == 1, w_mv >= 0]
)
prob_mv.solve()
w_min = w_mv.value
Rp_min = w_min @ R_mean
Vp_min = np.sqrt(w_min @ R_cov @ w_min.T)

#
Rp_targets = np.linspace(Rp_min,0.3,100)
Rp_valids = []
Vp_valids = []
for r in Rp_targets:
    prob_mv = cp.Problem(
        cp.Minimize(cp.quad_form(w_mv, R_cov)),
        [cp.sum(w_mv) == 1, w_mv >= 0, w_mv @ R_mean == r]
    )
    prob_mv.solve()
    w = w_mv.value
    if w is not None:
        Rp_valids.append(r)
        Vp_valids.append(np.sqrt(w @ R_cov @ w.T))

plt.plot(Vp_valids,Rp_valids, label='有效前沿组合',lw=2)
plt.plot(Vp_min,Rp_min,'g*',markersize=16,label='最小波动率组合')

Rf = 0.0385
result = sp.optimize.minimize(
    fun = lambda w: -(w @ R_mean - Rf) / np.sqrt( w @ R_cov @ w.T),
    x0 = np.array([0.2]*5),
    bounds = [(0,1)]*5,
    constraints=[
        {'type':'eq', 'fun':lambda w:np.sum(w)-1}
    ]
)
wm = result['x']
Rm = wm @ R_mean
Vm = np.sqrt( wm @ R_cov @ wm.T)
sharpe_ratio = (Rm - Rf) / Vm

Rp_ml = np.linspace(Rf,0.2,100)
Vp_ml = (Rp_ml-Rf)/sharpe_ratio

plt.plot(Vp_ml, Rp_ml,'b--',lw=2, label='资本市场线')
plt.plot(Vm,Rm,'r*',markersize=16,label='市场组合')
plt.legend(fontsize=18)
plt.show()

