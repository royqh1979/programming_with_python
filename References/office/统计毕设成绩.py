import pandas as pd

score = ('优秀','良好','中等','及格','不及格')
type = ('科研','生产','模拟','其他')
def calc(df:pd.DataFrame):
    n=len(df)
    s1=df.groupby('成绩').size()
    df1=pd.DataFrame()
    df1['人数']=s1
    df1['比例']=s1/n
    print(df1)

    s1=df.groupby('来源').size()
    df1=pd.DataFrame()
    df1['人数']=s1
    df1['比例']=s1/n
    print(df1)


filename = 'e:\\19毕设.xlsx'

df=pd.read_excel(filename)

df_ds = df[df['班级']=='电商15']
df_xg = df[df['班级']=='信管15']

print("电商：")
calc(df_ds)

print("信管：")
calc(df_xg)

