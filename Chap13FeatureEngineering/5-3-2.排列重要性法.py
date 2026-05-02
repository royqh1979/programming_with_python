import pandas as pd

df = pd.read_csv("credit_default_dataset.csv")
print(df)

# ========== 划分训练集和测试集 ==========
X = df.drop('违约', axis=1)
y = df['违约']

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# ========== 训练随机森林 ==========
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=8)
rf.fit(X_train, y_train)

print(f"基础模型特征重要性:")
importance = pd.Series(rf.feature_importances_, index=X.columns)
importance = importance.sort_values(ascending=False)
print(importance)

from sklearn.inspection import permutation_importance
# 计算排列重要性
perm_importance = permutation_importance(
    rf, X_train, y_train,
    n_repeats=30,           # 重复30次打乱，取平均
    random_state=42,
    scoring='accuracy'
)

# 构建重要性DataFrame
feature_names = X.columns.tolist()
importance_df = pd.DataFrame({
    '特征': feature_names,
    '重要性均值': perm_importance.importances_mean,
    '重要性标准差': perm_importance.importances_std
}).sort_values('重要性均值', ascending=False)

print("\n排列重要性排序：")
print(importance_df.to_string(index=False))

#删除后两个特征
X1_train = X_train.drop(columns=["教育水平","婚姻状况"])
X1_test = X_test.drop(columns=["教育水平","婚姻状况"])
rf2 = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=8)
rf2.fit(X1_train, y_train)

y_pred = rf.predict(X_test)
from sklearn.metrics import accuracy_score,f1_score
base_acc = accuracy_score(y_test, y_pred)
base_f1 = f1_score(y_test, y_pred)
print(f"基础模型准确率: {base_acc:.4f},f1 score:{base_f1}")

y_pred = rf2.predict(X1_test)
from sklearn.metrics import accuracy_score,f1_score
base_acc = accuracy_score(y_test, y_pred)
base_f1 = f1_score(y_test, y_pred)
print(f"删除特征后模型准确率: {base_acc:.4f},f1 score:{base_f1}")