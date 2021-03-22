import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from Colors import hillfit
from scipy.optimize import  curve_fit

colors= {'BW25113':'gray', '∆TolC':'olivedrab'}
df=pd.read_excel('2019-09-14-WT-dTolC-TMP-V041.xlsx','BgSubtracted')
df1=df.loc[~(df.Replica=='B'), :]
fig, ax = plt.subplots(4,7)
sns.set_style('ticks')
sns.despine()
x=df1.columns[3:-1].values
xfit=np.logspace(np.log10(min(x)),np.log10(max(x)),100)
ic50s=[]
hs=[]
mins=[]
maxs=[]
dfFitParams=df1.loc[:,['Strain','Drug','Replica']]
for i in range(len(df1)):
    cax=ax[i//len(ax[0]), i%len(ax[0])]
    y=df1.iloc[i, 3:-1]
    strain=df1.iloc[i,0]
    popt, pcov=curve_fit(hillfit, x, y, p0=[0,0,.1,1], bounds=((0,0,0.1,0),(0.1, .5, 1, 10)))
    mins.append(popt[0])
    maxs.append(popt[1])
    ic50s.append(popt[2])
    hs.append(popt[3])

    cax.semilogx(x,y,'-o',color=colors[strain])
    cax.semilogx(xfit, hillfit(xfit, *popt),'--r')
    cax.semilogx(popt[2], hillfit(popt[2],*popt), 'or')

dfFitParams['min']=mins
dfFitParams['max']=maxs
dfFitParams['IC50']=ic50s
dfFitParams['h']=hs

fig2,ax2=plt.subplots()
sns.set_style('ticks')
sns.despine()
sns.barplot(x='Drug', y='IC50', hue='Strain', data=dfFitParams, palette=['gray','olivedrab'], ax=ax2)
