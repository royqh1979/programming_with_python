import pandas as pd
import numpy as np

np.random.seed(20)
#读取数据
df = pd.read_csv("energydata.csv",index_col = 0)


X = df.drop(columns="Appliances")
Y = df["Appliances"]

#划分训练集和测试集
from sklearn.model_selection import train_test_split
X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.3)

#建立预处理pipeline
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
preprocessor = Pipeline([
    ('scale',StandardScaler())
])

r2 = {}
mse = {}
mae = {}
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
def calc_metrics(model_name, model):
    print(f"正在训练{model_name}")
    ## 训练模型
    pipeline = Pipeline(
        [
            ('prep',preprocessor),
            ('model',model)
        ]
    )
    pipeline.fit(X_train,Y_train)
    # 用模型预测测试集
    pred_test_y = pipeline.predict(X_test)
    # 计算模型的R2、MSE和MAE指标
    r2[model_name] = r2_score(Y_test,pred_test_y)
    mse[model_name] = mean_squared_error(Y_test,pred_test_y)
    mae[model_name] = mean_absolute_error(Y_test,pred_test_y)

# 线性回归
## 训练模型
from sklearn.linear_model import LinearRegression
calc_metrics("线性回归", LinearRegression())

#脊回归(尝试不同alpha值）
from sklearn.linear_model import Ridge
for alpha in [0.1,0.5,1,2,4,8,10]:
    calc_metrics(f"Ridge(alpha={alpha})", Ridge(alpha=alpha))

#Lasso回归(尝试不同alpha值）
from sklearn.linear_model import Lasso
for alpha in [0.005,0.01,0.02,0.04]:
    calc_metrics(f"Lasso(alpha={alpha})", Lasso(alpha=alpha))

# 回归决策树
from sklearn.tree import DecisionTreeRegressor
calc_metrics(f"回归决策树", DecisionTreeRegressor())


# 显示各模型的评价指标
rt = pd.DataFrame({'r2':r2,'mse':mse,'mae':mae})
print(rt)