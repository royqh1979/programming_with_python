import pandas as pd
import numpy as np

np.random.seed(300)
#读取数据
df = pd.read_csv("diamonds-price.csv")
X = df[["carat","depth","table","x","y","z","cut","color","clarity"]]
Y = df["price"]

#划分训练集和测试集
from sklearn.model_selection import train_test_split
X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.3)

#建立预处理Pipeline
from sklearn.pipeline import Pipeline
#对分类变量进行独热编码
# 回归模型k-1独热编码
# 决策树用k独热编码
from sklearn.preprocessing import OneHotEncoder
nominal_encoder = OneHotEncoder(drop='first')
nominal_pipeline_for_tree = OneHotEncoder()

# 数值型变量要做标准化处理
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()

#按照列名组合预处理
from sklearn.compose import ColumnTransformer
preprocessor = ColumnTransformer([
    ('num',scaler,["carat","depth","table","x","y","z"]),
    ('nominal', nominal_encoder,["cut","color","clarity"])
])
preprocessor_tree = ColumnTransformer([
    ('num',scaler,["carat","depth","table","x","y","z"]),
    ('nominal', nominal_pipeline_for_tree,["cut","color","clarity"])
])

r2 = {}
mse = {}
mae = {}
name = "Linear Regression"

# 线性回归
## 训练模型
from sklearn.linear_model import LinearRegression
pipeline = Pipeline(
    [
        ('prep',preprocessor),
        ('model',LinearRegression())
    ]
)
pipeline.fit(X_train,Y_train)
# 用模型预测测试集
pred_test_y = pipeline.predict(X_test)
# 计算模型的R2、MSE和MAE指标
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
r2[name] = r2_score(Y_test,pred_test_y)
mse[name] = mean_squared_error(Y_test,pred_test_y)
mae[name] = mean_absolute_error(Y_test,pred_test_y)

#脊回归(尝试不同alpha值）
from sklearn.linear_model import Ridge
for alpha in [0.1,0.5,1,2,4,8,10]:
    #训练模型
    pipeline = Pipeline(
        [
            ('prep', preprocessor),
            ('model', Ridge(alpha=alpha))
        ]
    )
    pipeline.fit(X_train, Y_train)
    # 用模型预测测试集
    pred_test_y = pipeline.predict(X_test)
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
    pipeline = Pipeline(
        [
            ('prep', preprocessor),
            ('model', Lasso(alpha=alpha))
        ]
    )
    pipeline.fit(X_train, Y_train)
    # 用模型预测测试集
    pred_test_y = pipeline.predict(X_test)
    # 计算模型的R2、MSE和MAE指标
    name = f"Lasso(alpha={alpha})"
    r2[name] = r2_score(Y_test,pred_test_y)
    mse[name] = mean_squared_error(Y_test,pred_test_y)
    mae[name] = mean_absolute_error(Y_test,pred_test_y)

# 回归决策树(k-1独热码)
from sklearn.tree import DecisionTreeRegressor
# 训练模型
pipeline = Pipeline(
    [
        ('prep', preprocessor),
        ('model', DecisionTreeRegressor())
    ]
)
pipeline.fit(X_train, Y_train)
# 用模型预测测试集
pred_test_y = pipeline.predict(X_test)
# 计算模型的R2、MSE和MAE指标
name = "决策树(k-1独热码)"
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
r2[name] = r2_score(Y_test,pred_test_y)
mse[name] = mean_squared_error(Y_test,pred_test_y)
mae[name] = mean_absolute_error(Y_test,pred_test_y)

# 回归决策树(k独热码)
from sklearn.tree import DecisionTreeRegressor

pipeline = Pipeline(
    [
        ('prep', preprocessor_tree),
        ('model', Ridge(alpha=alpha))
    ]
)
pipeline.fit(X_train, Y_train)
# 用模型预测测试集
pred_test_y = pipeline.predict(X_test)
# 计算模型的R2、MSE和MAE指标
name = "决策树(k独热码)"
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
r2[name] = r2_score(Y_test,pred_test_y)
mse[name] = mean_squared_error(Y_test,pred_test_y)
mae[name] = mean_absolute_error(Y_test,pred_test_y)

# 显示各模型的评价指标
rt = pd.DataFrame({'r2':r2,'mse':mse,'mae':mae})
print(rt.round(6))