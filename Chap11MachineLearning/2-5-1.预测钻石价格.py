import pandas as pd
import numpy as np

np.random.seed(300)
#读取数据
df = pd.read_csv("diamonds-price.csv")

#对分类变量做独热编码
df_cut = pd.get_dummies(df["cut"], drop_first=True).astype(np.int64)
df_color = pd.get_dummies(df["color"], drop_first=True).astype(np.int64)
df_clarity = pd.get_dummies(df["clarity"], drop_first=True).astype(np.int64)
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

r2 = {}
mse = {}
mae = {}
name = "Linear Regression"

# 线性回归
## 训练模型
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train,Y_train)
# 用模型预测测试集
pred_test_y = model.predict(X_test)
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
    model.fit(X_train,Y_train)
    # 用模型预测测试集
    pred_test_y = model.predict(X_test)
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
    model.fit(X_train,Y_train)
    # 用模型预测测试集
    pred_test_y = model.predict(X_test)
    # 计算模型的R2、MSE和MAE指标
    name = f"Lasso(alpha={alpha})"
    r2[name] = r2_score(Y_test,pred_test_y)
    mse[name] = mean_squared_error(Y_test,pred_test_y)
    mae[name] = mean_absolute_error(Y_test,pred_test_y)

# 回归决策树
from sklearn.tree import DecisionTreeRegressor
# 训练模型
model = DecisionTreeRegressor()
model.fit(X_train,Y_train)
# 用模型预测测试集
pred_test_y = model.predict(X_test)
# 计算模型的R2、MSE和MAE指标
name = "Decision Tree"
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
r2[name] = r2_score(Y_test,pred_test_y)
mse[name] = mean_squared_error(Y_test,pred_test_y)
mae[name] = mean_absolute_error(Y_test,pred_test_y)

# 显示各模型的评价指标
rt = pd.DataFrame({'r2':r2,'mse':mse,'mae':mae})
print(rt)