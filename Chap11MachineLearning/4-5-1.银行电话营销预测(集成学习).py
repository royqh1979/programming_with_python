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

def calc_metrics(module_name, module):
    print(f"正在训练 {module_name} ...")
    # 训练模型
    pipeline = Pipeline([
        ('prep', preprocessor),
        ('model', module)
    ])
    pipeline.fit(X_train, Y_train)
    # 用模型预测测试集
    pred_test_y = pipeline.predict(X_test)
    # 计算评价指标
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, \
        average_precision_score
    accuracy[module_name] = accuracy_score(Y_test, pred_test_y)
    precision[module_name] = precision_score(Y_test, pred_test_y)
    recall[module_name] = recall_score(Y_test, pred_test_y)
    f1score[module_name] = f1_score(Y_test, pred_test_y)
    roc[module_name] = roc_auc_score(Y_test, pred_test_y)
    ap[module_name] = average_precision_score(Y_test, pred_test_y)


#无正则项的logistic回归
name = "logistic回归(无惩罚项)"
from sklearn.linear_model import LogisticRegression
calc_metrics("logistic回归(无惩罚项)", LogisticRegression(penalty=None))

#决策树
from sklearn.tree import DecisionTreeClassifier
calc_metrics("决策树", DecisionTreeClassifier())

#随机森林
from sklearn.ensemble import RandomForestClassifier
calc_metrics("随机森林", RandomForestClassifier())

#GBDT
from sklearn.ensemble import GradientBoostingClassifier
calc_metrics("GBDT", GradientBoostingClassifier())

# 显示各模型的评价指标
rt = pd.DataFrame({'accuracy':accuracy,
                   'precision':precision,
                   'recall':recall,
                   'f1-score':f1score,
                   'roc-auc':roc,
                   'ap':ap})
print(rt.round(4))