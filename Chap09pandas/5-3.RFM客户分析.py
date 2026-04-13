import pandas as pd
#读入数据

data = pd.read_csv("UCI Online Retail.csv", index_col=0)
# 删除有缺失项的数据
data = data.dropna()

# 将客户ID转换为整数型（默认为浮点型）
data["CustomerID"] = data["CustomerID"].astype("int64")
# 将日期转换为日期型
data["InvoiceDate"] = pd.to_datetime(data["InvoiceDate"])
# 计算总金额
data["amounts"] = data["Quantity"] * data["UnitPrice"]

#计算RFM值
d1 = data[data["Quantity"]>0]
d2 = data[data["Quantity"]<0]
rfm  = pd.DataFrame()
rfm["R"] = data["InvoiceDate"].max() - d1.groupby("CustomerID")["InvoiceDate"].max()
rfm["R"] = rfm["R"].dt.days
rfm["M"] = data.groupby("CustomerID")["amounts"].sum()
rfm["F"] = d1.groupby("CustomerID")["amounts"].count().sub(d2.groupby("CustomerID")["amounts"].count(),fill_value=0)

#分别将R、F、M按照前5%,前10%,前20%，前40%的比例转换成1-5的评分
rfm["R"] = pd.cut(
    rfm["R"],
    rfm["R"].quantile([0,0.05,0.1,0.2,0.4,1]),
    labels=[1,2,3,4,5],
    include_lowest=True,
    right=True
)
rfm["F"] = pd.cut(
    rfm["F"],
    rfm["F"].quantile([0,0.6,0.8,0.9,0.95,1]),
    labels=[1,2,3,4,5],
    include_lowest=True,
    right=True
)
rfm["M"] = pd.cut(
    rfm["M"],
    rfm["M"].quantile([0,0.6,0.8,0.9,0.95,1]),
    labels=[1,2,3,4,5],
    include_lowest=True,
    right=True
)
print(rfm)