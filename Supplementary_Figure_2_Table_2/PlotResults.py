from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.optimize import curve_fit
from findICx import hillfit3p

# def fitHill(inp):
#     x=inp.index.values
#     y=inp.values
#     popt, pcov=curve_fit(hillfit, x, y, bounds=((0,0,0,0),(.1,1,10000,10)))
#     return popt[0],popt[1],popt[2],popt[3]
names=pd.read_csv('PlateMapList.csv')
df=pd.read_excel('CombinedData.xlsx', 'BgSubtracted')
df.set_index(['Drug','Concentration','ExperimentDate'],inplace=True)
df.columns=names['MutantName'].values

df=df.stack().reset_index()
df.columns=['Drug','Concentration','ExperimentDate','MutantName','OD']
df=df.loc[~df.MutantName.isnull(), :]
df=df.set_index(['MutantName','ExperimentDate','Drug']).pivot(columns='Concentration')
df.columns=[s[1] for s in df.columns.values]
df.to_csv('PivotedData.csv')

df=df.loc[df[0.05]>0,:]
maxODs=np.empty((len(df),1))*np.nan
hs=np.empty((len(df),1))*np.nan
ics=np.empty((len(df),1))*np.nan
x=df.columns
for i in range(len(df)):
    y=df.iloc[i,:]
    try:
        popt, pcov=curve_fit(hillfit3p, x, y, bounds=((0,0.1,0),(.85, 15000, 10)))
        print(i, popt)
        maxODs[i]=popt[0]
        ics[i]=popt[1]
        hs[i]=popt[2]
    except:
        continue

df['maxOD']=maxODs
df['IC50']=ics
df['h']=hs