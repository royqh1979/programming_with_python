import numpy as np
from scipy import stats

# 样本数据
sample_data = np.array([
    198, 205, 202, 196, 201, 204, 199, 203, 197, 200,
    206, 198, 201, 205, 199, 202, 197, 204, 200, 203,
    198, 206, 201, 199, 205, 202, 197, 204, 200, 203,
    199, 205, 201, 198, 202, 200, 206, 199, 203, 197,
    204, 201, 205, 198, 202, 200, 199, 203, 201, 204
])

# 已知参数
mu_0 = 200      # 标称均值
alpha = 0.05    # 显著性水平

#使用scipy的ttest_1samp函数计算
print("使用scipy计算")
print(stats.ttest_1samp(sample_data,mu_0))

#手工计算
# 计算样本统计量
n = len(sample_data)
sample_mean = np.mean(sample_data)
sample_std = np.std(sample_data, ddof=1)  # 样本标准差（无偏估计）

# 计算标准误
se = sample_std / np.sqrt(n)

# 计算t统计量
t_statistic = (sample_mean - mu_0) / se

# 自由度
df = n - 1

# 计算双侧检验的p值
p_value = 2 * (1 - stats.t.cdf(abs(t_statistic), df))

# 确定临界值
t_critical = stats.t.ppf(1 - alpha/2, df)

# 输出结果
print()
print("手工计算")
print(f"样本量 n = {n}")
print(f"样本均值 x̄ = {sample_mean:.3f} 克")
print(f"样本标准差 s = {sample_std:.3f} 克")
print(f"标准误 SE = {se:.3f}")
print(f"自由度 df = {df}")
print("-" * 50)
print(f"t统计量 = {t_statistic:.3f}")
print(f"p值 = {p_value:.5f}")
print(f"临界值 = ±{t_critical:.3f}")
print("=" * 50)

