import numpy as np
#读入数据
values = np.loadtxt("UCI Online Retail.csv",skiprows=1,usecols=[0,1,2], delimiter=',')
dates = np.loadtxt("UCI Online Retail.csv",skiprows=1,usecols=[3], delimiter=',',dtype=np.datetime64)
ids= values[:,0].astype(np.int64)
quantities = values[:,1]
price = values[:,2]
amounts = quantities * price

#计算原始RFM值
uniq_ids = np.unique(ids)
R = np.zeros(len(uniq_ids))
M = np.zeros(len(uniq_ids))
F = np.zeros(len(uniq_ids))
for i,uid in enumerate(uniq_ids):
    filtered_amounts = amounts[ ids == uid ]
    filtered_dates = dates[ ids == uid ]
    R[i] = np.max(dates)-np.max(filtered_dates)
    M[i] = np.sum(filtered_amounts)
    F[i] = len(filtered_amounts[filtered_amounts>0]) - len(filtered_amounts[filtered_amounts<0])

#分别将R、F、M按照前5%,前10%,前20%，前40%的比例转换成1-5的评分
def score_by_percentile(data):
    bins=[5, 10, 20, 40]
    percentiles = np.percentile(data, bins)  # [P5, P10, P20, P40]
    bins_edges = [-np.inf] + list(percentiles) + [np.inf]
    scores = np.digitize(data, bins_edges, right=True)
    return scores

R = score_by_percentile(R)
F = score_by_percentile(F)
M = score_by_percentile(M)

for id,r,f,m in zip(uniq_ids,R,F,M):
    print(id,r,f,m)