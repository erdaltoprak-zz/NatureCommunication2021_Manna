import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from Colors import mw_v041, mw_tmp
# from findICx import hillfit3p
# from scipy.optimize import  curve_fit
def findIC95(concs,ODs):
    # As final decision we agreed on IC50.
    ODthr=np.maximum(ODs[0],0.1)*.05 # Calculates IC50
    ODbool=ODs<ODthr

    # if ODbool[0]==True and ODbool[1]==False:
    #     concs=concs[1:]
    #     ODbool=ODbool[1:]
    if sum(ODbool)==0:
        IC95=max(concs)+1
    else:
        IC95=min(concs[ODbool])
    print(concs, ODbool, ODs, ODthr, IC95)
    return IC95



df=pd.read_csv('PivotedData2.csv').set_index(['MutantName','ExperimentDate','Drug'])
df.columns=[float(i) for i in df.columns]
ic50s=np.empty(len(df))*np.nan
for i in range(len(df)):
    xy=df.iloc[i,:].dropna()
    x=xy.index
    y=xy.values
    ic50s[i]=findIC95(x,y)

df['IC50Cl']=ic50s
dfParams=df.loc[:,'IC50Cl']
dfParams=dfParams.reset_index()

dfP1=dfParams.groupby(['MutantName','Drug']).IC50Cl.mean()
dfP2=dfParams.groupby(['MutantName','Drug']).IC50Cl.std()

dfPP=pd.concat([dfP1, dfP2],axis=1)
dfPP.columns=['Mean','Std']
dfPP=dfPP.reset_index()
dfPP['L28Mutated']=dfPP.MutantName.apply(lambda x: (1 if 'L28R' in x else 0))
dfPP['MaxedOut']=dfPP.Mean.apply(lambda x: (1 if x>9000 else 0))
dfPP=dfPP.set_index('MutantName')
dfPP2=pd.concat([dfPP.loc[dfPP.Drug=='TMP',:],dfPP.loc[~(dfPP.Drug=='TMP'),:]],axis=1)
dfPP2.columns=['Drug','MeanT','StdT','L28RMutated','MaxedOut','Drug','MeanV','StdV','L28RMutated','MaxedOut']
dfPP2=dfPP2.iloc[:,:-2]
fig,ax=plt.subplots()
sns.set_style('ticks')
sns.despine()
labels=[['Mutants with L28','Mutants with L28,\nIC$_{95}^{TMP}$>2700'],
        ['Mutants with R28','Mutants with R28,\nIC$_{95}^{TMP}$>2700']]
colors=['dimgrey','magenta']
markers=['o','^']

for mutated in range(2):
    for maxedout in range(2):
        d=dfPP2.loc[(dfPP2.L28RMutated==mutated)&(dfPP2.MaxedOut==maxedout),:]
        x=d.MeanT.values * mw_tmp * 1e-3  #+d.MeanT.values*np.random.random(d.MeanT.values.shape)*0.1*(-1**np.random.randint(1,2,1))
        y=d.MeanV.values * mw_v041 * 1e-3 #+d.MeanV.values*np.random.random(d.MeanV.values.shape)*0.1*(-1**np.random.randint(1,2,1))
        xerr=d.StdT.values / np.sqrt(3) * mw_tmp * 1e-3
        yerr=d.StdV.values / np.sqrt(3) * mw_v041 * 1e-3
        ax.errorbar(x=x,y=y,xerr=xerr,yerr=yerr,color=colors[mutated],
                    marker=markers[maxedout], linestyle='',
                    capsize=2,alpha=.5,linewidth=1,
                    label=labels[mutated][maxedout])

ax.loglog([5e-1, 5e3],[5e-1,5e3],'-b',alpha=0.3, label='Same efficacy', zorder=-1)
ax.loglog([5e0, 5e3],[5e-1,5e2],'--b',alpha=0.5, label='10 fold better efficacy',zorder=-1)
ax.loglog([5e1, 5e3],[5e-1,5e1],'-.b',alpha=0.7, label='100 fold better efficacy',zorder=-1)

ax.set_yscale('log')
ax.set_xscale('log')
ax.set_xlabel('IC$_{95}^{TMP}$ (µg/ml)')
ax.set_ylabel('IC$_{95}^{4\'-DTMP}$ (µg/ml)')
handles, labels= ax.get_legend_handles_labels()
ax.legend([handles[3]]+handles[5:]+handles[:3], [labels[3]]+labels[5:]+labels[:3],frameon=False,loc=2)

ax.axis('square')
ax.set_xlim(5e-1,5e3)
ax.set_ylim(5e-1,5e3)
fig.show()
fig.tight_layout(pad=.5)
fig.savefig('GenomicMutants-TMP-V041-2-SEM_ug.pdf',dpi=600,transparent=True)
fig.savefig('GenomicMutants-TMP-V041-2-SEM_ug.png',dpi=600,transparent=True)