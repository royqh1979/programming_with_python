import pandas as pd
import numpy as np

# 从scikit-learn库中导入iris样本数据集
from sklearn.datasets import load_iris

iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)

#显示基础描述性统计
print(df.describe())

#显示方差
print(df.var())