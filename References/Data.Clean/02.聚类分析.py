import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import matplotlib as mpl

# matplotlib 使用中文字体显示内容
font_name = "STKaiti"
mpl.rcParams['font.family']=font_name
mpl.rcParams['axes.unicode_minus']=False # in case minus sign is shown as box

datafile = 'data_cleaned.csv'

print("正在读取……")
data = pd.read_csv(datafile,encoding="UTF-8")
print("读取完毕")
print(data.columns)

class_count = 5
cpu_count = 4
kmodel = KMeans(n_clusters=class_count, n_jobs=cpu_count)
print("开始训练……")
kmodel.fit(data) #训练模型

print("训练完成")
centers = pd.DataFrame(kmodel.cluster_centers_,columns=data.columns)
print(centers)

data["class_label"]=kmodel.labels_
print(data.head(10))


# 归一化以便比较
centers_max=centers.max(axis=0)
centers_min=centers.min(axis=0)
centers = (centers - centers_min) / (centers_max - centers_min)
centers.plot.bar()
plt.show()