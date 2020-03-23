import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import statsmodels.formula.api as sm
from sklearn import metrics

df=pd.read_csv("prostate.data",sep="\t",index_col=0)

train = df[df['train']=='T']
test = df[df['train']=='F']

model=sm.ols("lpsa ~ lcavol+lweight+age+lbph+svi+lcp+gleason+pgg45",data=df).fit()
summary = model.summary()
print(summary)


prediction = model.get_prediction(test)
print(prediction.summary_frame(alpha=0.01))
y = test['lpsa']
y_pred=prediction.predicted_mean
print(f"MSE : {metrics.mean_squared_error(y,y_pred) :.4f}")

