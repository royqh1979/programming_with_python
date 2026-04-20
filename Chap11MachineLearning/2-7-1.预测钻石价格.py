import pandas as pd
import numpy as np

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
# 手工去除k独热码的第一列
X1_train = X_train.drop(columns=[cut_first_column,color_first_column,clarity_first_column])
X1_test = X_test.drop(columns=[cut_first_column,color_first_column,clarity_first_column])

r2 = {}
mse = {}
mae = {}
name = "Linear Regression"

# 线性回归
## 训练模型
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X1_train,Y_train)
# 用模型预测测试集
pred_test_y = model.predict(X1_test)
# 计算模型的R2、MSE和MAE指标
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
r2[name] = r2_score(Y_test,pred_test_y)
mse[name] = mean_squared_error(Y_test,pred_test_y)
mae[name] = mean_absolute_error(Y_test,pred_test_y)

#脊回归(尝试不同alpha值）
from sklearn.linear_model import Ridge
for alpha in [0.1,0.5,1,2,4,8,10]:
    #训练模型
    model = Ridge(alpha=alpha)
    model.fit(X1_train,Y_train)
    # 用模型预测测试集
    pred_test_y = model.predict(X1_test)
    # 计算模型的R2、MSE和MAE指标
    name = f"Ridge(alpha={alpha})"
    r2[name] = r2_score(Y_test,pred_test_y)
    mse[name] = mean_squared_error(Y_test,pred_test_y)
    mae[name] = mean_absolute_error(Y_test,pred_test_y)

#Lasso回归(尝试不同alpha值）
from sklearn.linear_model import Lasso
for alpha in [0.005,0.01,0.02,0.04]:
    # 训练模型
    model = Lasso(alpha=alpha)
    model.fit(X1_train,Y_train)
    # 用模型预测测试集
    pred_test_y = model.predict(X1_test)
    # 计算模型的R2、MSE和MAE指标
    name = f"Lasso(alpha={alpha})"
    r2[name] = r2_score(Y_test,pred_test_y)
    mse[name] = mean_squared_error(Y_test,pred_test_y)
    mae[name] = mean_absolute_error(Y_test,pred_test_y)

# 回归决策树(k-1独热码)
from sklearn.tree import DecisionTreeRegressor
# 训练模型
model = DecisionTreeRegressor()
model.fit(X1_train,Y_train)
# 用模型预测测试集
pred_test_y = model.predict(X1_test)
# 计算模型的R2、MSE和MAE指标
name = "决策树(k-1独热码)"
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
r2[name] = r2_score(Y_test,pred_test_y)
mse[name] = mean_squared_error(Y_test,pred_test_y)
mae[name] = mean_absolute_error(Y_test,pred_test_y)

# 回归决策树(k独热码)
from sklearn.tree import DecisionTreeRegressor
# 训练模型
model = DecisionTreeRegressor()
model.fit(X_train,Y_train)
# 用模型预测测试集
pred_test_y = model.predict(X_test)
# 计算模型的R2、MSE和MAE指标
name = "决策树(k独热码)"
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
r2[name] = r2_score(Y_test,pred_test_y)
mse[name] = mean_squared_error(Y_test,pred_test_y)
mae[name] = mean_absolute_error(Y_test,pred_test_y)



# 显示各模型的评价指标
rt = pd.DataFrame({'r2':r2,'mse':mse,'mae':mae})
print(rt)