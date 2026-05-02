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
model1 = LogisticRegression(penalty=None)
model1.fit(X_train, y_train)
print("普通logistic回归系数")
print(pd.DataFrame(model1.coef_,columns=X.columns).round(3))


model2 = LogisticRegression(penalty="l1", solver='liblinear',C=0.1)
model2.fit(X_train, y_train)
print("带l1正则项(Lasso)的logistic回归系数")
print(pd.DataFrame(model2.coef_,columns=X.columns).round(3))

y_pred = model1.predict(X_test)
from sklearn.metrics import accuracy_score,f1_score
base_acc = accuracy_score(y_test, y_pred)
base_f1 = f1_score(y_test, y_pred)
print(f"基础模型准确率: {base_acc:.4f},f1 score:{base_f1}")

y_pred = model2.predict(X_test)
from sklearn.metrics import accuracy_score,f1_score
base_acc = accuracy_score(y_test, y_pred)
base_f1 = f1_score(y_test, y_pred)
print(f"删除特征后模型准确率: {base_acc:.4f},f1 score:{base_f1}")