import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Create dataset
dataset_dict = {
    'Outlook': ['sunny', 'sunny', 'overcast', 'rain', 'rain', 'rain', 'overcast', 'sunny', 'sunny', 'rain', 'sunny', 'overcast', 'overcast', 'rain', 'sunny', 'overcast', 'rain', 'sunny', 'sunny', 'rain', 'overcast', 'rain', 'sunny', 'overcast', 'sunny', 'overcast', 'rain', 'overcast'],
    'Temperature': [85.0, 80.0, 83.0, 70.0, 68.0, 65.0, 64.0, 72.0, 69.0, 75.0, 75.0, 72.0, 81.0, 71.0, 81.0, 74.0, 76.0, 78.0, 82.0, 67.0, 85.0, 73.0, 88.0, 77.0, 79.0, 80.0, 66.0, 84.0],
    'Humidity': [85.0, 90.0, 78.0, 96.0, 80.0, 70.0, 65.0, 95.0, 70.0, 80.0, 70.0, 90.0, 75.0, 80.0, 88.0, 92.0, 85.0, 75.0, 92.0, 90.0, 85.0, 88.0, 65.0, 70.0, 60.0, 95.0, 70.0, 78.0],
    'Wind': [False, True, False, False, False, True, True, False, False, False, True, True, False, True, True, False, False, True, False, True, True, False, True, False, False, True, False, False],
    'Num_Players': [52, 39, 43, 37, 28, 19, 43, 47, 56, 33, 49, 23, 42, 13, 33, 29, 25, 51, 41, 14, 34, 29, 49, 36, 57, 21, 23, 41]
}

df = pd.DataFrame(dataset_dict)

# One-hot encode 'Outlook' column
df = pd.get_dummies(df, columns=['Outlook'],prefix='',prefix_sep='')

# Convert 'Wind' column to binary
df['Wind'] = df['Wind'].astype(int)

# Rearrange columns
column_order = ['sunny', 'overcast', 'rain', 'Temperature', 'Humidity', 'Wind', 'Num_Players']
df = df[column_order]

# Split features and target
X = df.drop('Num_Players', axis=1)
Y = df['Num_Players']
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, train_size=0.5, shuffle=False)

from sklearn.ensemble import GradientBoostingRegressor
print(f"正在训练 GDBT 模型...")
## 训练模型
model = GradientBoostingRegressor()
model.fit(X_train,Y_train)
# 用模型预测测试集
pred_test_y = model.predict(X_test)
# 计算模型的R2、MSE和MAE指标
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
print("r2: ",r2_score(Y_test,pred_test_y))
print("mse: ",mean_squared_error(Y_test,pred_test_y))
print("mae: ",mean_absolute_error(Y_test,pred_test_y))
print("Feature importance:")
importance = pd.Series(model.feature_importances_, index=X.columns)
importance = importance.sort_values(ascending=False)
print(importance)

from sklearn.tree import plot_tree
count=0
for estimator in model.estimators_:
    count+=1
    if count>3:
        break
    fig, ax = plt.subplots(1,1)
    plot_tree(estimator[0],max_depth=3, filled=True, impurity=False,ax=ax,fontsize=14)
    fig.tight_layout()
plt.show()
