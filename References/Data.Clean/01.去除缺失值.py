import pandas as pd
import numpy as np

datafile='datas/air_data.csv'
cleanedfile = 'data_cleaned.xls'

data = pd.read_csv(datafile,encoding="UTF-8")

# 数据清洗（去除含缺失值数据）
print(f"共有{len(data)}条数据")
data = data[data['SUM_YR_1'].notnull() & data['SUM_YR_2'].notnull()]

print(f"共有{len(data)}条数据")
SUM_YR_1 = data['SUM_YR_1'] #第一年总票价
SUM_YR_2 = data['SUM_YR_2'] #第二年总票价
SEG_KM_SUM = data['SEG_KM_SUM'] #总飞行公里数
AVG_Discount = data['avg_discount'] #平均折扣率

data = data[(SUM_YR_1 !=0) | (SUM_YR_2 != 0) | ((SEG_KM_SUM==0) & (AVG_Discount == 0))]

print(f"共有{len(data)}条数据")


#属性规约（筛选列，只保留分析用到的）

data = data[['LOAD_TIME','FFP_DATE','LAST_TO_END','FLIGHT_COUNT','SEG_KM_SUM','avg_discount']]

print(data.head(10)) # 显示头部10条数据

#数据变换（属性构造）
# 根据已有信息，计算出LRFMC五个指标
# 1. L = LOAD_TIME - FFP_DATE
# 入会时间长短（单位：月） = 研究截止时间 - 入会时间
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
#计算出相差月份
data["L"] = data['LOAD_TIME'].dt.to_period('M') - data['FFP_DATE'].dt.to_period('M')

#剩下四列直接改名即可
data.rename(columns={'LAST_TO_END':'R',
                     'FLIGHT_COUNT':'F',
                     'SEG_KM_SUM':'M',
                     'avg_discount':'C'},inplace = True)
#去除不需要的列
data.drop(columns=['LOAD_TIME','FFP_DATE'],inplace=True)


print(data.head(10))
# print(f"正在写入..")
#
# data.to_csv(cleanedfile,encoding="UTF-8")
# # data.to_excel(cleanedfile)
# print(f"写入完成")
