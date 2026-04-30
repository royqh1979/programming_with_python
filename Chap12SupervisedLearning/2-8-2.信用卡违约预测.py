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
roc_curve_data = {}
ap = {}
pr_curve_data = {}

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, \
    average_precision_score, roc_curve, precision_recall_curve

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
    roc_curve_data[model_name] = roc_curve(Y_test, pred_test_y)
    pr_curve_data[model_name] = precision_recall_curve(Y_test, pred_test_y)

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
# from sklearn.svm import SVC
# for kernel in ['rbf','linear','poly','sigmoid']:
#     calc_metrics(f"支持向量机({kernel})", SVC(kernel=kernel, C=1, max_iter=10000))

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

import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['font.family']=['Microsoft Yahei', 'sans-serif']
mpl.rcParams['axes.unicode_minus']=False

for name in roc_curve_data:
    plt.plot(roc_curve_data[name][0],roc_curve_data[name][1], label=name)
plt.legend()
plt.title("ROC曲线")
plt.show()

for name in pr_curve_data:
    plt.plot(pr_curve_data[name][1],pr_curve_data[name][0], label=name)
plt.legend()
plt.title("P-R曲线")
plt.show()


