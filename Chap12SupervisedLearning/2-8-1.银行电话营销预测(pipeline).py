import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#使用中文字体
from pylab import mpl
mpl.rcParams['font.sans-serif']="Simsun"
mpl.rcParams['axes.unicode_minus']=False

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
pr_curve_data  = {}
roc_curve_data = {}

from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,roc_auc_score,average_precision_score, precision_recall_curve, roc_curve
def test_model(model_name, model):
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
    pr_curve_data[model_name] = precision_recall_curve(Y_test,pred_test_y)
    roc_curve_data[model_name] = roc_curve(Y_test,pred_test_y)

#无正则项的logistic回归
from sklearn.linear_model import LogisticRegression
test_model("logistic回归(无惩罚项)", LogisticRegression(penalty=None))

#带L2正则项的logistic回归
from sklearn.linear_model import LogisticRegression
for alpha in [1,2,5,10,20]:
    test_model(f"logistic回归(L2 alpha={alpha})", LogisticRegression(penalty="l2", C=1 / alpha))

#带L1正则项的logistic回归
for alpha in [1,2,5,10,20]:
    test_model(f"logistic回归(L1 alpha={alpha})", LogisticRegression(penalty="l1", C=1 / alpha, solver='liblinear'))

#支持向量机
from sklearn.svm import SVC
for kernel in ['rbf','linear','poly','sigmoid']:
    test_model(f"支持向量机({kernel})", SVC(kernel=kernel, C=1, max_iter=10000))

#决策树
from sklearn.tree import DecisionTreeClassifier
test_model("决策树", DecisionTreeClassifier())

# 显示各模型的评价指标
rt = pd.DataFrame({'accuracy':accuracy,
                   'precision':precision,
                   'recall':recall,
                   'f1-score':f1score,
                   'roc-auc':roc,
                   'ap':ap})
print(rt.round(4))

#绘制roc曲线
fig, ax = plt.subplots(1,1)
for name in roc_curve_data.keys():
    ax.plot(roc_curve_data[name][0],roc_curve_data[name][1], label=name)
ax.set_title("ROC曲线")
ax.legend(fontsize=14)
ax.set_xlim(0,1)
ax.set_ylim(0,1)
fig.tight_layout()

#绘制pr曲线
fig, ax = plt.subplots(1,1)
for name in roc_curve_data.keys():
    ax.plot(pr_curve_data[name][1],pr_curve_data[name][0], label=name)
ax.legend(fontsize=14)
ax.set_title("PR曲线",fontsize=18)
ax.set_xlim(0,1)
ax.set_ylim(0,1)
fig.tight_layout()
plt.show()