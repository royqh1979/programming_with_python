import pandas as pd

df = pd.read_csv("credit_default_dataset.csv")
print(df)

def standardize(f):
    return (f - f.mean())/f.std()

# ========== 划分训练集和测试集 ==========
X = df.drop('违约', axis=1)
for f in ["年收入","信用卡额度","历史逾期次数","月均消费","账户年限","近6月查询次数","教育水平"]:
    X[f] = standardize(X[f])
y = df['违约']

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# ========== 训练随机森林 ==========
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()

from sklearn.feature_selection import SequentialFeatureSelector
# 前向特征选择
sfs = SequentialFeatureSelector(
    estimator=model,      # 基学习器
    n_features_to_select=4,   # 最终保留4个特征
    direction='forward',      # 前向法（还可选 'backward' 后向法）
    scoring='accuracy',       # 评估指标
    cv=5,                     # 5折交叉验证
    n_jobs=-1                 # 并行计算
)

sfs.fit(X_train, y_train)

# 查看结果
print("被选中的特征索引:",X.columns[sfs.get_support()])
print("被选中的特征索引:", sfs.get_support(indices=True))
print("被选中的特征掩码:", sfs.get_support())

