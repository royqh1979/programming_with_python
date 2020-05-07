import pandas as pd
import numpy as np

datafile='datas/air_data.csv'
cleanedfile = 'data_cleaned.csv'

data = pd.read_csv(datafile,encoding="UTF-8")

# 数据清洗（去除含缺失值数据）
print(f"共有{len(data)}条数据")
data = data[data['SUM_YR_1'].notnull() & data['SUM_YR_2'].notnull()]

print(f"共有{len(data)}条数据")
SUM_YR_1 = data['SUM_YR_1'] #第一年总票价
SUM_YR_2 = data['SUM_YR_2'] #第二年总票价
SEG_KM_SUM = data['SEG_KM_SUM'] #总飞行公里数
AVG_Discount = data['avg_discount'] #平均折扣率

data = data[(SUM_YR_1 !=0) | (SUM_YR_2 != 0) | ((SEG_KM_SUM!=0) & (AVG_Discount != 0))]

print(f"共有{len(data)}条数据")


#属性规约（筛选列，只保留分析用到的）

data = data[['LOAD_TIME','FFP_DATE','LAST_TO_END','FLIGHT_COUNT','SEG_KM_SUM','avg_discount']]

print(data.head(10)) # 显示头部10条数据

#数据变换（属性构造）
# 根据已有信息，计算出LRFMC五个指标
# 1. L = LOAD_TIME - FFP_DATE
# 入会时间（单位：月） = 研究截止时间 - 入会时间
# 2. R = LAST_TO_END
# 会员最近一次乘坐航班到现在的时间（单位：月）
# 3. F = FLIGHT_COUNT
# 会员乘坐航班次数
# 4. M = SEG_KM_SUM
# 会员累计飞行里程
# 5. C = avg_discount
# 会员平均折扣数

# 因为LOAD_TIME和FFP_DATE列都是字符串，所以需要先转换为日期
data['LOAD_TIME'] = pd.to_datetime(data['LOAD_TIME'])
data['FFP_DATE'] = pd.to_datetime(data['FFP_DATE'])
#计算出相差天数
tmp = data['LOAD_TIME'] - data['FFP_DATE']
# 转换为相差月份
tmp = tmp // np.timedelta64(1,'M')
data["入会时间L"]=tmp
#剩下四列直接改名即可
data.rename(columns={'LAST_TO_END':'最近一次乘坐航班时间R',
                     'FLIGHT_COUNT':'乘坐航班次数F',
                     'SEG_KM_SUM':'累计飞行里程M',
                     'avg_discount':'平均折扣数C'},inplace = True)
#去除不需要的列
data.drop(columns=['LOAD_TIME','FFP_DATE'],inplace=True)

print("转换后数据")
print(data.head(10))

print("各列最大值:")
print(data.max(axis=0))
print("各列最小值:")
print(data.min(axis=0))
print("各列均值:")
print(data.mean(axis=0))
print("各列标准差:")
print(data.std(axis=0))
print("各列偏度：")
print(data.skew(axis=0))



# 数据归一化（转化为[0，1]区间上的值）
# data_max=data.max(axis=0)
# data_min=data.min(axis=0)
# data = (data-data_min)/(data_max-data_min)

# 用标准正态分布转换数据
data_mean=data.mean(axis=0)
data_std=data.std(axis=0)
data = (data-data_mean)/data_std


print(data.head(10))


print(f"正在写入..")

data.to_csv(cleanedfile,encoding="UTF-8",index=False)
# data.to_excel(cleanedfile)
print(f"写入完成")
