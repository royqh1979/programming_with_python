import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import  metrics
from sklearn.model_selection import cross_validate,GridSearchCV

import matplotlib.pylab as plt

import pandas as pd

GBDT=pd.read_csv("G:/GBDT.csv")
train=GBDT

GBDT.head()
# 设置以下属性，保证dataframe各列能全部输出
pd.set_option('display.width',400)
pd.set_option('display.max_column',20)
pd.set_option('display.max_colwidth',100)

GBDT['PerpetratorRace']=GBDT['PerpetratorRace'].astype('str')
print(pd.get_dummies(GBDT).head(10))
# target='Relationship'
# train = train[~ train['PerpetratorAge'].isna()]
# x_columns = [x for x in train.columns if x not in [target]]
# # for x in train.columns:
# #     col = train[x]
# #     t=np.count_nonzero(col.isna())
# #     print(f"{x} {t}")
# X = train[x_columns]
# y = train[target]
#
# print("开始训练：")
# gbm0 = GradientBoostingClassifier(verbose=1)
# gbm0.fit(X,y)
# print(f"特征数:{gbm0.n_features_}")
#
# y_pred = gbm0.predict(X)
# y_predprob = gbm0.predict_proba(X)[:,1]
# print("Accuracy : %.4g" % metrics.accuracy_score(y.values, y_pred))
# print("Precision : %.4g" % metrics.precision_score(y.values, y_pred))
# print("Recall : %.4g" % metrics.recall_score(y.values, y_pred))
# print("AUC Score (Train): %f" % metrics.roc_auc_score(y, y_predprob))
#
# import pickle
# with open('g:/clf.pickle', 'wb') as f:
#     pickle.dump(gbm0, f)
#
#
#
