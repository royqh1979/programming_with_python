import matplotlib.pyplot as plt
import matplotlib as mpl

#使用中文字体
mpl.rcParams['font.family']=['Microsoft Yahei','sans-serif']
mpl.rcParams['axes.unicode_minus']=False

#导入数据
import pandas as pd
df = pd.read_csv("housing.csv")
df = df[["latitude", "longitude"]]
print(df)

#K均值聚类
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=6)
df["Cluster"] = kmeans.fit_predict(df)
df["Cluster"] = df["Cluster"].astype("category")

# 各组质心
centers = pd.DataFrame(
    data=kmeans.cluster_centers_,
    columns=["latitude", "longitude"]
)
print("各组质心：")
print(centers)

#绘制散点图
import seaborn as sns
sns.relplot(
    x="longitude", y="latitude", hue="Cluster", data=df, height=6,
)
plt.scatter(x="longitude", y="latitude", color="black", data=centers)
plt.show()


