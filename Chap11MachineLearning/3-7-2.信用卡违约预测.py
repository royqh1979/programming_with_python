import pandas as pd
df = pd.read_csv("UCI_Credit_Card.csv", index_col=0)

Y = df["default.payment.next.month"]
X = df.drop(columns=["default.payment.next.month"])

from sklearn.model_selection import train_test_split
X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.3)

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder

pay_names = ["PAY_0"]+[ f"PAY_{x}" for x in range(2,7)]
bill_names = [f"BILL_AMT{x}" for x in range(1,7)]
pay_names2 = [ f"PAY_AMT{x}" for x in range(1,7)]
preprocessor = ColumnTransformer([
    ("num",StandardScaler(),["LIMIT_BAL","AGE"]+pay_names+bill_names+pay_names2),
    ("nominal", OneHotEncoder(drop="first"),["SEX","EDUCATION","MARRIAGE"])
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
print(f"正在拟合 {name}...")
#训练模型
pipeline = Pipeline([
    ('prep', preprocessor),
    ('model', LogisticRegression(penalty=None))
])
pipeline.fit(X_train, Y_train)
# 用模型预测测试集
pred_test_y = pipeline.predict(X_test)
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
    print(f"正在拟合 {name}...")
    from sklearn.linear_model import LogisticRegression
    pipeline = Pipeline([
        ('prep', preprocessor),
        ('model', LogisticRegression(penalty="l2",C=1/alpha))
    ])
    pipeline.fit(X_train, Y_train)
    # 用模型预测测试集
    pred_test_y = pipeline.predict(X_test)
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
    print(f"正在拟合 {name}...")
    from sklearn.linear_model import LogisticRegression
    pipeline = Pipeline([
        ('prep', preprocessor),
        ('model', LogisticRegression(penalty="l1",C=1/alpha, solver='liblinear'))
    ])
    pipeline.fit(X_train, Y_train)
    # 用模型预测测试集
    pred_test_y = pipeline.predict(X_test)
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
    pipeline = Pipeline([
        ('prep', preprocessor),
        ('model', SVC(kernel=kernel, C=1, max_iter=10000))
    ])
    pipeline.fit(X_train, Y_train)
    # 用模型预测测试集
    pred_test_y = pipeline.predict(X_test)

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
pipeline = Pipeline([
    ('prep', preprocessor),
    ('model', DecisionTreeClassifier())
])
pipeline.fit(X_train, Y_train)
# 用模型预测测试集
pred_test_y = pipeline.predict(X_test)
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
