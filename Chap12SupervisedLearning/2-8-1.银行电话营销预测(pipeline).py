import pandas as pd
import numpy as np

np.random.seed(42)
df = pd.read_csv("bank.csv")

Y = np.where(df["y"]=='yes',1,0)
X = df[["job","marital","education","default","housing","loan", "age","balance","duration"]]
from sklearn.model_selection import train_test_split
X_train,X_test,Y_train, Y_test = train_test_split(X,Y,test_size=0.3)

#构造预处理pipeline
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.compose import ColumnTransformer
preprocessor = ColumnTransformer([
    ('num',StandardScaler(),["age","balance","duration"]),
    ('nominal', OneHotEncoder(drop="first"),["job","marital","education","default","housing","loan"])
])

accuracy = {}
precision = {}
recall = {}
f1score = {}
roc = {}
ap = {}

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, \
    average_precision_score

def calc_metrics(model_name, model):
    print(f"正在拟合 {model_name} ...")
    pipeline = Pipeline([
        ('prep', preprocessor),
        ('model', model)
    ])
    pipeline.fit(X_train, Y_train)
    # 用模型预测测试集
    pred_test_y = pipeline.predict(X_test)
    # 计算评价指标
    accuracy[model_name] = accuracy_score(Y_test, pred_test_y)
    precision[model_name] = precision_score(Y_test, pred_test_y)
    recall[model_name] = recall_score(Y_test, pred_test_y)
    f1score[model_name] = f1_score(Y_test, pred_test_y)
    roc[model_name] = roc_auc_score(Y_test, pred_test_y)
    ap[model_name] = average_precision_score(Y_test, pred_test_y)

#无正则项的logistic回归
from sklearn.linear_model import LogisticRegression
calc_metrics("logistic回归(无惩罚项)", LogisticRegression(penalty=None))

#带L2正则项的logistic回归
from sklearn.linear_model import LogisticRegression
for alpha in [1,2,5,10,20]:
    calc_metrics(f"logistic回归(L2 alpha={alpha})", LogisticRegression(penalty="l2",C=1/alpha))

#带L1正则项的logistic回归
for alpha in [1,2,5,10,20]:
    calc_metrics(f"logistic回归(L1 alpha={alpha})", LogisticRegression(penalty="l1",C=1/alpha, solver='liblinear'))

#支持向量机
from sklearn.svm import SVC
for kernel in ['rbf','linear','poly','sigmoid']:
    calc_metrics(f"支持向量机({kernel})", SVC(kernel=kernel, C=1, max_iter=10000))

#决策树
from sklearn.tree import DecisionTreeClassifier
calc_metrics("决策树", DecisionTreeClassifier())

# 显示各模型的评价指标
rt = pd.DataFrame({'accuracy':accuracy,
                   'precision':precision,
                   'recall':recall,
                   'f1-score':f1score,
                   'roc-auc':roc,
                   'ap':ap})
print(rt.round(4))