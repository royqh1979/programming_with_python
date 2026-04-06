import numpy as np
import cvxpy as cp

# ============================================
# 步骤1：下载数据
# ============================================
tickers=['中国电影','中国平安','中国国旅','中国卫星','中国医药']
data=np.loadtxt("5只A股股票收盘价的日数据.csv",delimiter=',',skiprows=1,usecols=(1,2,3,4,5))
data=data.T # 转置
# ============================================
# 步骤2：计算收益率和统计量
# ============================================

returns = np.log(data[:,1:]/data[:,:-1])
mu = np.mean(returns,1) * 252          # 年化收益
Sigma = np.cov(returns) * 252        # 年化协方差
n = len(tickers)

returns
print(mu)
print(Sigma)

# ============================================
# 步骤3：最小方差组合
# ============================================

w_mv = cp.Variable(n)
prob_mv = cp.Problem(
    cp.Minimize(cp.quad_form(w_mv, Sigma)),
    [cp.sum(w_mv) == 1, w_mv >= 0]
)
prob_mv.solve()

print(f"\n=== 最小方差组合 ===")
for idx,val in zip(tickers, w_mv.value):
    print(f"权重: {idx}, {val:.4f}")
print(f"波动率: {np.sqrt(w_mv.value @ Sigma @ w_mv.value)*100:.2f}%")
print(f"收益率: {mu @ w_mv.value *100:.2f}%")

