import pandas as pd
import numpy as np

np.random.seed(42)
df = pd.read_csv("bank.csv")

df_job = pd.get_dummies(df["job"],prefix="j")
df_material = pd.get_dummies(df["marital"], prefix="m")
df_edu = pd.get_dummies(df["education"], prefix = "e")
df["default"] = np.where(df["default"]=='yes',1,0)
df["housing"] = np.where(df["housing"]=='yes',1,0)
df["loan"] = np.where(df["loan"]=='yes',1,0)

df["y"] = np.where(df["y"]=='yes',1,0)
df1 = df[["age","balance","duration"]]
df1 = (df1 - df1.mean()) / df1.std()

X = pd.concat([
    df1,
    df_job,
    df_material,
    df_edu,
    df[["default","housing","loan"]]
],axis=1)
Y = df["y"]

from sklearn.model_selection import train_test_split
X_train,X_test,Y_train, Y_test = train_test_split(X,Y,test_size=0.3)
X1_train = X_train.drop(columns=[
    df_job.columns[0],
    df_material.columns[0],
    df_edu.columns[0]
])
X1_test = X_test.drop(columns=[
    df_job.columns[0],
    df_material.columns[0],
    df_edu.columns[0]
])

accuracy = {}
precision = {}
recall = {}
f1score = {}
roc = {}
ap = {}

#无正则项的logistic回归
name = "logistic回归(无惩罚项)"
from sklearn.linear_model import LogisticRegression
model = LogisticRegression(penalty=None)
model.fit(X1_train,Y_train)
# 用模型预测测试集
pred_test_y = model.predict(X1_test)
# 计算评价指标
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,roc_auc_score,average_precision_score
accuracy[name] = accuracy_score(Y_test,pred_test_y)
precision[name] = precision_score(Y_test,pred_test_y)
recall[name] = recall_score(Y_test,pred_test_y)
f1score[name] = f1_score(Y_test,pred_test_y)
roc[name] = roc_auc_score(Y_test,pred_test_y)
ap[name] = average_precision_score(Y_test,pred_test_y)

#带L2正则项的logistic回归
for alpha in [1,2,5,10,20]:
    name = f"logistic回归(L2 alpha={alpha})"
    from sklearn.linear_model import LogisticRegression
    model = LogisticRegression(penalty="l2",C=1/alpha)
    model.fit(X1_train,Y_train)
    # 用模型预测测试集
    pred_test_y = model.predict(X1_test)
    # 计算评价指标
    from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,roc_auc_score,average_precision_score
    accuracy[name] = accuracy_score(Y_test,pred_test_y)
    precision[name] = precision_score(Y_test,pred_test_y)
    recall[name] = recall_score(Y_test,pred_test_y)
    f1score[name] = f1_score(Y_test,pred_test_y)
    roc[name] = roc_auc_score(Y_test,pred_test_y)
    ap[name] = average_precision_score(Y_test,pred_test_y)

#带L1正则项的logistic回归
for alpha in [1,2,5,10,20]:
    name = f"logistic回归(L1 alpha={alpha})"
    from sklearn.linear_model import LogisticRegression
    model = LogisticRegression(penalty="l1",C=1/alpha, solver='liblinear')
    model.fit(X1_train,Y_train)
    # 用模型预测测试集
    pred_test_y = model.predict(X1_test)
    # 计算评价指标
    from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,roc_auc_score,average_precision_score
    accuracy[name] = accuracy_score(Y_test,pred_test_y)
    precision[name] = precision_score(Y_test,pred_test_y)
    recall[name] = recall_score(Y_test,pred_test_y)
    f1score[name] = f1_score(Y_test,pred_test_y)
    roc[name] = roc_auc_score(Y_test,pred_test_y)
    ap[name] = average_precision_score(Y_test,pred_test_y)

#支持向量机
for kernel in ['rbf','linear','poly','sigmoid']:
    name = f"支持向量机({kernel})"
    print(f"正在拟合{name}...")
    from sklearn.svm import SVC
    model = SVC(kernel=kernel, C=1000, max_iter=10000)
    model.fit(X1_train,Y_train)
    # 用模型预测测试集
    pred_test_y = model.predict(X1_test)
    # 计算评价指标
    from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,roc_auc_score,average_precision_score
    accuracy[name] = accuracy_score(Y_test,pred_test_y)
    precision[name] = precision_score(Y_test,pred_test_y)
    recall[name] = recall_score(Y_test,pred_test_y)
    f1score[name] = f1_score(Y_test,pred_test_y)
    roc[name] = roc_auc_score(Y_test,pred_test_y)
    ap[name] = average_precision_score(Y_test,pred_test_y)

#决策树
name = "决策树"
from sklearn.tree import DecisionTreeClassifier
model = DecisionTreeClassifier()
model.fit(X_train,Y_train)
# 用模型预测测试集
pred_test_y = model.predict(X_test)
# 计算评价指标
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,roc_auc_score,average_precision_score
accuracy[name] = accuracy_score(Y_test,pred_test_y)
precision[name] = precision_score(Y_test,pred_test_y)
recall[name] = recall_score(Y_test,pred_test_y)
f1score[name] = f1_score(Y_test,pred_test_y)
roc[name] = roc_auc_score(Y_test,pred_test_y)
ap[name] = average_precision_score(Y_test,pred_test_y)

# 显示各模型的评价指标
rt = pd.DataFrame({'accuracy':accuracy,
                   'precision':precision,
                   'recall':recall,
                   'f1-score':f1score,
                   'roc-auc':roc,
                   'ap':ap})
print(rt.round(4))