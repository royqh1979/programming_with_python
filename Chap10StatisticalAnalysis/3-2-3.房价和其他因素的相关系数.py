import pandas as pd
from scipy.stats import pearsonr
from sklearn.datasets import fetch_california_housing
# 加载真实数据
df = pd.read_csv("cal-housing.csv")
# 目标变量：房价中位数（十万美元）
print(f"\n数据集规模：{len(df):,}条真实记录")
# 计算三个关键指标的Pearson相关系数
features = ['MedInc', 'HouseAge', 'AveRooms', 'AveOccup']
target = 'MedHouseVal'
print("\n" + "=" * 70)
print("Pearson相关性分析结果（与房价的关系）")
print("=" * 70)
print(f"{'指标':<15}{'相关系数r':>12}{'p值':>12}{'R²':>12}")
print("-" * 70)
for feature in features:
    r, p = pearsonr(df[feature], df[target])
    r_squared = r ** 2
    print(f"{feature:<15}{r:>12.4f}{p:>12.2e}{r_squared:>12.4f}")

