import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from Colors import tmpcolor, v041color, rterdal
from scipy.optimize import curve_fit
df=pd.read_csv('DataWithHillFitParameters.csv')
df=df.loc[df['TimeMeasured']==24,:]
df2=df.loc[:,['Name','EvolvedIn','Culture#','Day#','fIC50-B','h-B']]
palette=[tmpcolor, v041color]
fig,ax=plt.subplots()
sns.set_style('ticks')
sns.despine()

sns.lineplot(x='Day#',y='h-B',hue='EvolvedIn',data=df2,
             err_style='bars',ci=67,markers=True,marker='o',
             ax=ax, palette=palette)
ax.set_ylim(0,15)
ax.set_xlabel('Time (days)')
ax.set_ylabel('Hill Coefficient')
ax.legend(frameon=False)
fig.set_size_inches(6,4)
# fig.savefig('HillCoefficient_Days.pdf',dpi=600)
# fig.savefig('HillCoefficient_Days.png',transparent=True,dpi=600)


df3=df2.groupby(by=['EvolvedIn','Culture#','Day#']).mean().reset_index()
for i in range(7):
    l=df3.iloc[0,:]
    l['Culture#']=i+1
    df3.loc[len(df3)] =l
for i in range(8):
    l2=df3.iloc[148,:]
    l2['Culture#']=i+1
    df3.loc[len(df3)] =l2

bounds=((1e-1,100,.1),(1.5,12000,2))
df3=df3.loc[df3['Culture#']>0,:]
df3.sort_values(by=['EvolvedIn','Culture#','Day#'],inplace=True)
rEvo=dict(tmp=[],v041=[])

fig,ax=plt.subplots(2,4,sharex=True,sharey=True)
sns.set_style('ticks')
sns.despine()
for i in range(1,9):
    row,col= ((i-1)//len(ax[0]), (i-1)%len(ax[0]))
    cax=ax[row,col]
    xfit=np.linspace(0,21,100)
    x = range(22)
    if i==8:
        dV=df3.loc[(df3['EvolvedIn']=='V041')&(df3['Culture#']==i),:]
        poptV, pcovV= curve_fit(rterdal, dV['Day#'],dV['fIC50-B'], bounds=bounds)
        yfitV=rterdal(xfit,*poptV)
        rEvo['v041'].append(poptV[2])
        yV = dV['fIC50-B']
        cax.semilogy(x, yV, '-o', color=v041color)
        cax.semilogy(xfit, yfitV,'-r')
        print(i, poptV[2])
    else:
        dV = df3.loc[(df3['EvolvedIn'] == 'V041') & (df3['Culture#'] == i), :]
        poptV, pcovV = curve_fit(rterdal, dV['Day#'], dV['fIC50-B'], bounds=bounds)
        dT = df3.loc[(df3['EvolvedIn'] == 'TMP') & (df3['Culture#'] == i), :]
        poptT, pcovT = curve_fit(rterdal, dT['Day#'], dT['fIC50-B'], bounds=bounds)
        rEvo['tmp'].append(poptT[2])
        rEvo['v041'].append(poptV[2])
        yfitT = rterdal(xfit, *poptT)
        yfitV = rterdal(xfit, *poptV)

        yT=dT['fIC50-B']
        yV = dV['fIC50-B']
        cax.semilogy(x, yT, '-o', color=tmpcolor)
        cax.semilogy(x, yV, '-o', color=v041color)
        cax.semilogy(xfit, yfitT, '-r', xfit, yfitV,'-r')
        cax.set_xlabel('Time (days)')
        cax.set_ylim(1e-1, 1.5e4)
        print(i, poptT[2], poptV[2])
    if i in [1, 5]:
        sns.despine(ax=cax)
        handles, labels = cax.get_legend_handles_labels()
        cax.legend(handles[1:], ['TMP', '4\'-DTMP'], frameon=False, loc=4, bbox_to_anchor=(1.1,0))
        cax.set_ylabel('[Drug] (µg/mL)')
        cax.set_yticklabels([1,1e1,1e2,1e3,1e4])
    else:
        sns.despine(ax=cax, left=True)
        # cax.set_yticklabels([])
        cax.yaxis.set_tick_params(width=0,which='both')
        cax.set_ylabel('')
    if i<5:
        cax.set_xlabel('')



FinalResistance=dict(tmp=[],v041=[])
FinalResistance['tmp']=df3.loc[(df3['EvolvedIn']=='TMP')&(df3['Day#']==21),'fIC50-B'].values
FinalResistance['v041']=df3.loc[(df3['EvolvedIn']=='V041')&(df3['Day#']==21),'fIC50-B'].values

fig2,ax2=plt.subplots()
sns.set_style('ticks')
sns.despine()
ax2.plot(rEvo['tmp'],FinalResistance['tmp'],'o',color=tmpcolor,label='TMP')
ax2.plot(rEvo['v041'],FinalResistance['v041'],'o',color=v041color,label='4\'-DTMP')
ax2.set_xlabel('Hill Coefficient')
ax2.set_ylabel('Resistance to Drug (µg/mL)')
ax2.legend(frameon=False, loc=2)


rmTMP=np.mean(rEvo['tmp'])
rsTMP=np.std(rEvo['tmp'])
rmFRTMP=np.mean(FinalResistance['tmp'])
rsFRTMP=np.std(FinalResistance['tmp'])

rmV041=np.mean(rEvo['v041'])
rsV041=np.std(rEvo['v041'])
rmFRV041=np.mean(FinalResistance['v041'])
rsFRV041=np.std(FinalResistance['v041'])

fig3,ax3=plt.subplots()
sns.set_style('ticks')
sns.despine()
ax3.errorbar(rmTMP,rmFRTMP,xerr=rsTMP,yerr=rsFRTMP,marker='o',color=tmpcolor,label='TMP')
ax3.errorbar(rmV041,rmFRV041,xerr=rsV041,yerr=rsFRV041,marker='o',color=v041color,label='4\'-DTMP')
ax3.set_xlabel('Rate of Evolution (1/day)')
ax3.set_ylabel('Final Resistance (µg/mL)')
ax3.set_yscale('log')
ax3.set_xlim(0,1)
ax3.set_ylim(1e2,2e3)
ax3.set_yticks([100, 200, 400, 800, 1600])
ax3.set_yticklabels([100, 200, 400, 800, 1600])
ax3.legend(frameon=False, loc=2)
fig3.set_size_inches(3, 2.4)
fig3.tight_layout(pad=.5)
# fig3.savefig('HillCoeff_FinalResistance(IC50)-2.pdf',dpi=600)
# fig3.savefig('HillCoeff_FinalResistance(IC50)-2.png',transparent=True,dpi=600)

from scipy.stats import ttest_ind
print(ttest_ind(rEvo['tmp'], rEvo['v041']))
print(ttest_ind(FinalResistance['tmp'], FinalResistance['v041']))


# Plotting of One Example Evolution Rate Calculation
fig,ax=plt.subplots()
sns.set_style('ticks')
sns.despine()
c=0
for i in [7]:
    cax=ax#[c]
    c+=1
    xfit=np.linspace(0,21,100)
    x = range(22)
    if i==8:
        dV=df3.loc[(df3['EvolvedIn']=='V041')&(df3['Culture#']==i),:]
        poptV, pcovV= curve_fit(rterdal, dV['Day#'],dV['fIC50-B'], bounds=bounds)
        yfitV=rterdal(xfit,*poptV)
        rEvo['v041'].append(poptV[2])
        yV = dV['fIC50-B']
        cax.semilogy(x, yV, '-o', color=v041color)
        cax.semilogy(xfit, yfitV,'-r')
        print(i, poptV[2])
    else:
        dV = df3.loc[(df3['EvolvedIn'] == 'V041') & (df3['Culture#'] == i), :]
        poptV, pcovV = curve_fit(rterdal, dV['Day#'], dV['fIC50-B'], bounds=bounds)
        dT = df3.loc[(df3['EvolvedIn'] == 'TMP') & (df3['Culture#'] == i), :]
        poptT, pcovT = curve_fit(rterdal, dT['Day#'], dT['fIC50-B'], bounds=bounds)
        rEvo['tmp'].append(poptT[2])
        rEvo['v041'].append(poptV[2])
        yfitT = rterdal(xfit, *poptT)
        yfitV = rterdal(xfit, *poptV)

        yT=dT['fIC50-B']
        yV = dV['fIC50-B']
        cax.semilogy(x, yT, '-o', color=tmpcolor, markeredgecolor='w')
        cax.semilogy(x, yV, '-o', color=v041color, markeredgecolor='w')
        cax.semilogy(xfit, yfitT, '-r', xfit, yfitV,'-r')
        cax.set_xlabel('Time (d)')
        cax.set_ylabel('IC$_{50}$ (µg/mL)')
        cax.set_ylim(1e-1, 1.5e4)
        print(i, poptT[2], poptV[2])
    # if i in [1, 5]:
    #     sns.despine(ax=cax)
    #     handles, labels = cax.get_legend_handles_labels()
    #     cax.legend(handles[1:], ['TMP', '4\'-DTMP'], frameon=False, loc=4, bbox_to_anchor=(1.1,0))
    #     cax.set_ylabel('[Drug] (µg/mL)')
    #     cax.set_yticklabels([1,1e1,1e2,1e3,1e4])
    # else:
    #     sns.despine(ax=cax, left=True)
    #     # cax.set_yticklabels([])
    #     cax.yaxis.set_tick_params(width=0,which='both')
    #     cax.set_ylabel('')
    # if i<5:
    #     cax.set_xlabel('')

fig.set_size_inches(3.6,2.4)
fig.tight_layout(pad=.5)
fig.savefig('OneExample.pdf',dpi=600,transparent=True)
fig.savefig('OneExample.png',dpi=600,transparent=True)