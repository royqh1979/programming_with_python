import pandas as pd
import numpy as np

df = pd.read_csv("defection-detect.csv")

df = df.rename(columns={"Discoloration Defects":"Discoloration_Defects",
           "Hours Since Cleanse":"Hours_Since_Cleanse",
           "Size of Screw":"Size_of_Screw",
           "Clump Defects":"Clump_Defects"
           })
print(np.mean(df["Discoloration_Defects"]))
print(np.var(df["Discoloration_Defects"]))
print(df)

import statsmodels.formula.api as sm
model = sm.poisson("Discoloration_Defects ~ Hours_Since_Cleanse + Size_of_Screw + Temperature + Clump_Defects", data=df)
lm = model.fit()
print(lm.summary())

print(" ---- incident rate ratio ---- ")
import numpy as np
print(np.exp(lm.params))