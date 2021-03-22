import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from findICx import hillfit3p
from scipy.optimize import  curve_fit
df=pd.read_csv('PivotedData2.csv').set_index(['MutantName','ExperimentDate','Drug'])
df.columns=[float(i) for i in df.columns]
dfParams=pd.DataFrame([],index=df.index)
mxs=np.empty(len(df))*np.nan
ics=np.empty(len(df))*np.nan
hs=np.empty(len(df))*np.nan
for i in range(len(df)):
    xy=df.iloc[i,:].dropna()
    x=xy.index
    y=xy.values
    try:
        popt, pcov = curve_fit(hillfit3p,x,y,bounds=((0,0.1,0.1),(1,15000,10)))
        mxs[i]=popt[0]
        ics[i]=popt[1]
        hs[i]=popt[2]
        print(i, df.iloc[i,:].index,popt)
    except:
        continue
dfParams['maxOD']=mxs
dfParams['ic50']=ics
dfParams['hs']=hs
