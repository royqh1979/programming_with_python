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

#使用statsmodels计算
from statsmodels.stats.weightstats import ztest
z_statistics, p_value = ztest(sample_data,value=mu_0)

print("使用statsmodels计算")
print("z统计量：",z_statistics)
print("p值：", p_value)

#手工计算
# 计算样本统计量
n = len(sample_data)
sample_mean = np.mean(sample_data)
# unbiased estimator of standard deviation
sigma = np.std(sample_data, ddof=1)
# 计算标准误
se = sigma / np.sqrt(n)

# 计算Z统计量
z_statistic = (sample_mean-mu_0)/se

# 计算双侧检验的p值
p_value = 2 * (1 - stats.norm.cdf(abs(z_statistic)))

# 确定临界值
z_critical = stats.norm.ppf(1 - alpha/2)

# 输出结果
print()
print("手工计算")
print(f"样本量 n = {n}")
print(f"样本均值 x̄ = {sample_mean:.3f} 克")
print(f"标准误 SE = {se:.3f}")
print(f"Z统计量 = {z_statistic:.3f}")
print(f"p值 = {p_value:.4f}")
print(f"临界值 = ±{z_critical:.3f}")
print("-" * 40)

# 决策
if abs(z_statistic) > z_critical:
    print("结论：拒绝原假设，平均灌装量与200克存在显著差异")
else:
    print("结论：不拒绝原假设，无充分证据表明平均灌装量与200克不同")

if p_value < alpha:
    print(f"p值({p_value:.4f}) < α({alpha})，结果统计显著")
else:
    print(f"p值({p_value:.4f}) ≥ α({alpha})，结果不显著")

# 计算95%置信区间
ci_lower = sample_mean-z_critical * se
ci_upper = sample_mean+z_critical * se
print(f"\n95%置信区间: [{ci_lower:.3f}, {ci_upper:.3f}] 克")
