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
print("=" * 50)
print("单样本t检验分析结果")
print("=" * 50)
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

# 决策
print("\n【假设检验决策】")
print(f"H₀: μ = {mu_0} 克（平均灌装量等于标称值）")
print(f"H₁: μ ≠ {mu_0} 克（平均灌装量不等于标称值）")

if abs(t_statistic) > t_critical:
    print(f"\n|t| = {abs(t_statistic):.3f} > t临界 = {t_critical:.3f}")
    print("结论：拒绝原假设，平均灌装量与200克存在显著差异")
else:
    print(f"\n|t| = {abs(t_statistic):.3f} ≤ t临界 = {t_critical:.3f}")
    print("结论：不拒绝原假设，无充分证据表明平均灌装量与200克不同")

if p_value < alpha:
    print(f"\np值({p_value:.5f}) < α({alpha})，结果统计显著")
else:
    print(f"\np值({p_value:.5f}) ≥ α({alpha})，结果不显著")

# 计算95%置信区间
ci_lower = sample_mean - t_critical * se
ci_upper = sample_mean + t_critical * se
print(f"\n【置信区间】")
print(f"95%置信区间: [{ci_lower:.3f}, {ci_upper:.3f}] 克")
