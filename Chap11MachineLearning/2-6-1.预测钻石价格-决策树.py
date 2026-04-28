import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(300)
#读取数据
df = pd.read_csv("diamonds-price.csv")
cut_first_column = df["cut"].unique()[0]
color_first_column = df["color"].unique()[0]
clarity_first_column = df["clarity"].unique()[0]
#对分类变量做k独热编码，因为决策树需要
# 回归模型需要k-1独热码，后面手工去除第一列
df_cut = pd.get_dummies(df["cut"]).astype(np.int64)
df_color = pd.get_dummies(df["color"]).astype(np.int64)
df_clarity = pd.get_dummies(df["clarity"]).astype(np.int64)
#对数值型变量做标准化处理
df1 = df[["carat","depth","table","x","y","z"]]
df1 = (df1 - df1.mean())/df1.std()
# 整合自变量和因变量
X = pd.concat([df1,
              df_cut,
              df_color,
              df_clarity],axis=1)
Y = df["price"]
Y = (Y-Y.mean())/Y.std()
print(X)

#划分训练集和测试集
from sklearn.model_selection import train_test_split
X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.3)


from sklearn.tree import DecisionTreeRegressor
print(f"正在训练 决策树 模型...")
## 训练模型
model = DecisionTreeRegressor()
model.fit(X_train,Y_train)
# 用模型预测测试集
pred_test_y = model.predict(X_test)
# 计算模型的R2、MSE和MAE指标
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
print("r2: ",r2_score(Y_test,pred_test_y))
print("mse: ",mean_squared_error(Y_test,pred_test_y))
print("mae: ",mean_absolute_error(Y_test,pred_test_y))

#绘制决策树
from sklearn.tree import plot_tree
plt.figure(figsize=(20,10))
plot_tree(model,max_depth=3,filled=True,fontsize=18,feature_names=X_train.columns)
plt.show()