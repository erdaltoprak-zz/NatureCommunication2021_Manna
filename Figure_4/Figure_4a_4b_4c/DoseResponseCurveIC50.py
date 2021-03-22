import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import curve_fit
from Colors import  tmpcolor, v041color, ic50erdal, rterdal, doseresponse, hillfit

df=pd.read_csv('Data_Restructured_NoBlank_02_04_2020.csv')
ic50s1=[]
ic50s2=[]
hs1=[]
hs2=[]
colors = [tmpcolor, v041color]
colors_r=[v041color]

def findHillCoeff(ax, x, y,tpos):
    popt, pcov = curve_fit(rterdal, x, np.log(y))
    xfit=np.linspace(0,21,100)
    yfit=rterdal(xfit, *popt)
    ax.plot(xfit,np.exp(yfit), '-xr')
    ax.text(*tpos,'h: '+str(round(popt[2],2)))
    return popt[2]


for i in range(len(df)):
    # row,col= (i//len(ax[0]), i%len(ax[0]))
    # cax=ax[row,col]
    y=df.iloc[i,-14:]
    x = np.array(y.index.astype(np.float))
    y=y.values
    popt1, pcov1 = curve_fit(doseresponse, x, y, bounds=((0.35, 0, 1),(1, 5000,15)))
    np.savez_compressed('Individual_Hill_Fit_Parameters_hVar/'+str(i)+'-'+df.Name[i]+'.npz', params=popt1, cov=pcov1)
    popt2, pcov2 = curve_fit(ic50erdal, x, y, bounds=((0.35, 0, 1), (1, 5000, 15)))
    np.savez_compressed('Erdal_Hill_Fit_Parameters/' + str(i) + '-' + df.Name[i] + '.npz', params=popt2, cov=pcov2)
    # fig,cax=plt.subplots()
    # xfit = np.logspace(np.log10(x.min()), np.log10(x.max()))
    # cax.semilogx(x,y,'-ok')
    # cax.semilogx(xfit,doseresponse(xfit,*popt),'-r')
    ic50s1.append(popt1[1])
    ic50s2.append(popt2[1])
    hs1.append(popt1[2])
    hs2.append(popt2[2])
df['fIC50-A']=ic50s1
df['fIC50-B']=ic50s2
df['h-A']=hs1
df['h-B']=hs2

hvals=dict(tmp=np.zeros(7),v041=np.zeros(8))

legendbool = ['full']+[False]*3+['full']+[False]*3
fig2, ax2 = plt.subplots(2, 4)
sns.set_style('ticks')
fig3, ax3 = plt.subplots(2, 4)
sns.set_style('ticks')
fIC50=['fIC50-A','fIC50-B']
for i in range(8):
    c=0
    for ax in [ax2,ax3]:
        row, col = (i // len(ax[0]), i % len(ax[0]))
        currax = ax[row, col]
        df0 = df.loc[(df['Day#'] == 0) & (df['TimeMeasured'] == 24), :]
        df1 = df.loc[(df['Culture#'] == i + 1) & (df['TimeMeasured'] == 24), :]
        df2 = pd.concat([df0, df1], axis='rows')
        if i==7:
            df2=df2.loc[df2['EvolvedIn']=='V041',:]
            sns.lineplot(x='Day#', y=fIC50[c], hue='EvolvedIn',
                         palette=colors_r, markers=True, marker='o', data=df2, ax=currax, legend=legendbool[i])
            a=df2.groupby(['EvolvedIn','Day#']).mean().reset_index()
            # hvals['v041'][i]=findHillCoeff(currax, range(22),a.loc[a['EvolvedIn']=='V041','fIC50'].values,(15,50))

        else:
            sns.lineplot(x='Day#', y=fIC50[c], hue='EvolvedIn',
                         palette=colors, data=df2, markers=True, marker='o', ax=currax,legend=legendbool[i])
            a = df2.groupby(['EvolvedIn', 'Day#']).mean().reset_index()
            # hvals['tmp'][i]=findHillCoeff(currax, range(22),a.loc[a['EvolvedIn']=='TMP','fIC50'].values,(0,1000))
            # hvals['v041'][i]=findHillCoeff(currax, range(22),a.loc[a['EvolvedIn']=='V041','fIC50'].values,(15,50))
        currax.set_yscale('log')
        currax.set_ylabel('IC$_{50}$ (µg/mL)')
        currax.set_xlabel('Time (d)')
        currax.set_ylim(1e-1,7e3)
        # currax.set_title('Culture-'+str(i+1),y=.9)
        if i in [0, 4]:
            sns.despine(ax=currax)
            handles, labels = currax.get_legend_handles_labels()
            currax.legend(handles[1:], ['TMP', '4\'-DTMP'], frameon=False, loc=4, bbox_to_anchor=(1.1,0))
        else:
            sns.despine(ax=currax, left=True)
            currax.set_yticklabels([])
            currax.yaxis.set_tick_params(width=0,which='both')
            currax.set_ylabel('')
        if i<4:
            currax.set_xlabel('')
        c+=1
    fig2.set_size_inches(6.8,3)
    fig2.tight_layout(pad=.5)
    fig3.set_size_inches(6.8, 3)
    fig3.tight_layout(pad=.5)
    # fig3.savefig('IndividualCultures-fIC50.pdf', dpi=600)
    # fig3.savefig('IndividualCultures-fIC50.png', transparent=True, dpi=600)

# fig4, ax4 = plt.subplots(2, 4)
# sns.set_style('ticks')
# # fIC50=['fIC50-A','fIC50-B']
# df['fIC95-A']=df['fIC50-A']* (19**(1/df['h-A']))
# df['fIC95-B']=df['fIC50-B']* (19**(1/df['h-B']))
# for i in range(8):
#     row, col = (i // len(ax4[0]), i % len(ax4[0]))
#     currax = ax4[row, col]
#     df0 = df.loc[(df['Day#'] == 0) & (df['TimeMeasured'] == 24), :]
#     df1 = df.loc[(df['Culture#'] == i + 1) & (df['TimeMeasured'] == 24), :]
#     df2 = pd.concat([df0, df1], axis='rows')
#     if i==7:
#         df2=df2.loc[df2['EvolvedIn']=='V041',:]
#         sns.lineplot(x='Day#', y='fIC50-B', hue='EvolvedIn',
#                      palette=colors_r, markers=True, marker='o', data=df2, ax=currax, legend=legendbool[i])
#     else:
#         sns.lineplot(x='Day#', y='fIC50-B', hue='EvolvedIn',
#                      palette=colors, data=df2, markers=True, marker='o', ax=currax,legend=legendbool[i])
#     currax.set_yscale('log')
#     currax.set_ylabel('IC$_{50}$ (µg/mL)')
#     currax.set_xlabel('Time (d)')
#     currax.set_ylim(4e-1,1.5e4)
#     # currax.set_title('Culture-'+str(i+1),y=.9)
#     if i in [0, 4]:
#         sns.despine(ax=currax)
#         handles, labels = currax.get_legend_handles_labels()
#         currax.legend(handles[1:], ['TMP', '4\'-DTMP'], frameon=False, loc=4, bbox_to_anchor=(1.1,0))
#     else:
#         sns.despine(ax=currax, left=True)
#         currax.set_yticklabels([])
#         currax.yaxis.set_tick_params(width=0,which='both')
#         currax.set_ylabel('')
#     if i<4:
#         currax.set_xlabel('')
#
#     fig4.set_size_inches(6.8, 3)
#     fig4.tight_layout(pad=.5)
#     fig4.savefig('IndividualCultures-fIC50.pdf', dpi=600)
#     fig4.savefig('IndividualCultures-fIC50.png', transparent=True, dpi=600)

df.to_csv('DataWithHillFitParameters.csv',index=False)

fig5, ax5=plt.subplots()
sns.set_style('ticks')
sns.despine()
df24h=df.loc[df.TimeMeasured==24,:]
print(0, df24h.shape)
for j in range(1,9):
    if j==8:
        d0=df24h.loc[(df24h['Culture#']==0)&(df24h['EvolvedIn']=='V041'),:]
    else:
        d0 = df24h.loc[df24h['Culture#'] == 0, :]
    d0['Culture#']=j
    df24h=pd.concat([df24h, d0],axis='rows')
    print(j, df24h.shape)
sns.lineplot('Day#','fIC50-B',hue='EvolvedIn',units='Culture#',data=df24h,
             palette=colors, lw=.5, estimator=None, alpha=.75)
sns.lineplot('Day#','fIC50-B',hue='EvolvedIn',data=df24h,
             palette=colors, lw=2.5,  ci=0, markers=True, marker='o', markersize=6)
ax5.set_yscale('log')
ax5.set_yticks([.3, 3, 30, 300, 3000])
ax5.set_yticklabels([.3, 3, 30, 300, 3000])
ax5.set_ylim(.3,3000)
ax5.set_ylabel('IC$_{50}$ (µg/mL)')
ax5.set_xlabel('Time (d)')
handles, labels = ax5.get_legend_handles_labels()
ax5.legend(handles[1:3], ['TMP', '4\'-DTMP'], frameon=False, loc=4, fontsize=10)
fig5.set_size_inches(3.6, 2.4)
fig5.tight_layout(pad=.5)
# fig5.savefig('All_IC50_Curves-2.png',dpi=600,transparent=True)
# fig5.savefig('All_IC50_Curves-2.pdf',dpi=600)
