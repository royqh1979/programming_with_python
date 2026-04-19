import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# 生成模拟数据（模拟真实分布）
n = 2000

# 对照组：正态分布，均值150元，标准差40元
control_group = np.random.normal(loc=150, scale=40, size=n)
control_group = np.maximum(control_group, 20)  # 最小消费20元

# 实验组：正态分布，均值160元（假设促销有效），标准差45元
treatment_group = np.random.normal(loc=160, scale=45, size=n)
treatment_group = np.maximum(treatment_group, 20)

# 步骤2：检验方差齐性（Levene检验）
print("\n步骤2：方差齐性检验（Levene Test）")
levene_stat, levene_p = stats.levene(control_group, treatment_group)
print(f"Levene统计量 = {levene_stat:.4f}, p值 = {levene_p:.4f}")
if levene_p > 0.05:
    print("结论：p>0.05，不能拒绝方差相等假设，使用标准t检验（equal_var=True）")
    equal_var = True
else:
    print("结论：p≤0.05，方差不齐，使用Welch校正t检验（equal_var=False）")
    equal_var = False

# 步骤3：执行独立t检验
print("\n步骤3：执行独立样本t检验")
t_stat, p_value = stats.ttest_ind(treatment_group, control_group, equal_var=equal_var)

print(f"t统计量 = {t_stat:.4f}")
print(f"p值 = {p_value:.6f}")
print(f"自由度 ≈ {len(control_group) + len(treatment_group) - 2}")

# 步骤4：计算效应量（Cohen's d）
print("\n步骤4：效应量计算（Cohen's d）")
pooled_std = np.sqrt(((n - 1) * control_group.var() + (n - 1) * treatment_group.var()) / (2 * n - 2))
cohens_d = (treatment_group.mean() - control_group.mean()) / pooled_std
print(f"Cohen's d = {cohens_d:.4f}")
if abs(cohens_d) < 0.2:
    effect_size = "小"
elif abs(cohens_d) < 0.5:
    effect_size = "中等"
else:
    effect_size = "大"
print(f"效应大小：{effect_size}")

# 步骤5：决策与置信区间
print("\n" + "=" * 60)
print("【检验结论】")
print("=" * 60)

alpha = 0.05
if p_value < alpha:
    print(f"结论：p值({p_value:.6f}) < α({alpha})，拒绝原假设")
    print("✓ 统计显著：新促销策略对客单价有显著影响")

    # 计算95%置信区间
    diff_mean = treatment_group.mean() - control_group.mean()
    se_diff = np.sqrt(control_group.var() / n + treatment_group.var() / n)
    ci_low = diff_mean - 1.96 * se_diff
    ci_high = diff_mean + 1.96 * se_diff

    print(f"\n95%置信区间：[${ci_low:.2f}, ${ci_high:.2f}]")
    print(f"解释：有95%把握认为促销策略使客单价提升{ci_low:.2f}~{ci_high:.2f}元")

    # ROI计算
    cost_per_user = 15  # 假设每张券平均成本15元
    revenue_lift = diff_mean
    roi = (revenue_lift - cost_per_user) / cost_per_user * 100
    print(f"\n业务建议：")
    print(f"• 平均每用户增收：${revenue_lift:.2f}")
    print(f"• 每用户券成本：${cost_per_user}")
    print(f"• ROI：{roi:.1f}%")
    if roi > 0:
        print("• 建议：大规模推广该促销策略")
    else:
        print("• 建议：优化券面额或发放人群，当前ROI为负")

else:
    print(f"结论：p值({p_value:.6f}) ≥ α({alpha})，不能拒绝原假设")
    print("✗ 统计不显著：无充分证据表明促销策略有效")
    print("建议：")
    print("• 可能样本量不足，建议延长测试时间")
    print("• 或调整促销力度（如提高优惠面额）")

