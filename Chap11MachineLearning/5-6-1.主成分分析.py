# https://www.geeksforgeeks.org/machine-learning/implementing-pca-in-python-with-scikit-learn/
import pandas as pd
import numpy as np
df =pd.read_csv("cancer.csv",index_col=0)
df = df.drop(columns=["diagnosis"])
print(df)

#标准化
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X = scaler.fit_transform(df)
print(X.shape)

from sklearn.decomposition import PCA
pca = PCA()
pca.fit(X)

print("Explained variance:", np.round(pca.explained_variance_ratio_,3))
print("Cumulative:", np.cumsum(pca.explained_variance_ratio_))
print(np.where(np.cumsum(pca.explained_variance_ratio_) > 0.9))

n = np.where(np.cumsum(pca.explained_variance_ratio_) > 0.9)[0][0]
pca = PCA(n_components=n)
X = pca.fit_transform(X)
print(X.shape)