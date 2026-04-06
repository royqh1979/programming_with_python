import numpy as np

n_samples = 1000
n_defaults = 50
# 原始数据重建
data = np.array([1]*n_defaults + [0]*(n_samples - n_defaults))
n_bootstrap = 10000
bootstrap_p = []
#bootstrap样本构建
for _ in range(n_bootstrap):
    # 有放回抽样
    sample = np.random.choice(data, size=n_samples, replace=True)
    bootstrap_p.append(np.mean(sample))

# 百分位法计算CI
ci_boot_lower = np.percentile(bootstrap_p, 2.5)
ci_boot_upper = np.percentile(bootstrap_p, 97.5)

print(f"Bootstrap重复次数: {n_bootstrap}")
print(f"95% CI: [{ci_boot_lower:.3f}, {ci_boot_upper:.3f}]")
print(f"Bootstrap标准误: {np.std(bootstrap_p):.3f}")