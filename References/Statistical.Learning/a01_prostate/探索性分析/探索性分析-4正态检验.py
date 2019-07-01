# 关掉所有警告信息
import warnings
warnings.filterwarnings('ignore')


import pandas as pd
from scipy import stats
# 读取数据，数据项之间以"\t"分隔，第一列是索引列
df = pd.read_csv("../prostate.data",sep="\t",index_col=0)

print(df.head(10))
n=len(df)
value_cols = ['lcavol','lweight','age','lbph','lcp','pgg45','lpsa']


print(f"样本数量{n}")
# from SAS:

# 当样本含量n ≤2000 时,结果以Shapiro - Wilk (W 检验) 为准,当样本含量n>2000 时,结果以Kolmogorov - Smirnov (D 检验) 为准

# Shapiro-Wilk 检验
# The Shapiro-Wilk test tests the null hypothesis that the data was drawn from a normal distribution.
#
# For N > 5000 the W test statistic is accurate but the p-value may not be.
#
# The chance of rejecting the null hypothesis when it is true is close to 5% regardless of sample size.
print("==  Shapiro-Wilk 检验 ==")

for col_name in value_cols:
    w,pvalue=stats.shapiro(df[col_name])
    label=''
    if pvalue<0.005:
        label ='***'
    elif pvalue< 0.01:
        label = '**'
    elif pvalue< 0.05:
        label = '*'

    print(f" {label}属性 {col_name} 统计量={w} p值={pvalue}")


# Kolmogorov-Smirnov检验
# Perform the Kolmogorov-Smirnov test for goodness of fit.
#
# This performs a test of the distribution F(x) of an observed random variable against a given distribution G(x). Under the null hypothesis the two distributions are identical, F(x)=G(x). The alternative hypothesis can be either ‘two-sided’ (default), ‘less’ or ‘greater’. The KS test is only valid for continuous distributions.
print("==  Kolmogorov-Smirnov检验 ==")

for col_name in value_cols:
    D, pvalue =stats.kstest(df[col_name],'norm')
    label=''
    if pvalue<0.005:
        label ='***'
    elif pvalue< 0.01:
        label = '**'
    elif pvalue< 0.05:
        label = '*'

    print(f" {label}属性 {col_name} 统计量={D} p值={pvalue}")