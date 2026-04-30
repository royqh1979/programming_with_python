import pandas as pd
import numpy as np
df = pd.read_csv("house-prices.csv",index_col=0)
print(df)
X = df.drop(columns=["Price"])
Y = df["Price"]

from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
onehot = OneHotEncoder(drop="first")

from sklearn.compose import ColumnTransformer
preprocess = ColumnTransformer([
    ('num',scaler,["SqFt","Bedrooms","Bathrooms"]),
    ('nominal',onehot,["Brick","Neighborhood"])
])

from sklearn.linear_model import LinearRegression
model = LinearRegression()

from sklearn.pipeline import Pipeline
pipeline = Pipeline([
    ('prep',preprocess),
    ('model',model)
])

from sklearn.model_selection import cross_validate
csv = cross_validate(pipeline,X,Y,cv=5)
print(csv)
print("交叉评估得分(R2):",np.mean(csv['test_score']))


pipeline.fit(X,Y)
pred = pipeline.predict(X)
from sklearn.metrics import r2_score
print("完整训练集评分(R2):", r2_score(Y,pred))